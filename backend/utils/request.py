import logging

import requests
from backend.utils.decorators import retry


@retry
def api_request(base_url, **kwargs):
    try:
        url_variables = ""
        if kwargs:
            for k, v in kwargs.items():
                url_variables += "{}={}&".format(k, v)
        complete_url = "{}?{}".format(base_url, url_variables[:-1]) if url_variables else base_url

        resp = requests.get(complete_url)
        data = resp.json()
        return data
    except Exception as e:
        logging.error("Exception Encountered: {}".format(e))
        return dict()
