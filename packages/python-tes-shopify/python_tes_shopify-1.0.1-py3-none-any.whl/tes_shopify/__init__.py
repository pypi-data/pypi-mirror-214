from tes.api import API


def init_app(code, name, scopes, access_mode, api_version):
    API.set_app_config(
        {
            "shopify_app_code": code,
            "shopify_app_name": name,
            "shopify_scopes": scopes,
            "shopify_access_mode": access_mode,
            "shopify_api_version": api_version,
        }
    )
