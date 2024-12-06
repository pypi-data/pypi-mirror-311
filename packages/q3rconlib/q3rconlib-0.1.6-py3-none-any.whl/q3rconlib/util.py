import functools
import time

from .error import Q3RconLibLoginError


def timeout(func):
    """Attempts a rcon login until time elapsed is greater than {Q3Rcon}._login_timeout"""

    @functools.wraps(func)
    def wrapper(*args):
        rcon, *_ = args

        err = None
        start = time.time()
        while time.time() < start + rcon._login_timeout:
            try:
                resp = func(*args)
                if not resp:
                    raise TimeoutError("timeout attempting to login")
                elif resp in (
                    "Bad rcon",
                    "Bad rconpassword.",
                    "Invalid password.",
                ):
                    raise Q3RconLibLoginError(code=1)
                elif (
                    resp == "No rcon password set on server or "
                    "password is shorter than 8 characters.\n"
                ):
                    raise Q3RconLibLoginError(code=3)

                err = None
                break
            except (TimeoutError, ConnectionRefusedError, ConnectionResetError) as e:
                err = e
                rcon.logger.error(f"{type(e).__name__}: {e}... retrying login attempt")
                continue

        if err:
            raise Q3RconLibLoginError(code=2)

    return wrapper
