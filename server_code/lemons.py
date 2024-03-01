"""Interacting with LemonSqueezy API."""
import anvil.server
import anvil.http
import anvil.secrets
import json
import hmac
import hashlib

url = "https://api.lemonsqueezy.com/v1/checkouts"


def create_checkout(api_key=None, variants=[], store_id=None,
                    selected_variant=None, user_email=None, test_mode=True,
                    redirect_url=None):
    """Create a custom checkout URL."""
    if not api_key:
        api_key = anvil.secrets.get_secret('lemon_api_key')
    if not variants:
        variants = ['261989', '262003', '262005']
    if not store_id:
        store_id = '71134'
    if not selected_variant:
        selected_variant = '261989'
    if not user_email:
        user_email = 'name@example.com'
    if not redirect_url:
        redirect_url = 'https://dreambyte.ai'
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
                    "enabled_variants": variants,
                    "redirect_url": redirect_url
                },
                "checkout_options": {
                    "button_color": "#2DD272"
                },
                "checkout_data": {
                    # "discount_code": "10PERCENTOFF",
                    "email": user_email
                },
                # "expires_at": "2024-10-30T15:20:06Z",
                "expires_at": None,
                "preview": True,
                "test_mode": test_mode
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": str(store_id)
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": str(selected_variant)
                    }
                }
            }
        }
    }
    # json_data = json.dumps(data)
    # response = anvil.http.request(url=url, method="POST", data=json_data, headers=headers)

    try:
        response = anvil.http.request(url=url, method="POST", data=data, json=True, headers=headers)
    except anvil.http.HttpError as e:
        print(e.content)
        print(f"Error {e.status}")

    print(response)
    # print(response['links']['self'])
    # print(response['data']['id'])  # checkout id
    print(response['data']['attributes']['url'])
    return response['data']['attributes']['url']


def get_customer(api_key=None, customer_id=None):
    """Get customer object and portal link."""
    if not api_key:
        api_key = anvil.secrets.get_secret('lemon_api_key')
    if not customer_id:
        customer_id = '2348771'

    cust_url = f'https://api.lemonsqueezy.com/v1/customers/{customer_id}'
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {api_key}'
    }
    response = anvil.http.request(url=cust_url, method="GET", json=True, headers=headers)
    cust_portal = response['data']['attributes']['urls']['customer_portal']
    print(cust_portal)
    return cust_portal, response


def get_stores(api_key=None, all_info=False):
    """List all stores."""
    if not api_key:
        api_key = anvil.secrets.get_secret('lemon_api_key')
    store_url = "https://api.lemonsqueezy.com/v1/stores"
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {api_key}'
    }
    response = anvil.http.request(url=store_url, method="GET", json=True, headers=headers)
    if 'next' in response['links'].keys():
        raise ValueError('More than 10 stores listed - please email support.')
    store_list = [store for store in response['data']]

    if all_info:
        data = []
        store_counter = 0
        for store in response['data']:
            data.append(store)
            resp_products = anvil.http.request(
                url=store['relationships']['products']['links']['related'],
                method="GET",
                json=True,
                headers=headers
            )

            data[store_counter]['products'] = []
            product_counter = 0
            for product in resp_products['data']:
                data[store_counter]['products'].append(product)
                resp_variants = anvil.http.request(
                    url=product['relationships']['variants']['links']['related'],
                    method="GET",
                    json=True,
                    headers=headers
                )
                data[store_counter]['products'][product_counter]['variants'] = [variant for variant in resp_variants['data']]
                product_counter += 1

            store_counter += 1
        # print(json.dumps(data))
        # print('----------------')
        return data
    return store_list


def get_products(api_key=None, store_id=None):
    """Get list of products in a store."""
    if not api_key:
        api_key = anvil.secrets.get_secret('lemon_api_key')
    if not store_id:
        store_id = '71134'
    products_url = f"https://api.lemonsqueezy.com/v1/products?filter[store_id]={store_id}"
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {api_key}'
    }
    response = anvil.http.request(url=store_url, method="GET", json=True, headers=headers)
    if 'next' in response['links'].keys():
        raise ValueError('More than 10 products listed - please email support.')
    product_list = [prod for prod in response['data']]
    return product_list