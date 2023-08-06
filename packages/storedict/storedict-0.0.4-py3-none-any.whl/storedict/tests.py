import pytest
from storedict import create_store


@pytest.fixture(params=[None, "http://localhost:8200"])
def store(request):
    """
    Test both LocalStore() and ProductionStore().
    """
    return create_store(request.param)


@pytest.fixture(autouse=True)
def clear_store(store):
    """
    Clear the store before and after each test.
    """
    store.clear()
    yield
    store.clear()


def test_getitem(store):
    with pytest.raises(KeyError):
        store["foo"]

    store["foo"] = "bar"
    assert store["foo"] == "bar"


def test_setitem(store):
    store["foo"] = "bar"
    assert store["foo"] == "bar"


def test_delitem(store):
    with pytest.raises(KeyError):
        del store["foo"]

    store["foo"] = "bar"
    del store["foo"]
    with pytest.raises(KeyError):
        store["foo"]


def test_iter(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(iter(store)) == ["foo", "baz"]


def test_len(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert len(store) == 2


def test_contains(store):
    assert "foo" not in store
    store["foo"] = "bar"
    assert "foo" in store
    del store["foo"]
    assert "foo" not in store


def test_get(store):
    assert store.get("foo") is None
    assert store.get("foo", "bar") == "bar"

    store["foo"] = "bar"
    assert store.get("foo") == "bar"
    assert store.get("foo", "baz") == "bar"


def test_items(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.items()) == [("foo", "bar"), ("baz", "qux")]


def test_keys(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.keys()) == ["foo", "baz"]


def test_values(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.values()) == ["bar", "qux"]


def test_clear(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    store.clear()
    assert len(store) == 0
    assert list(store.items()) == []


def test_validate_key(store):
    """Keys must always be strings"""
    with pytest.raises(TypeError):
        store[1]  # __getitem__
    with pytest.raises(TypeError):
        store[1] = 2  # __setitem__
    with pytest.raises(TypeError):
        del store[1]  # __delitem__
    with pytest.raises(TypeError):
        1 in store  # __contains__
    with pytest.raises(TypeError):
        store.get(1)  # get


def test_validate_value(store):
    # Allowed types
    store["foo"] = "bar"
    store["foo"] = 1
    store["foo"] = False
    store["foo"] = {"bar": 1}
    store["foo"] = [1, 2, 3]

    with pytest.raises(TypeError):
        store["foo"] = (1, 2, 3)
    with pytest.raises(TypeError):
        store["foo"] = {"bar": (1, 2, 3)}

    # Dict key must be a string
    with pytest.raises(TypeError):
        store["foo"] = {1: 2}
    with pytest.raises(TypeError):
        store["foo"] = {"bar": {1: 2}}
