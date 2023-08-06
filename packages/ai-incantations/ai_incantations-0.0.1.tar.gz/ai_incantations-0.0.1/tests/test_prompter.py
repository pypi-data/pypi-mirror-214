import pytest
from ai_incantations.prompter import Incantation


def test_deserialize():
    prompts = Incantation("tests/test_data.llmp")
    assert isinstance(prompts.data, dict)


def test_interpolate_single_placeholder():
    prompts = Incantation("tests/test_data.llmp")
    content = prompts.category.key1
    result = prompts.interpolate(content, {"var1": "test"})
    assert result == "This is a test string."


def test_interpolate_multiple_placeholders():
    prompts = Incantation("tests/test_data.llmp")
    content = prompts.category.key2
    result = prompts.interpolate(content, {"var1": "test", "var2": "word"})
    assert result == "This is a test string with a word."


def test_interpolate_missing_placeholder():
    prompts = Incantation("tests/test_data.llmp")
    content = prompts.category.key2
    with pytest.raises(KeyError) as e:
        prompts.interpolate(content, {"var1": "test"})

    assert str(e.value) == "'Error: The var2 key was not found in the provided values.'"
