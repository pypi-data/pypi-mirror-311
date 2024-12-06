import json
from base64 import urlsafe_b64encode
import logging
import random
import string
from typing import Any, TypeVar

T = TypeVar("T")


_LOGGER = logging.getLogger(__name__)


def get_dict_value_or_none(dictionary, key) -> Any:
    if dictionary is None or key not in dictionary:
        return None
    return dictionary[key]


def get_dict_value_or_default(dictionary, key, default: T) -> T:
    if dictionary is None or key not in dictionary:
        return default
    return dictionary[key]


def get_list_value_or_default(list, idx, default: T) -> T:
    try:
        return list[idx]
    except IndexError:
        return default


def pretty_print(json_object):
    print(json.dumps(json_object, indent=4, sort_keys=True))
    print("\n")


def pretty_print_except(json_object, except_keys=[]):
    if json_object is None:
        return

    json_object_copy = json_object.copy()
    for key in except_keys:
        if key in json_object_copy:
            del json_object_copy[key]
    pretty_print(json_object_copy)


def base64_url_encode(data):
    return urlsafe_b64encode(data).rstrip(b"=")


def generate_challenge(length):
    characters = string.ascii_letters + string.digits
    challenge = "".join(random.choice(characters) for _ in range(length))
    return challenge


def get_response_json_or_log_and_raise_exception(response, message: str):
    try:
        return response.json()
    except Exception as e:
        _LOGGER.error(f"{message} {response.status_code} {response.text}")
        raise Exception(f"{message} {response.status_code} {response.text}") from e
