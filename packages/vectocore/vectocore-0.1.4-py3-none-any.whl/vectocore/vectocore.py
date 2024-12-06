import os
import json
import requests
from vectocore.components.common_logs import _logger as logger


class Vectocore:
    def __init__(self, tenantKey=""):
        # 변수 은닉화
        self.__VECTOR_URL = "https://api.vectocore.com/api"
        self.__tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenantKey)
        if self.__tenant_key == "" or self.__tenant_key is None:
            raise ValueError("Tenant key is none")

    def put_index(self, index_name: str, desc=""):
        data = {"command": "put_index", "index_name": index_name, "index_desc": desc}

        logger.info("data : {}".format(data))
        response = requests.post(url=self.__VECTOR_URL, json=data)

        logger.info("response : {}".format(response))

        return response
