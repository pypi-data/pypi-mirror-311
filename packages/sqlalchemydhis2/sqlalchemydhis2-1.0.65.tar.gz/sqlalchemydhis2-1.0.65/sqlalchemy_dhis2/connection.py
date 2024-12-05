from typing import Any, Optional


def add_authorization(session: Any, username: Optional[str], password: Optional[str], token: Optional[str]):
    if token is not None:
        session.headers.update({"Authorization": f"Bearer {token}"})
    else:
        session.auth = (username, password)