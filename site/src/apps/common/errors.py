from fastapi import HTTPException, status

from db.model import Model


def object_not_found(model: Model, status_code=status.HTTP_404_NOT_FOUND):
    return HTTPException(
        status_code=status_code,
        detail=f"{model.__name__} is not found",
    )


def id_not_found(model: Model, ids, status_code=status.HTTP_404_NOT_FOUND):
    return HTTPException(
        status_code=status_code,
        detail=f"{model.__name__} {ids} is not found",
    )


def field_value_must_be_unique(field: str = "{Field name here}"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{field.capitalize()} must be unique",
    )
