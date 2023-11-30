from __future__ import annotations

from pathlib import Path


def current_user() -> str:
    """Returns current user name"""
    import os

    try:
        # fails on WSL
        username = os.getlogin()
    except FileNotFoundError:
        # works on WSL
        username = os.environ["USER"]
    return username


def get_user_full_name(username: str) -> str:
    """Returns a user's full name given a username or original value if not found"""
    full_name = username
    with Path("/etc/passwd").open() as f:
        for line in f:
            if line.split(":")[0] == username:
                full_name = line.split(":")[4].strip("/n")
                break
    if full_name:
        return full_name.replace(",,,", "")
    return username
