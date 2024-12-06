import os
import json
import requests
import logging
import logging.handlers
import os

logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)


class Vectocore:
    def __init__(self, tenantKey=""):
        # 변수 은닉화
        self.__VECTOR_URL = "https://api.vectocore.com/api"
        self.__tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenantKey)
        if self.__tenant_key == "" or self.__tenant_key is None:
            raise ValueError("Tenant key is none")

    def put_index(self, index_name: str, desc=""):
        headers = {"Content-Type": "application/json", "x-api-key": self.__tenant_key}
        data = {"command": "put_index", "index_name": index_name, "index_desc": desc}

        logger.info("data : {}".format(data))
        response = requests.post(url=self.__VECTOR_URL, headers=headers, json=data)

        logger.info("response : {}".format(response))

        return response
