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
