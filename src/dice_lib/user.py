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
    """Returns full name of user"""
    full_name = ",,,"
    user_file = "/etc/passwd"
    with open(user_file) as f:
        for line in f:
            if line.startswith(username):
                full_name = line.split(":")[4]
                break
    full_name = "unknown" if full_name == ",,," else full_name
    return full_name
