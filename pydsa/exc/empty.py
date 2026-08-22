"""Exception raised for operations on empty data structures."""

from .base import PydsaError


class EmptyError(PydsaError):
    """Raised when an operation is attempted on an empty data structure.

    Parameters
    ----------
    estimator : object
        The instance on which the operation was attempted. Its class
        name is used to build the error message.
    """

    def __init__(self, estimator: object) -> None:
        """Initialize the error with a message naming the empty structure's type."""
        message = f"{type(estimator).__name__} is empty"
        super().__init__(message)
