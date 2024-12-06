import yaml
import os
import re



def get_api_config(env, name):
    """
    Get the API configuration for a specific environment and API name.
    
    Parameters:
    - env (str): The environment (e.g., 'preprod', 'demo').
    - name (str): The specific name of the API within the environment (e.g., 'api-api-preprod-amergin').

    Returns:
    - dict: A dictionary containing 'api_key_id', 'api_secret_key', and 'base_url'.
    """
    try:
        # Open and load the YAML configuration file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_path = os.path.join(base_dir, 'config', 'config.yaml')

        # Open and load the YAML configuration file
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        # Loop through the configurations for the given environment
        for entry in config['environments'].get(env, []):
            if entry['name'] == name:
                # Return the API key, secret, and name as base_url
                return {
                    'api_key_id': entry['api_key_id'],
                    'api_secret_key': entry['api_secret_key'],
                    'base_url': 'https://' + entry['url'] + '/v1'
                }

        # If no matching configuration is found, return None
        print(f"No configuration found for {env} environment with API name {name}.")
        return None

    except FileNotFoundError:
        print("Error: config.yaml file not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
        return None


def extract_paths(file_content):
    """
    Extracts API paths from a TypeScript paths file, including paths with parameters,
    and derives the HTTP method from the key, with special handling for 'list'.

    Parameters:
    - file_content (str): The content of the TypeScript file containing the paths.

    Returns:
    - dict: A dictionary mapping path names to a tuple containing the HTTP method, API path, and additional parameters.
    """
    paths = {}
    # Match the pattern for API paths (e.g., assemblyList: "/external-api/assemblies" or "/external-api/assemblies/:assemblyId")
    matches = re.findall(r'(\w+):\s*"(/[\w/-]+(:\w+)?)"', file_content)

    for match in matches:
        path_name, api_path, _ = match
        
        # Derive the method from the path name
        method, requires_pagination = derive_http_method(path_name)
        
        # Store the derived method, the API path, and pagination info
        paths[path_name] = {
            'method': method,
            'path': api_path,
            'pagination': requires_pagination
        }
    
    return paths


def derive_http_method(path_name):
    """
    Derives the HTTP method from the path name based on common action keywords, 
    and determines if pagination is needed.

    Parameters:
    - path_name (str): The name of the path (e.g., 'create', 'update', 'list', 'info').

    Returns:
    - tuple: (HTTP method as a string, requires_pagination as a bool)
    """
    # Common action keywords mapped to HTTP methods
    action_method_map = {
        'create': 'POST',
        'update': 'PUT',
        'delete': 'DELETE',
        'remove': 'DELETE',
        'get': 'GET',
        'info': 'GET'
    }

    # Default to GET method
    method = 'GET'
    requires_pagination = False

    # Special case for 'list' indicating a paginated GET request
    if 'list' in path_name.lower():
        method = 'GET'
        requires_pagination = True

    # Check for other keywords to determine the method
    for keyword, mapped_method in action_method_map.items():
        if keyword.lower() in path_name.lower():
            method = mapped_method
            break
    
    return method, requires_pagination


def get_ts_files_info(base_dir):
    """
    Searches through the specified directory for paths files, extracts relevant information from them.

    Parameters:
    - base_dir (str): The base directory where the search will start.

    Returns:
    - list: A list of dictionaries containing extracted data from paths files.
    """
    extracted_data = []

    # Traverse the directory to find TypeScript files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("paths.ts"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    paths_info = extract_paths(content)
                    extracted_data.append({
                        'file': file,
                        'type': 'paths',
                        'data': paths_info
                    })
    
    return extracted_data



def extract_urls_from_file(file_path):
    """
    Extract all URLs from the specified api_client.py file.

    Parameters:
    - file_path (str): The path to the api_client.py file.

    Returns:
    - list: A list of all extracted URLs in the form they appear in the file.
    """
    urls = []
    # Define a regex pattern to match URL strings in the format "/external-api/...".
    url_pattern = re.compile(r'url\s*=\s*f?"(/external-api/[^\s"]+)"')

    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire content of the file.
        content = file.read()

        # Find all occurrences of the URL pattern.
        matches = url_pattern.findall(content)

        # Collect and clean the URLs.
        for match in matches:
            urls.append(match)

    return urls

def find_new_apis(extracted_info, existing_urls):
    """
    Identifies APIs from extracted TypeScript paths that are not yet implemented in the Python client.

    Parameters:
    - extracted_info (list): List of dictionaries containing data from paths files.
    - existing_urls (list): List of URLs extracted from the existing Python API client.

    Returns:
    - list: A list of new APIs that need to be created.
    """
    new_apis = []

    # Normalize the existing URLs to match the TypeScript format
    normalized_existing_urls = {url.replace('{',':').replace('}','').rstrip('/') for url in existing_urls}

    # Loop through each extracted TypeScript path
    for file in extracted_info:
        for path_name, path_data in file['data'].items():
            # Normalize the path to ensure consistent comparison
            normalized_path = path_data['path'].rstrip('/')

            # Check if the path exists in the Python client
            if normalized_path not in normalized_existing_urls:
                new_apis.append({
                    'name': path_name,
                    'path': normalized_path,
                    'method': path_data.get('method', 'GET'),
                    'pagination': path_data.get('pagination', False)
                })
    
    return new_apis

def identify_missing_external_apis(base_directory, python_client_path):
    """
    Wrapper function to extract, compare, and identify missing API implementations.

    Parameters:
    - base_directory (str): The base directory where the TypeScript paths files are located.
    - python_client_path (str): The path to the Python client file containing the implemented URLs.

    Returns:
    - list: A list of new APIs that need to be implemented.
    
    Eaxmple:
        base_directory = C:/Users/Sean.Nicholson/GitHub/core2/backend/src/modules/external_api
        python_client_path = ./external/api_client.py
        
    """
    # Extract TypeScript path info
    extracted_info = get_ts_files_info(base_directory)

    # Extract URLs from the existing Python client
    existing_urls = extract_urls_from_file(python_client_path)

    # Find new APIs that are not yet implemented
    new_apis = find_new_apis(extracted_info, existing_urls)

    # Print the new APIs for clarity
    for api in new_apis:
        print(f"API Name: {api['name']}, Method: {api['method']}, Path: {api['path']}, Pagination: {api['pagination']}")
    
    return new_apis