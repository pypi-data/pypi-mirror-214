import re
import semver

from .exceptions import *

MIN_DESCRIPTION_LENGTH = 20
MAX_DESCRIPTION_LENGTH = 100


def raise_exception_invalid_email(email: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        raise VaderConfigError(f"Email is not a valid email: {email}")


def raise_exception_invalid_description(
    description: str,
    min_length: int = MIN_DESCRIPTION_LENGTH,
    max_length: int = MAX_DESCRIPTION_LENGTH,
):
    if len(description) < min_length:
        raise VaderConfigError(f"Description may not be under {min_length} characters")

    if len(description) > max_length:
        raise VaderConfigError(f"Description may not be over {max_length} characters")


def raise_exception_invalid_version(version):
    if not semver.VersionInfo.is_valid(version):
        raise VaderConfigError(f"Version number is not a valid version: {version}")
