from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional
from central.db import get_db, Users
from sqlalchemy.orm import Session

# debug
from exceptions import execute_stored_procedure


Security = HTTPBasic(auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

rows = execute_stored_procedure(
    "fastapi_add_logs",
    ["dev_tester", "CAM laptop", "security.py;", "pwd context and Security var ready"],
)


def hash_password(password: str) -> str:
    """Encodes a plain password into a secure hash."""
    rows = execute_stored_procedure(
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "security.py; in hash pwd",
            "inside hash pwd function",
        ],
    )
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the plain password matches the stored hash."""
    rows = execute_stored_procedure(
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "security.py; in verify pwd",
            "inside verify pwd function",
        ],
    )
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[Optional[HTTPBasicCredentials], Depends(Security)] = None,
):  # -> UUID | None | Any

    # Check HTTP Basic Auth (Username/Password)

    rows = execute_stored_procedure(
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "security.py; in get current user",
            "inside get current user function",
        ],
    )

    if credentials:
        user_in_db = (
            db.query(Users).filter(Users.username == credentials.username).first()
        )

        rows = execute_stored_procedure(
            "fastapi_add_logs",
            [
                "dev_tester",
                "CAM laptop",
                "config.py; in get current user",
                "checking user credentials",
            ],
        )

        if user_in_db and verify_password(credentials.password, user_in_db.password):
            rows = execute_stored_procedure(
                "fastapi_add_logs",
                [
                    "dev_tester",
                    "CAM laptop",
                    "config.py; in get current user",
                    "user authenticated",
                ],
            )
            return "authenticated"
            # return hash_uid(str(user_in_db.uid))  # Return the ID found in DB

    rows = execute_stored_procedure(
        "fastapi_add_logs",
        [
            "dev_tester",
            "CAM laptop",
            "config.py; in get current user",
            "Authentication failed. raising exception",
        ],
    )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Must provide valid UserID header or Username/Password",
    )
