import pathlib

import pytest

from rara_text_evaluator.ngram_model_builder import NgramModelBuilder
from rara_text_evaluator.quality_validator import QualityValidator, DEFAULT_RESPONSE

DEFAULT_FILENAME = "ngram_model.pkl"


@pytest.fixture(autouse=True)
def delete_model_file():
    yield
    path = pathlib.Path(DEFAULT_FILENAME)
    path.unlink()
    assert path.exists() is False


def test_model_training_process_with_et_text(delete_model_file):
    language = 'et'
    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
    text_corpus = "Kas sa oled teadlik sellest et märgade mõõkade loopimine ei ole alus ühe õiglase valitsuse loomiseks!?"
    log_probabilities = nmb.build_model(text_corpus)
    nmb.save_model(log_probabilities, DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()

    qv = QualityValidator()
    qv.add_model(language=language, model_path=DEFAULT_FILENAME)
    probability = qv.get_probability("You should be aware that asking whether an african or european swallow is faster is inappropriate!")
    assert probability != DEFAULT_RESPONSE


def test_model_training_process_with_en_text(delete_model_file):
    language = 'en'
    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyz.,:;-_!\"()%@1234567890' ")
    text_corpus = "Are you not aware that throwing around wet scimitars is no basis for a true government!?"
    log_probabilities = nmb.build_model(text_corpus)
    nmb.save_model(log_probabilities, DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()

    qv = QualityValidator()
    qv.add_model(language=language, model_path=DEFAULT_FILENAME)
    probability = qv.get_probability("You should be aware that it's inappropriate to ask whether an european or african swallow is faster!")
    assert probability != DEFAULT_RESPONSE
