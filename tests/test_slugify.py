from steerer.services import slugify


def test_spaces():
    assert slugify("hello world") == "hello-world"


def test_uppercase():
    assert slugify("Hello World") == "hello-world"


def test_consecutive_hyphens():
    assert slugify("hello   world") == "hello-world"


def test_special_chars():
    assert slugify("hello!@#world") == "hello-world"
