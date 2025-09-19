from fastapi import HTTPException, status


def credentials_exception(
    status_code: int = status.HTTP_401_UNAUTHORIZED,
    detail: str = "Could not validate credentials",
):
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
