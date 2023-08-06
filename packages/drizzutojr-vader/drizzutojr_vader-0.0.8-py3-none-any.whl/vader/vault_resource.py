import json

from vapi import VAPI

from abc import ABC, abstractmethod


class VaultResource(ABC):
    def _get_vault_resource(self, path):
        return VAPI().get(path)

    def _post_vault_resource(self, path, config):
        return VAPI().post(path, config)

    def _delete_vault_resource(self, path):
        return VAPI().delete(path)

    def _list_vault_resources(self, path):
        return VAPI().list(path)
