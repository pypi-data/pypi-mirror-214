import logging
import json

import requests
from requests.exceptions import HTTPError
from tes.config import CONFIG

logger = logging.getLogger(__file__)


REQUEST_METHODS = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DEL": requests.delete,
}


class ShopifyClient:
    def __init__(self, shop: str, access_token: str, version: str):
        self.shop = shop
        self.base_url = f"https://{shop}/admin/api/{version}/"
        self.access_token = access_token

    @staticmethod
    def authenticate(shop: str, code: str) -> str:
        url = f"https://{shop}/admin/oauth/access_token"
        payload = {
            "client_id": CONFIG.get("shopify_api_key"),
            "client_secret": CONFIG.get("shopify_secret_key"),
            "code": code,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()["access_token"]
        except HTTPError as ex:
            logging.exception(ex)
            return None

    def authenticated_shopify_call(
        self,
        call_path: str,
        method: str,
        params: dict = None,
        payload: dict = None,
        headers: dict = {},
    ) -> dict:
        url = f"{self.base_url}{call_path}"
        request_func = REQUEST_METHODS[method]
        headers["X-Shopify-Access-Token"] = self.access_token
        try:
            response = request_func(
                url, params=params, json=payload, headers=headers
            )
            logger.debug(url, payload, response.text)
            response.raise_for_status()
            resp_content = json.dumps(response.json(), indent=4)
            logging.debug(
                f"authenticated_shopify_call response:\n{resp_content}"
            )
            return response.json()
        except HTTPError as ex:
            logging.exception(ex)
            return None

    def create_webook(self, address: str, topic: str) -> dict:
        payload = {
            "webhook": {"topic": topic, "address": address, "format": "json"}
        }
        webhook_response = self.authenticated_shopify_call(
            call_path="webhooks.json", method="POST", payload=payload
        )
        if not webhook_response:
            return None
        return webhook_response["webhook"]
