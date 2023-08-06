import re
import copy

SPECIAL_CHARACTERS = "[-@!#$%^&*()<>?/\\\|}{~:]"
BLACKLIST_KEYS = ["password", "token", "secret_id", "secret-id", "credential"]
SANITIZE_VALUE = "SANITIZE"


def contains_special_character(
    custom_string: str, special_characters: str = SPECIAL_CHARACTERS
):
    regex = re.compile(special_characters)
    if regex.search(custom_string):
        return True
    return False


def generate_project_name(app_id, boundary_id):
    return f"{app_id}-{boundary_id}"


def generate_namespace_path(parent_namespace, namespace):
    return f"{parent_namespace}/{namespace}".replace("//", "/")


def generate_full_path(namespace_path, parent_path, resource_name):
    return f"{namespace_path}/{parent_path}/{resource_name}".replace("//", "/")


def generate_vault_policy_name(app_id, boundary_id, category, unique_name):
    return f"{app_id}-{boundary_id}-{category}-{unique_name}"


def sanitize_dict(the_dict, whitelist_keys=[], blacklist_keys=[]):
    the_dict = copy.deepcopy(the_dict)
    blacklist_keys = list(set(blacklist_keys + BLACKLIST_KEYS))
    blacklist_keys = list(filter(lambda x: x not in whitelist_keys, blacklist_keys))

    for key, value in the_dict.items():
        if isinstance(value, dict):
            the_dict[key] = sanitize_dict(value, whitelist_keys, blacklist_keys)
        elif key.lower() in blacklist_keys:
            the_dict[key] = SANITIZE_VALUE

    return the_dict
