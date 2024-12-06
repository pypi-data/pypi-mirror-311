import pytest

from rara_text_evaluator.quality_validator import QualityValidator, DEFAULT_RESPONSE, DEFAULT_TEXT_SIZE_REQUIREMENT


def test_quality_evaluator_process():
    validator = QualityValidator()
    text = "Elas kord üks muinasjutt ja see muinasjutt sai läbi!!"
    probability = validator.get_probability(text)
    assert len(text) > DEFAULT_TEXT_SIZE_REQUIREMENT
    assert probability > DEFAULT_RESPONSE


def test_short_text_returning_default_response():
    validator = QualityValidator()
    text = "See on lühike!"
    probability = validator.get_probability(text)
    assert len(text) < DEFAULT_TEXT_SIZE_REQUIREMENT
    assert probability == DEFAULT_RESPONSE


def test_fallback_language_being_used():
    validator = QualityValidator()
    text = ("Maanantaista torstaihin herään viisitoista yli seitsemän. "
            "Perjantaisin herään kahdeksalta, koska oppituntini alkavat myöhemmin. "
            "Herättyäni syön aamupalaa, puen päälleni ja menen kouluun.!")
    validator.get_probability(text)
    assert validator.model_lang is None


def test_using_defined_language_instead_of_autodetect():
    validator = QualityValidator()
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    validator.get_probability(text, lang="en")
    assert validator.model_lang == "en"


def test_using_wrong_language_code_results_in_fallback():
    validator = QualityValidator()
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    language_code = "fin"
    validator.get_probability(text, lang=language_code)
    assert language_code not in validator.language_model_container
    assert validator.model_lang is None


def test_different_texts_returning_unique_test_quality_answers():
    validator = QualityValidator()
    texts = [
        "Teadavasti, kui inimene on kergem kui part, siis ta on nõid!",
        "Võtke pühalt käsigranaadilt tema kaitse ja lugege arve kolm, ei loe mitte kaks ja kindlasti mitte neli.",
        "Mis on su nimi? Kust sa tuled? Mis on ühe pääsukese maksimum lendamiskiirus?"
    ]

    qualities = []
    for text in texts:
        qualities.append(validator.get_probability(text))

    assert len(set(qualities)) == len(texts)


def test_exception_being_thrown_when_no_models_loaded():
    validator = QualityValidator(load_defaults=False)
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    with pytest.raises(ValueError):
        validator.get_probability(text, lang="et")
