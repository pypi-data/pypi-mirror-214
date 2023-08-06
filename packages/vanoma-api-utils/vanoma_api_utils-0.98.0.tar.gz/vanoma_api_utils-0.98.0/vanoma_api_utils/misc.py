import os
import shortuuid  # type: ignore
from typing import Dict
from babel import numbers
from .constants import ERROR_CODE


def resolve_environment() -> str:
    return os.environ.get("ENVIRONMENT", "testing")


def resolve_debug() -> bool:
    return resolve_environment() != "production"


def create_api_error(error_code: ERROR_CODE, error_message: str) -> Dict[str, str]:
    return {"error_code": error_code.value, "error_message": error_message}


def get_shortuuid() -> str:
    return shortuuid.uuid()


def get_file_extension(filename: str) -> str:
    return filename.split(".")[1]


def format_currency(amount: float, currency: str) -> str:
    return numbers.format_currency(amount, currency, "¤ #,###", currency_digits=False)
