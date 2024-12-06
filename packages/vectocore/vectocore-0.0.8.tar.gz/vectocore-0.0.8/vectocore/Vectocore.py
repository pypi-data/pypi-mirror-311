import os
import json
import requests


class Vectocore:
    def __init__(self, tenantKey: str):
        self.tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenantKey)

    def test(self, input: str) -> str:
        return "here is {} comes".format(input)
