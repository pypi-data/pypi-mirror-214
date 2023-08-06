import json

from vapi import VAPI

from abc import ABC, abstractmethod


class VaultResource(ABC):
    def _get_vault_resource(self, path):
        return json.loads(VAPI().get(path))

    def _post_vault_resource(self, path, config, expected_status_code=200):
        return json.loads(VAPI().post(path, config))

    def _delete_vault_resource(self, path, expected_status_code=204):
        return json.loads(VAPI().delete(path))

    def _list_vault_resources(self, path):
        return json.loads(VAPI().list(path))
