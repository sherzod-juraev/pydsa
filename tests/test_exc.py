import pytest

from pydsa.exc import (
    EdgeNotFoundError,
    EmptyError,
    IndexOutOfRangeError,
    InvalidPathError,
    InvalidValueError,
    KeyNotFoundError,
    NotFoundError,
    PydsaError,
    VertexNotFoundError,
)

ALL_ERRORS = [
    EmptyError,
    IndexOutOfRangeError,
    NotFoundError,
    KeyNotFoundError,
    VertexNotFoundError,
    EdgeNotFoundError,
    InvalidValueError,
    InvalidPathError,
]

BUILTIN_BASES = [
    (NotFoundError, KeyError),
    (KeyNotFoundError, KeyError),
    (VertexNotFoundError, KeyError),
    (EdgeNotFoundError, KeyError),
    (IndexOutOfRangeError, IndexError),
    (InvalidValueError, ValueError),
    (InvalidPathError, ValueError),
]


class TestHierarchy:
    def test_pydsa_error_is_an_exception(self) -> None:
        assert issubclass(PydsaError, Exception)

    @pytest.mark.parametrize("error", ALL_ERRORS)
    def test_every_error_derives_from_pydsa_error(self, error: type[Exception]) -> None:
        assert issubclass(error, PydsaError)

    @pytest.mark.parametrize(
        ("child", "parent"),
        [
            (KeyNotFoundError, NotFoundError),
            (VertexNotFoundError, NotFoundError),
            (EdgeNotFoundError, NotFoundError),
            (InvalidPathError, InvalidValueError),
        ],
    )
    def test_category_parent(self, child: type[Exception], parent: type[Exception]) -> None:
        assert issubclass(child, parent)

    @pytest.mark.parametrize(
        ("error", "other"),
        [
            (EmptyError, NotFoundError),
            (EmptyError, InvalidValueError),
            (IndexOutOfRangeError, NotFoundError),
            (NotFoundError, InvalidValueError),
            (KeyNotFoundError, VertexNotFoundError),
            (VertexNotFoundError, EdgeNotFoundError),
            (InvalidPathError, NotFoundError),
        ],
    )
    def test_unrelated_errors_do_not_catch_each_other(
        self, error: type[Exception], other: type[Exception]
    ) -> None:
        assert not issubclass(error, other)


class TestCatching:
    @pytest.mark.parametrize("error", ALL_ERRORS)
    def test_caught_as_pydsa_error(self, error: type[Exception]) -> None:
        with pytest.raises(PydsaError, match="boom"):
            raise error("boom")

    def test_category_catches_its_members(self) -> None:
        for member in (KeyNotFoundError, VertexNotFoundError, EdgeNotFoundError):
            with pytest.raises(NotFoundError):
                raise member("boom")

    def test_invalid_value_error_catches_invalid_path_error(self) -> None:
        with pytest.raises(InvalidValueError):
            raise InvalidPathError("boom")


class TestBuiltinCompatibility:
    @pytest.mark.parametrize(("error", "builtin"), BUILTIN_BASES)
    def test_is_also_a_builtin_error(
        self, error: type[Exception], builtin: type[Exception]
    ) -> None:
        assert issubclass(error, builtin)

    @pytest.mark.parametrize(("error", "builtin"), BUILTIN_BASES)
    def test_caught_by_pydsa_error_and_by_builtin(
        self, error: type[Exception], builtin: type[Exception]
    ) -> None:
        for catcher in (PydsaError, builtin):
            with pytest.raises(catcher):
                raise error("boom")


class TestMessages:
    @pytest.mark.parametrize("error", ALL_ERRORS)
    def test_message_is_shown_as_written(self, error: type[Exception]) -> None:
        assert str(error("Something is wrong")) == "Something is wrong"

    @pytest.mark.parametrize("error", ALL_ERRORS)
    @pytest.mark.parametrize("args", [(), ("only",), ("first", "second")])
    def test_str_matches_plain_exception(
        self, error: type[Exception], args: tuple[str, ...]
    ) -> None:
        assert str(error(*args)) == str(Exception(*args))

    @pytest.mark.parametrize("error", ALL_ERRORS)
    def test_args_are_preserved(self, error: type[Exception]) -> None:
        assert error("Something is wrong").args == ("Something is wrong",)

    def test_message_with_quotes_and_newline_is_not_escaped(self) -> None:
        message = 'Key it\'s "x"\nnot found'
        assert str(KeyNotFoundError(message)) == message
