import base64
from urllib.parse import urlencode
import hashlib
import hmac
import re
from functools import wraps

from tes.api import API, DB
from tes.api.response import APIResponse
from tes.config import CONFIG


class ShopifyUtils:
    @staticmethod
    def create_app_entry():
        DB()["shopify"].insert_one(
            {
                "app_name": API.app_config.get("shopify_app_name"),
                "access_token": "",
                "nonce": "",
                "installed": False,
            }
        )

    @staticmethod
    def app_update(data):
        DB()["shopify"].update_one(
            {"app_name": API.app_config.get("shopify_app_name")},
            {"$set": data},
            upsert=False,
        )

    @staticmethod
    def set_access_token(access_token):
        ShopifyUtils.app_update({"access_token": access_token})

    @staticmethod
    def set_nonce(nonce):
        ShopifyUtils.app_update({"nonce": nonce})

    @staticmethod
    def app_installed():
        ShopifyUtils.app_update({"installed": True})

    @staticmethod
    def app_remove():
        DB()["shopify"].delete_one(
            {"app_name": API.app_config.get("shopify_app_name")}
        )

    @staticmethod
    def get_shopify_app():
        return DB()["shopify"].find_one(
            {"app_name": API.app_config.get("shopify_app_name")}
        )

    @staticmethod
    def set_app_db(shop):
        print("shopname:", ShopifyUtils.get_db_name(shop))
        API.app_db.set_db_profile(ShopifyUtils.get_db_name(shop))

    @staticmethod
    def verify_web_call(func):
        @wraps(func)
        def decorator(*args, **kwargs) -> bool:
            hmac_from_query_string = API.request.args.get("hmac")
            query_dict = API.request.args.get_dict()
            del query_dict["hmac"]

            if "charge_id" in query_dict.keys():
                del query_dict["charge_id"]
                return True
            url_encoded = urlencode(query_dict)
            secret = CONFIG.get("shopify_secret_key").encode("utf-8")
            signature = hmac.new(
                secret, url_encoded.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            is_valid = hmac.compare_digest(hmac_from_query_string, signature)

            if not is_valid:
                return APIResponse.not_authorized(
                    detail="HMAC could not be verified:\n"
                    f"\thmac {hmac_from_query_string}\n"
                    f"\tdata {query_dict}",
                    track=True,
                )

            shop = API.request.args.get("shop")
            if shop and not ShopifyUtils.is_valid_shop(shop):
                return APIResponse.not_authorized(
                    detail=f"Shop name received is invalid: \n\tshop {shop}",
                    track=True,
                )
            ShopifyUtils.set_app_db(shop)
            print("### DB SET!!")
            print("func:", func)
            return func(*args, **kwargs)

        return decorator

    @staticmethod
    def verify_webhook_call(func):
        @wraps(func)
        def decorator(*args, **kwargs) -> bool:
            digest = hmac.new(
                CONFIG.get("shopify_secret_key").encode("utf-8"),
                API.request.data_raw,
                hashlib.sha256,
            ).digest()
            is_valid = hmac.compare_digest(
                base64.b64encode(digest),
                API.request.headers.get("X-Shopify-Hmac-Sha256").encode(
                    "utf-8"
                ),
            )
            if not is_valid:
                return APIResponse.not_authorized(
                    detail=f"HMAC could not be verified: \n"
                    f"\thmac {hmac}\n"
                    f"\tdata {API.request.data}",
                    track=True,
                )
            return func(*args, **kwargs)

        return decorator

    @staticmethod
    def is_valid_shop(shop: str) -> bool:
        # Shopify docs give regex with protocol required,
        # but shop never includes protocol
        shopname_regex = r"[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com[\/]?"
        return re.match(shopname_regex, shop)

    @staticmethod
    def generate_install_redirect_url(shop, scopes, nonce, access_mode):
        scopes_string = ",".join(scopes)
        access_mode_string = ",".join(access_mode)
        redirect_url = f"https://{shop}/admin/oauth/authorize?client_id={CONFIG.get('shopify_api_key')}&scope={scopes_string}&redirect_uri={CONFIG.get('shopify_redirect_url')}&state={nonce}&grant_options[]={access_mode_string}"  # noqa: E501
        return redirect_url

    @staticmethod
    def generate_post_install_redirect_url(shop: str):
        redirect_url = (
            f"https://{shop}/admin/apps/{CONFIG.get('shopify_app_name')}"
        )
        return redirect_url

    @staticmethod
    def get_db_name(shop):
        shop = shop.replace(".myshopify.com", "")
        if shop == "kleine-prints-shop":
            return "kleineprints"
        return shop
