from fastapi import HTTPException, status


def example_error(param):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f""" Параметр ошибки: {param} """,
    )
