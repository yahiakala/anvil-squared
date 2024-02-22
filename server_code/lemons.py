"""Interacting with LemonSqueezy API."""
import anvil.server
import anvil.http
import anvil.secrets
import json

url = "https://api.lemonsqueezy.com/v1/checkouts"


def create_checkout(api_key=None, variants=[], store_id=None, selected_variant=None):
    if not api_key:
        api_key = anvil.secrets.get_secret('lemon_api_key')
    if not variants:
        variants = [261989, 262003, 262005]
    if not store_id:
        store_id = 71134
    if not selected_variant:
        selected_variant = 261989
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        "data": {
            "type": "checkouts",
            "attributes": {
                # "custom_price": 50000,
                "product_options": {
                    "enabled_variants": variants
                },
                "checkout_options": {
                    "button_color": "#2DD272"
                },
                "checkout_data": {
                    # "discount_code": "10PERCENTOFF",
                },
                "expires_at": "2024-10-30T15:20:06Z",
                # "expires_at": None,
                "preview": True,
                "test_mode": True
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": store_id
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": selected_variant
                    }
                }
            }
        }
    }
    json_data = json.dumps(data)
    response = anvil.http.request(url=url, method="POST", data=json_data, headers=headers)

    # try:
    #     response = anvil.http.request(url=url, method="POST", data=data, json=True, headers=headers)
    # except anvil.http.HttpError as e:
    #     print(e)
    #     print(f"Error {e.status}")

    # print(response)
    # print(response.get('content'))