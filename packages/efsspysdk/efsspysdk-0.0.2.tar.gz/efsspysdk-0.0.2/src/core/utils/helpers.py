from .errors import APIError, AuthenticationError, InvalidResourceError
import json


# Recieve the base_url and path as arguments and return a formatted URL string.
def format_url(base_url, path):  
    if not base_url.endswith('/'):
        base_url += '/'
    return f"{base_url}{path.lstrip('/')}"


# Check if the API key is defined. TO DO: Check if the API key is valid.
def verify_api_key(api_key):
    if not api_key or not isinstance(api_key, str):
        raise ValueError('API key must be provided')
    
# Do a request to the API and trigger the process response function.
def request(session, method, url, fields=None):
    response = session.request(method, url)
    
    response.raise_for_status()
    
    data = response.json()
    
    processed_data = process_response(data, fields)
    
    json_data = json.dumps(processed_data, indent=4)

    return json_data

# Process the response from the API and return the data in the format specified by the fields argument.
def process_response(data, fields=None):
    if not isinstance(data, dict):  # Se data não for um dict, retorna como está.
        return data
    if 'docs' in data:
        items = data['docs']
    else:
        items = data
    if isinstance(items, list):
        if fields:
            return [{field: doc.get(field, None) for field in fields} for doc in items]
        else:
            return items
    elif isinstance(items, dict):
        if fields:
            return {field: items.get(field, None) for field in fields}
        else:
            return items
    else:
        return data

# Raise specific error for each status code.
def raise_for_status(response):
    if response.status_code == 401:
        raise AuthenticationError('Invalid API key or secret')
    elif response.status_code == 404:
        raise InvalidResourceError(f'The resource at {response.url} does not exist')
    elif not response.status_code == 200:
        raise APIError(f'An error occurred when making the request: {response.content}', response.status_code)