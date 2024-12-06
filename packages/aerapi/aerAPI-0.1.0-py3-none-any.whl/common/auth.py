import requests
import logging
import common.utils as utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_auth_headers(api_key_id, api_secret_key):
    """
    Create the headers needed for authentication with API keys.

    Parameters:
    - api_key_id (str): The API key ID from the config file
    - api_secret_key (str): The API secret key from the config file

    Returns:
    - dict: Headers containing the API key ID and secret key
    """
    headers = {
        'Api-Key-Id': api_key_id,
        'Api-Secret-Key': api_secret_key,
        'Content-Type': 'application/json'
    }
    return headers


def check_authentication_status(response):
    """
    Check if the API response indicates authentication failure.

    Parameters:
    - response (requests.Response): The response from an API request

    Returns:
    - bool: True if authentication failed, False otherwise
    """
    if response.status_code == 401:
        # Authentication failed
        print("Authentication failed. Please check your API keys.")
        return False
    return True


def make_authenticated_request(config, url, method='GET', params=None, data=None, debug=False, multiSend=False, sendSize=100, timeout=30):
    """
    Make an authenticated request to a given API, with optional support for sending requests in chunks.
    """
    base_url = config['base_url']
    api_key_id = config['api_key_id']
    api_secret_key = config['api_secret_key']

    # print(base_url)
    # print(api_key_id)
    # print(api_secret_key)

    full_url = f"{base_url.rstrip('/')}{url}"
    if debug:
        logger.info(f"Request URL: {full_url}")

    headers = get_auth_headers(api_key_id, api_secret_key)
    responses = []

    # Multi-send logic
    if multiSend and data and isinstance(data, dict) and 'items' in data:
        items = data['items']
        chunks = utils.chunkIt(items, max(1, len(items) // sendSize))

        for chunk in chunks:
            chunked_data = {"items": chunk}
            try:
                response = _send_request(method, full_url, headers, chunked_data, params, timeout, debug=debug)
                if response:
                    responses.append(response)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error during chunked request: {e}")
                return None

        return responses

    # Single request logic
    try:
        return _send_request(method, full_url, headers, data, params, timeout, debug=debug)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during request: {e}")
        return None


def _send_request(method, url, headers, data, params, timeout, debug):
    if method == 'GET':
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data, timeout=timeout)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers, params=params, timeout=timeout)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    # Check if authentication or other errors occurred
    if not check_authentication_status(response):
        return None

    # Log the status code for each request
    if debug:
        logger.info(f"Response Status Code: {response.status_code}")

    # Return JSON response if content exists, otherwise return an empty dict
    return response.json() if response.content else {}
