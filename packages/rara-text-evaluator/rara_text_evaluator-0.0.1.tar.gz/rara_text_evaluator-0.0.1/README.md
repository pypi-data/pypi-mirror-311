## How to install

1. Clone this repository.
1. Ensure you have Git LFS hooks installed with ```git lfs install```.
1. Create a Python environment with Python 3.10 or above.
1. Install build with ```pip install build```
1. Run ```python -m build``` inside the repository.
1. Run ```pip install .```

# How to test

1. Clone the repository.
1. Create a Python environment with Python 3.10 or above.
1. Install build with ```pip install build```
1. Run ```python -m build``` inside the repository.
1. Install the library with its testing module ```pip install .[testing]```
1. Run the tests inside the repository root ```pytest```

## Text Quality Validator Module Overview

This documentation describes two classes:

`NgramModelBuilder (ngram_model_builder.py)`

`QualityValidator (quality_validator.py)`

### NgramModelBuilder

The class takes a given text corpus and builds an n-gram model, which contains the probability distribution of
character sequences and supports assigning the model's language using an ISO-639-1 language code.

#### Functions

`build_model(self, text_corpus: str) -> list[list[float]]`

Creates an n-gram model based on the given text corpus and returns a logarithmic probability matrix.

`save_model(self, log_prob_matrix: list[list[float]], file_path: str) -> None`

Saves the n-gram model as a pickle file, including metadata such as `n`, `accepted_chars`, and optionally `lang`.

#### Example Usage

```python
from rara_text_evaluator.ngram_model_builder import NgramModelBuilder

nmb = NgramModelBuilder(n=2, lang='et', accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
text_corpus = "Hello, I am a text corpus. You probably want a larger text corpus for better results."
log_probabilities = nmb.build_model(text_corpus)
nmb.save_model(log_probabilities, "ngram_model.pkl")
```

### QualityValidator

The class uses a pre-built model to assess the quality of the provided text and supports automatic
fallback models if the language detected in the input text does not match the `lang` parameter of the model.

If the primary language is already language-agnostic, the fallback model is not necessary.
However, if the primary model is language-specific, the fallback model should be used to support multiple languages.

The current models in use can be found in `src/rara_text_evaluator/models`:

- `text_validator_ngram_3_et.pkl` (Estonian)
    - Trained on DIGAR "born digital" articles (from
      `/var/data/articles_for_quality_assessment_training/digar_1_born_digital_texts.jl` on the `rara-dev.texta.ee`
      server)
    - Words: `4 164 975`, Characters: `30 630 998`
- `text_validator_ngram_3_en.pkl` (English)
    - Trained on NLTK corpora ([gutenberg, brown, reuters, webtext](https://www.nltk.org/nltk_data/))
    - Words: `5 900 439`, Characters: `28 649 578`
- `text_validator_ngram_3_fallback.pkl` (language-agnostic)
    - Trained on the combined DIGAR and NLTK corpora
    - Words: `10 065 413`, Characters: `59 280 576`

To test the model, mainly the fallback one which does not require a specific language,
a collection of DIGAR articles unseen during training were used under the assumption that older,
reformatted digital texts would be more error-prone and thus should have a lower score.

The distribution of publication dates per digitization type for the articles is shown below.
Source: `/var/data/articles/digar_1.jl`

![Distribution of Publication Dates by Digitization Type](images/digitizationtypebydate.png)

Exactly 10 000 samples were taken from both the born digital and the reformatted digital categories,
and their text quality assessment scores were calculated. From the following graph, it can be seen that older texts
indeed are more error-prone, as the distribution of scores for the reformatted digital category is shifted towards
lower scores.

This can additionally be used as a visual reference for setting a threshold for
acceptable text quality scores. As a rough estimate, a score of around `0.6 - 0.7` could be used as a threshold,
as most digitally born texts have a score above this value, whereas most reformatted digital texts
fall below it.

![Text Quality Assessment Histogram](images/textqualityassessment_agnostic.png)

#### Functions

`get_probability(self, text: str, default_response: float = 0.0, length_limit: int = 30, lang: str | None = None) -> float`

Returns the probability that the given text is readable and error-free, based on the average transition probability.
The score also passes through a sigmoid function to ensure it is within the range [0, 1].

**Note**: Texts that are too short (<30 characters by default or the value of length_limit) or contain only spaces
return a score of 0 (value of
default_response).

`add_model(self, language: str, model_path: str) -> None`

Allows the user to add a model from a file path into the model storage,
either to overwrite existing languages or adding new ones.

To overwrite the fallback model use the QueryValidator.FALLBACK_MODEL_KEY
as the language parameter.

#### Example Usage

```python
from rara_text_evaluator.quality_validator import QualityValidator

qv = QualityValidator()
test_text = "Hello, I am a test text. I should be at least 30 characters long."
print(qv.get_probability(test_text))
```
