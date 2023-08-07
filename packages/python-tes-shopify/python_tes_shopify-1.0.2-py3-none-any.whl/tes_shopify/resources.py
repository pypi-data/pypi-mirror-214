import uuid
import json
import logging
from tes.api import API
from tes.api.response import APIResponse
from .shopify_utils import ShopifyUtils
from .client import ShopifyClient

from tes.config import CONFIG

logger = logging.Logger(__file__)


# @API.get("/launched")
@ShopifyUtils.verify_web_call
def launched():
    nonce = uuid.uuid4().hex
    if not ShopifyUtils.get_shopify_app():
        print("no shopify APP")
        ShopifyUtils.create_app_entry()

    print("shopify APP set")
    ShopifyUtils.set_nonce(nonce)
    print("shopify nonce set")

    redirect_url = ShopifyUtils.generate_install_redirect_url(
        shop=API.request.args.get("shop"),
        scopes=API.app_config.get("shopify_scopes"),
        nonce=nonce,
        access_mode=API.app_config.get("shopify_access_mode"),
    )
    print("redirect_url:", redirect_url)
    return "{}", 302, "application/json", redirect_url


# @API.get("/installed")
@ShopifyUtils.verify_web_call
def installed():
    shopify_app = ShopifyUtils.get_shopify_app()
    if not shopify_app or shopify_app.get("nonce") != API.request.args.get(
        "state"
    ):
        return APIResponse.not_authorized(detail="invalid 'state' received")
    shop = API.request.args.get("shop")
    access_token = ShopifyClient.authenticate(
        shop=shop, code=API.request.args.get("code")
    )
    ShopifyUtils.set_access_token(access_token)

    shopify_client = ShopifyClient(
        shop, access_token, API.app_config.get("shopify_api_version")
    )
    shopify_client.create_webook(
        address=f"{CONFIG.get('shopify_app_webhhok_url')}/uninstalled",
        topic="app/uninstalled",
    )
    """
    w_url = CONFIG.get('shopify_app_webhhok_url')
    shopify_client.create_webook(
        address=f"{w_url}/gdpr/customers/datarequest",
        topic="customers/data_request")
    shopify_client.create_webook(
        address=f"{w_url}/gdpr/customers/redact",
        topic="customers/redact")
    shopify_client.create_webook(
        address=f"{w_url}/gdpr/shop/redact",
        topic="shop/redact")
    """
    for webhooks in CONFIG.get_list("shopify_webhooks"):
        address = webhooks["address"]
        if "arn:aws" not in address:
            address = (
                f"{CONFIG.get('shopify_app_webhhok_url')}{webhooks['address']}"
            )
        shopify_client.create_webook(address=address, topic=webhooks["topic"])

    redirect_url = ShopifyUtils.generate_post_install_redirect_url(shop=shop)
    ShopifyUtils.app_installed()
    return "{}", 302, "application/json", redirect_url


# @API.post("/webhooks/uninstalled")
@ShopifyUtils.verify_webhook_call
def webhooks_uninstalled():
    webhook_topic = API.request.headers.get("X-Shopify-Topic")
    webhook_payload = API.request.data
    resp_content = json.dumps(webhook_payload, indent=4)
    logging.error(f"webhook call received {webhook_topic}:\n{resp_content}")
    ShopifyUtils.app_remove()
    return "OK"


# @API.post("/webhooks/gdpr/customers/datarequest")
@ShopifyUtils.verify_webhook_call
def webhooks_gdpr_customers_datarequest():
    # https://shopify.dev/tutorials/add-gdpr-webhooks-to-your-app
    # Clear all personal information
    # you may have stored about the specified shop
    return "OK"


# @API.post("/webhooks/gdpr/customers/redact")
@ShopifyUtils.verify_webhook_call
def webhooks_gdpr_customers_redact():
    return "OK"


# @API.post("/webhooks/gdpr/shop/redact")
@ShopifyUtils.verify_webhook_call
def webhooks_gdpr_shop_redact():
    return "OK"
