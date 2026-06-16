from .base import PydsaError


class EmptyError(PydsaError):
    def __init__(self, estimator: object) -> None:

        message = f"{type(estimator).__name__} is empty"
        super().__init__(message)
