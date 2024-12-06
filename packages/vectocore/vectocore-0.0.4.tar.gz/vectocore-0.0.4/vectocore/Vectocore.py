import os
import json
import requests


def __init__(self, tenant_key: str):
    self.__tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenant_key)


def test(self, input: str) -> str:
    return "here is {} comes. and tenant : {}".format(input, self.__tenant_key)
