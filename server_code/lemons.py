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
    json_data = json.dumps(data)
    # response = anvil.http.request(url=url, method="POST", data=json_data, headers=headers)

    try:
        response = anvil.http.request(url=url, method="POST", data=data, json=True, headers=headers)
    except anvil.http.HttpError as e:
        print(e.content)
        print(f"Error {e.status}")

    print(response)
    # print(response['links']['self'])
    print(response['data']['id'])  # checkout id
    print(response['data']['attributes']['url'])


@anvil.server.http_endpoint('/lemon_1', methods=['POST'])
def lemon_1():
    # subscription_created
    # subscription_payment_success
    # subscription_updated

    # try:
    signature = anvil.server.request.headers.get('x-signature')

    if not signature:
        return anvil.server.HttpResponse("Missing signature", status=400)

    event = anvil.server.request.headers.get('x-event-name')
    secret = anvil.secrets.get_secret('lemon_signing')
    
    payload = anvil.server.request.body.get_bytes()
    
    # Compute the HMAC digest
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    
    # Compare the computed digest with the provided signature
    if not hmac.compare_digest(digest, signature):
        return anvil.server.HttpResponse("Invalid signature", status=403)  # Return a 403 Forbidden status code if the signature is invalid

    print(payload)
    # Process the request further if the signature is valid
    # For example, you can parse the JSON body and process the data
    # request_data = anvil.server.request.json()
    
    return anvil.server.HttpResponse("Signature verified", status=200)
    # except Exception as e:
        # return anvil.server.HttpResponse(f"Error processing request: {str(e)}", status=500)
    pass