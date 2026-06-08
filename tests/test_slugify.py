from steerer.services import slugify


def test_spaces():
    assert slugify("hello world") == "hello-world"


def test_uppercase():
    assert slugify("Hello World") == "hello-world"


def test_consecutive_hyphens():
    assert slugify("hello   world") == "hello-world"


def test_special_chars():
    assert slugify("hello!@#world") == "hello-world"


def test_only_special_chars():
    assert slugify("!@#$%") == ""


def test_only_dashes():
    assert slugify("---") == ""


def test_strips_leading_and_trailing_dashes():
    assert slugify("!hello!") == "hello"
