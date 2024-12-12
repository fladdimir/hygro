from functools import wraps
import time


def retry(backoff_s=1, n_tries=1_000_000):
    def retry_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            n = 0
            while True:
                try:
                    n += 1
                    return f(*args, **kwds)
                except RuntimeError as error:
                    if n <= n_tries:
                        print(f"error on attempt {n}: {error}")
                        print(f"retrying in {backoff_s}s")
                        time.sleep(backoff_s)
                    else:
                        raise error

        return wrapper

    return retry_wrapper
