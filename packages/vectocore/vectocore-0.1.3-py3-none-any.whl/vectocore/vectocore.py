import os
import json
import requests


class Vectocore:
    def __init__(self, tenantKey=""):
        self.tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenantKey)

    def test(self, input: str) -> str:
        return "here is {} comes. tenant key : {}!!!!!".format(input, self.tenant_key)

    def test2(self, input: str) -> str:
        return ">>>>>here is {} comes. tenant key : {}!!!!!".format(input, self.tenant_key)
