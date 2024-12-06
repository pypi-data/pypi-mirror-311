import logging
import math
import pickle
from importlib import resources

from langdetect import detect, DetectorFactory, LangDetectException

logger = logging.getLogger(__name__)

DEFAULT_RESPONSE = 0.0
DEFAULT_TEXT_SIZE_REQUIREMENT = 30


class QualityValidator:
    FALLBACK_MODEL_KEY = "fallback"

    def __init__(self, load_defaults: bool = True):
        """
        Initializes the QualityValidator by loading the primary and optional fallback models.

        Parameters
        ----------
        load_defaults : bool
            Whether to automatically load the default models into the memory.
            If set to False, models including a fallback one must be loaded using the add_model() method.

        """
        DetectorFactory.seed = 0  # Set seed for langdetect to ensure consistent results

        self.default_model_mapping = {
            "et": "text_validator_ngram_3_et.pkl",
            "en": "text_validator_ngram_3_en.pkl",
            self.FALLBACK_MODEL_KEY: "text_validator_ngram_3_fallback.pkl",
        }

        self.language_model_container = {}
        if load_defaults:
            self._load_default_language_models()

    def _load_default_language_models(self) -> None:
        for language, name in self.default_model_mapping.items():
            path = resources.files(f"rara_text_evaluator.models")
            self.language_model_container[language] = self._load_model(path / name)

    def _load_model(self, model_path: str):
        with open(model_path, "rb") as f:
            return pickle.load(f)

    def _set_model(self, model_data: dict) -> None:
        """
        Set the current model to use based on the model data dictionary.

        Parameters
        ----------
        model_data : dict
            The model data dictionary containing model parameters and data.

        Returns
        -------
        None
        """
        self.model_data = model_data
        self.n = model_data["n_gram"]
        self.model_lang = model_data.get("lang")
        self.accepted_chars = model_data["accepted_chars"]
        self.log_probabilities = model_data["log_probabilities"]
        self.char_count = len(self.accepted_chars)

    def _normalize(self, line: str) -> str:
        """
        Normalize text by converting to lowercase and removing unaccepted characters.
        """
        return "".join([c.lower() for c in line if c.lower() in self.accepted_chars])

    def _ngram(self, n: int, text: str) -> tuple:
        """
        Return all n-grams from text after normalizing.
        """
        filtered = self._normalize(text)
        for start in range(len(filtered) - n + 1):
            ngram = filtered[start:start + n]
            prefix = ngram[:-1]
            suffix = ngram[-1]
            yield (prefix, suffix)

    def _get_avg_transition_prob(self, text: str) -> float:
        """
        Returns the average transition probability from the text using log probabilities.
        """
        log_prob = 0.0
        transition_ct = 0

        for prefix, suffix in self._ngram(self.n, text):
            if prefix in self.log_probabilities and suffix in self.log_probabilities[prefix]:
                log_prob += self.log_probabilities[prefix][suffix]
            else:
                log_prob += math.log(1 / (self.char_count * 2))  # Smoothing for unseen n-grams
            transition_ct += 1

        return math.exp(log_prob / (transition_ct or 1))

    def _detect_language(self, text: str) -> str | None:
        """
        Detect the language of the provided text, return None if detection fails
        (for example if the text contains no alphabetic characters).

        Parameters
        ----------
        text : str
            Input text to detect language from.

        Returns
        -------
        str
            Detected language code (ISO-639-1) or None if detection fails.
        """
        try:
            return detect(text)
        except LangDetectException:
            return None

    def _detect_and_set_model(self, text: str, lang: str | None = None) -> None:
        """
        Validate the detected language and switch to the appropriate model if necessary.
        Skips validation if no fallback model is provided.

        Parameters
        ----------
        text : str
            The text for which the language needs to be validated.

        lang : str
            Language code for the given text, if set to None will use langdetect to automatically detect the language.

        Returns
        -------
        None
        """
        detected_lang = lang or self._detect_language(text)

        if detected_lang in self.language_model_container:
            self._set_model(self.language_model_container[detected_lang])
            logger.info(f"{detected_lang=} == {self.model_lang=}, using primary model.")
        else:
            self._set_model(self.language_model_container[self.FALLBACK_MODEL_KEY])
            logger.info(f"{detected_lang=} != {self.model_lang=}, using fallback model.")

    def _sigmoid(self, x: float, x0: float = 0.05, k: float = 50.0) -> float:
        """
        Sigmoid function to calculate the probability based on the average transition probability.

        Parameters
        ----------
        x : float
            The average transition probability.
        x0 : float, optional
            The x value of the sigmoid midpoint, by default 0.05.
        k : float, optional
            The steepness of the sigmoid, by default 50.0.

        Returns
        -------
        float
            The probability that the text is readable.
        """
        return 1 / (1 + math.exp(-k * (x - x0)))

    def add_model(self, language: str, model_path: str) -> None:
        """
        Allows the user to add a model from a file path into the model storage,
        either to overwrite existing languages or adding new ones.

        To overwrite the fallback model use the QueryValidator.FALLBACK_MODEL_KEY
        as the language parameter.
        """
        self.language_model_container[language] = self._load_model(model_path)

    def _validate_model_registry(self):
        if self.FALLBACK_MODEL_KEY not in self.language_model_container:
            raise ValueError("There must always be a fallback model loaded into memory!")

    def get_probability(
            self,
            text: str,
            default_response: float = DEFAULT_RESPONSE,
            length_limit: int = DEFAULT_TEXT_SIZE_REQUIREMENT,
            lang: str | None = None
    ) -> float:
        """
        Calculate the probability that the given text seems readable and is not full of artifacts.
        Method uses a sigmoid function to calculate the probability based on the average transition probability.

        Parameters
        ----------
        text : str
            The text to calculate the probability for.

        default_response : float
            What number to return if the text doesn't reach the required length.

        length_limit : int
            Maximum number of characters for text without leading or trailing whitespace.

        lang : str
            Language code for the given text, if set to None will use langdetect to automatically detect the language.

        Returns
        -------
        float
            The probability that the text is readable
        """
        self._validate_model_registry()

        if len(text.strip()) < length_limit:
            logger.info(f"Text must be >={length_limit} characters long without leading or trailing whitespace.")
            return default_response

        self._detect_and_set_model(text, lang=lang)
        sigmoid_prob = self._sigmoid(self._get_avg_transition_prob(text))

        return sigmoid_prob
