import time
import logging


def retry(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 2
        for i in range(max_retries):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logging.error("Encountered Exception: {}".format(e))
                if i < max_retries - 1:
                    logging.info("Retrying in {} seconds...".format(retry_delay))
                    time.sleep(retry_delay)
        raise Exception("Failed to execute function after {} retries".format(max_retries))

    return wrapper
