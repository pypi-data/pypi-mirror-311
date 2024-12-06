import math
import pickle
from collections import defaultdict
from pathlib import Path

ISO_639_1_CODES = {"et", "en"}


class NgramModelBuilder:
    def __init__(
            self,
            n: int = 2,
            lang: str | None = None,
            accepted_chars: str = "abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' "
    ):
        """
        Initialize the NgramModelBuilder.

        Parameters
        ----------
        n : int
            The size of the n-grams (e.g., 2 for bigrams, 3 for trigrams).
        lang : str
            Language code (ISO-639-1).
        accepted_chars : str
            A string of accepted characters for the n-gram model.

        Raises
        ------
        ValueError
            If the lang parameter is not a valid ISO-639-1 code.
        """

        if lang is not None and lang not in ISO_639_1_CODES:
            raise ValueError(f"Invalid language code '{lang}'. Must be ISO-639-1 code and one of {ISO_639_1_CODES}.")

        self.n = n
        self.lang = lang
        self.accepted_chars = accepted_chars
        self.char_count = len(self.accepted_chars)
        self.ngram_counts = defaultdict(lambda: defaultdict(int))
        self.log_probabilities = defaultdict(dict)  # Prefix -> {Suffix: log probability}

    def _normalize(self, text: str) -> str:
        """
        Normalize text by converting to lowercase and removing unaccepted characters.

        Parameters
        ----------
        text : str
            Text to be normalized.

        Returns
        -------
        str
            Normalized text.
        """
        return "".join([c.lower() for c in text if c.lower() in self.accepted_chars])

    def build_model(self, text_corpus: str) -> dict[str, dict[str, float]]:
        """
        Build the n-gram model based on the given text corpus.

        Parameters
        ----------
        text_corpus : str
            Text to build the n-gram model from.

        Returns
        -------
        dict[str, dict[str, float]]
            The log probability dictionary.
        """

        normalized_text = self._normalize(text_corpus)

        for i in range(len(normalized_text) - self.n + 1):
            ngram = normalized_text[i:i + self.n]
            prefix = ngram[:-1]
            suffix = ngram[-1]
            self.ngram_counts[prefix][suffix] += 1

        for prefix, suffix_counts in self.ngram_counts.items():
            total_count = sum(suffix_counts.values())
            for suffix in self.accepted_chars:
                count = self.ngram_counts[prefix].get(suffix, 0) + 1  # Add-one smoothing
                prob = count / total_count
                self.log_probabilities[prefix][suffix] = math.log(prob)

        return self.log_probabilities

    def save_model(self, log_probabilities: dict[str, dict[str, float]], file_path: str) -> None:
        """
        Save the model as a dictionary to a pickle file.

        Parameters
        ----------
        log_probabilities : dict[str, dict[str, float]]
            The log probability dictionary.
        file_path : str
            The model save path.

        Returns
        -------
        None
        """

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        model_dict = {
            "n_gram": self.n,
            "accepted_chars": self.accepted_chars,
            "log_probabilities": log_probabilities
        }

        if self.lang:
            model_dict["lang"] = self.lang

        with open(file_path, "wb") as f:
            pickle.dump(model_dict, f)
