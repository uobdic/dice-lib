def current_linux_user() -> str:
    """Returns current user name"""
    import os

    return os.getlogin()
