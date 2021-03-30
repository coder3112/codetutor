from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    pass


credentials_exception = CredentialsException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

jwt_exception = CredentialsException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not find bearer token in header authorization",
    headers={"WWW-Authenticate": "Bearer"},
)

admin_exception = CredentialsException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not admin",
    headers={"WWW-Authenticate": "Bearer"},
)


class CoursesException(HTTPException):
    pass
