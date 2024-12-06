import requests
import time
import os
import json
import numpy as np
import re
import pandas as pd
from jsonschema import validate
import jsonschema.exceptions
from common.config_utils import get_api_config
# from common.auth import make_authenticated_request
import urllib
import datetime as dt


def export_addin_functions_to_excel(env, client, analysis=True, path=os.getcwd()):
    """
    Exports Excel Add-in functions (either analysis or risk) from an API endpoint to an Excel file.

    This function retrieves the list of Excel Add-in functions (either for "analysis" or "risk") from a specified 
    environment's API. The functions are extracted, transformed into a DataFrame, and exported to an Excel file. 
    The resulting Excel file contains two columns: the function ID and its description.

    Parameters:
    - env (str): The environment in which the API is hosted (e.g., 'prod', 'qa').
    - client (str): The client identifier for the API.
    - analysis (bool): Determines whether to fetch "analysis" functions (True) or "risk" functions (False). Defaults to True.
    - path (str): The directory path where the resulting Excel file will be saved. Defaults to the current working directory.

    Returns:
    - data (dict): The JSON data retrieved from the API, containing all functions and their descriptions.
    """
    config = get_api_config(env, client)
    base_url = config['base_url'].rstrip('/')

    base_url = base_url.replace('/api/v1', '')

    addin_type = "analysis" if analysis else "risk"
    url = f"{base_url}/excel-addin/{addin_type}/functions.json"
    print(f"Request URL: {url}")
    request = urllib.request.urlopen(url)
    data = json.load(request)

    dict_functions = {i['id']: i['description'] for i in data['functions']}

    df_functions = pd.DataFrame(list(dict_functions.items()), columns=['Function', 'Description'])

    date_now = dt.datetime.now().strftime('%Y_%m_%d')
    excel_filename = f'{env}_{addin_type}_addin_functions_{date_now}.xlsx'

    excel_export(df_functions, excel_filename, path)

    print(f"Exported {len(dict_functions)} {addin_type} functions to {os.path.join(path, excel_filename)}")

    return 'Complete'  # data


def chunkIt(seq, num):
    """
    Divides a sequence into approximately equal-sized chunks.

    Parameters:
    - seq: The sequence (list, string, etc.) to be split into chunks.
    - num: The number of chunks to divide the sequence into.

    Returns:
    - A list of sublists, each representing a chunk of the original sequence.
      If the sequence length is not perfectly divisible by the number of chunks, 
      the last few chunks might be slightly larger or smaller than the others.
    
    Example:
    >>> chunkIt([1, 2, 3, 4, 5], 2)
    [[1, 2], [3, 4, 5]]
    """
    avg = len(seq) / float(num)  # Calculate average size of each chunk
    out = []  # List to store the chunks
    last = 0.0  # Track the starting index for each chunk

    # Continue slicing the sequence until all elements are chunked
    while last < len(seq):
        # Slice the sequence from the current position (last) to the calculated end (last + avg)
        out.append(seq[int(last):int(last + avg)])
        last += avg  # Move the starting point for the next chunk

    return out


def retry_request(request_func, retries=3, delay=2, backoff=2, *args, **kwargs):
    """
    Retry an API request in case of failure.
    (Same as the example provided before.)
    """
    attempt = 0
    while attempt < retries:
        try:
            response = request_func(*args, **kwargs)
            if response.status_code == 200:
                return response.json()  # Assuming API returns JSON
        except requests.RequestException as e:
            print(f"Request failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= backoff
            attempt += 1
    return None


def flatten_json(nested_json, delimiter='_'):
    """
    Flatten a nested JSON object into a single level.
    (Same as the example provided before.)
    """
    flat_dict = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + delimiter)
        elif isinstance(x, list):
            for i, item in enumerate(x):
                flatten(item, name + str(i) + delimiter)
        else:
            flat_dict[name[:-1]] = x

    flatten(nested_json)
    return flat_dict


def build_url(base_url, endpoint):
    """
    Build a complete API URL from the base URL and endpoint.
    (Same as the example provided before.)
    """
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


# Function to export a DataFrame to Excel in the current working directory
def excel_export(df, name, path=os.getcwd()):
    """
    Exports a pandas DataFrame to an Excel file in the specified path.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to export.
    - name (str): The name for the output Excel file.
    - path (str): The directory path to save the file. Defaults to the current working directory.
    """
    file_path = os.path.join(path, f'{name}.xlsx')
    with pd.ExcelWriter(file_path, datetime_format='YYYY-MM-DD') as writer:
        df.to_excel(writer)


# Function to check and create directories for standard uploading format
def check_dir(output_directory_name='exp'):
    """
    Ensures that a set of directories exists, creating them if necessary.
    
    Parameters:
    - output_directory_name (str): The base directory for the folder structure.
    
    Returns:
    - str: Confirmation message after completion.
    """
    base_path = os.path.join(os.getcwd(), output_directory_name)

    sub_dirs = ['assumptions', 'fee_structures', 'reference', 'maintenance', 'assemblies', 'leases']

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for sub_dir in sub_dirs:
        full_path = os.path.join(base_path, sub_dir)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    return 'Finished'


# JSON encoder class for handling numpy data types in JSON
class NpEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle numpy data types.
    Converts numpy data types to native Python types for JSON serialization.
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def dump_json(data, filename, path=os.getcwd(), indent=4):
    """
    Dumps JSON data to a file. If the data is a list, it wraps the list into a dictionary 
    with the key "items" before dumping.
    
    Parameters:
    - data (dict or list): The JSON data to be saved. If it's a list, it will be wrapped with {"items": [data]}.
    - filename (str): The name of the file (without extension).
    - path (str): The directory path where the file should be saved. Defaults to the current working directory.
    - indent (int): The indentation level for the JSON output. Default is 4.
    
    Returns:
    - str: Full path of the saved JSON file.
    """
    # Construct the full file path
    file_path = os.path.join(path, f'{filename}.json')

    try:
        # If the data is a list, wrap it in a dictionary under the key "items"
        if isinstance(data, list):
            data = {"items": data}

        # Dump the JSON data to the file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=indent, cls=NpEncoder)
        print(f"JSON data successfully dumped to {file_path}")
    except Exception as e:
        print(f"Error dumping JSON data to file: {e}")

    return file_path


# Function to load JSON data from a file
def load_json(file_path):
    """
    Loads JSON data from a file.

    Parameters:
    - file_path (str): The path of the file to load JSON data from.

    Returns:
    - dict: The loaded JSON data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


# Function to load a JSON schema from a file
def get_schema(schema_file_path):
    """
    Loads a JSON schema from a file.

    Parameters:
    - schema_file_path (str): The path to the JSON schema file.

    Returns:
    - dict: The loaded schema.
    """
    with open(schema_file_path, 'r') as file:
        return json.load(file)


# Function to validate JSON data against a schema
def validate_schema(schema_path, json_data):
    """
    Validates JSON data against a schema.

    Parameters:
    - schema_path (str): The path to the schema.
    - json_data (dict): The JSON data to be validated.

    Returns:
    - tuple: (bool, str) indicating whether the validation passed, and a message.
    """
    schema_id = json_data['$schema']
    full_schema_path = os.path.join(schema_path, schema_id)
    schema = get_schema(full_schema_path)

    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False, f"Given JSON data is invalid: {err}"

    return True, "Given JSON data is valid"


# Function to validate JSON data against a schema and export if valid
def validate_export(schema_path, file_path, json_data):
    """
    Validates JSON data against a schema and exports it to a file if valid.

    Parameters:
    - schema_path (str): The path to the schema.
    - file_path (str): The path to save the validated JSON data.
    - json_data (dict): The JSON data to validate and export.
    """
    is_valid, message = validate_schema(schema_path, json_data)

    if is_valid:
        export_json_cwd(file_path, json_data)
        print(f"Successfully exported {json_data['$schema'].split('.')[0].replace('KBImport', '')} to output file after passing schema validation.")
    else:
        print(f"CRITICAL: JSON validation failed. Error: {message}")


def format_id(s):
    """
    Formats a given input by removing special characters and standardizing it to uppercase with underscores.

    This function takes an input , removes parentheses, and splits on various 
    delimiters including spaces, hyphens, underscores, commas, dots, slashes, and hashes. The resulting 
    segments are joined by underscores, converted to uppercase, and stripped of any leading or trailing underscores.

    Parameters:
    - s: The input value to be formatted, which can be any type convertible to a string.

    Returns:
    - str: The formatted identifier, consisting of uppercase letters and underscores only.

    Example:
    >>> format_id("(hello-world) #123")
    'HELLO_WORLD_123'
    """
    y = str(s)
    y = ''.join(re.split('[()]', y))
    y = '_'.join(re.split('[#/\-_.,\s]+', y)).upper().strip('_')
    return y


def deep_replace(data, target, replacement):
    """
    Recursively replaces all occurrences of a substring within a nested structure.

    This function traverses a given data structure, which can contain nested dictionaries,
    lists, and strings, and replaces all occurrences of substring `a` with substring `b`
    in any string it encounters. For dictionaries, it applies the replacement to each 
    value. For lists, it iterates through each item and performs the replacement as needed.

    Parameters:
    - data (str | dict | list): The data structure to process. Can be a string, dictionary,
      list, or a nested combination thereof.
    - target (str): The substring to be replaced.
    - replacement (str): The replacement substring.

    Returns:
    - str | dict | list: A new data structure with all instances of `a` replaced by `b`
      in any strings found.

    Example:
    replace_deep({"name": "example", "items": ["example1", "test"]}, "example", "sample")
    {'name': 'sample', 'items': ['sample1', 'test']}
    """

    if isinstance(data, str):
        return data.replace(target, replacement)
    elif isinstance(data, dict):
        return {k: deep_replace(v, target, replacement) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_replace(v, target, replacement) for v in data]
    else:
        # nothing to do?
        return data


def filter_list_of_dictionaries_by_list_of_strings(list_of_dicts, include_items=None, exclude_items=None, key_string=None, include_filter_type='ANY', exclude_filter_type='ALL'):
    """
    Filters a list of dictionaries based on inclusion and/or exclusion criteria determined by substrings 
    found in the value of a specified key in each dictionary.

    Parameters:
    ----------
    - include_items (list, optional): 
        A list of substrings to include. If specified, the function includes dictionaries where the value 
        of `key_string` contains the substrings, according to the logic defined by `include_filter_type`.

    - exclude_items (list, optional): 
        A list of substrings to exclude. If specified, the function excludes dictionaries where the value 
        of `key_string` contains the substrings, according to the logic defined by `exclude_filter_type`.

    - key_string (str): 
        The name of the key in each dictionary whose value will be examined for inclusion or exclusion.

    - include_filter_type (str, optional): 
        Determines how `include_items` is applied:
        - 'ANY' (default): Includes dictionaries where any of the substrings in `include_items` are found.
        - 'ALL': Includes dictionaries where all substrings in `include_items` are found.

    - exclude_filter_type (str, optional): 
        Determines how `exclude_items` is applied:
        - 'ANY' (default): Excludes dictionaries where any of the substrings in `exclude_items` are found.
        - 'ALL': Excludes dictionaries where all substrings in `exclude_items` are found.

    - include (bool, optional): 
        If `True` (default), applies the inclusion criteria. If `False`, skips inclusion filtering.

    Returns:
    -------
    - filtered_list (list): 
        A list of dictionaries from the input that satisfy the filtering criteria:
          - Includes dictionaries meeting the `include_items` and `include_filter_type` criteria, if specified.
          - Excludes dictionaries meeting the `exclude_items` and `exclude_filter_type` criteria, if specified.

    """
    # Validate key_string parameter
    if not key_string or key_string not in list_of_dicts[0]:
        raise ValueError("The 'key_string' parameter must be specified and must be in the dictionaries")

    # Start with the original list
    filtered_list = list_of_dicts  # [] if( include_items is None and exclude_items is None) else list_of_dicts
    # Apply inclusion filtering if enabled
    if include_items is not None:
        if include_filter_type.strip().upper() == 'ANY':
            filtered_list = [
                x for x in filtered_list
                if any(item in x.get(key_string, '') for item in include_items)
            ]
        elif include_filter_type.strip().upper() == 'ALL':
            filtered_list = [
                x for x in filtered_list
                if all(item in x.get(key_string, '') for item in include_items)
            ]
        else:
            print(f"Invalid 'include_filter_type': {include_filter_type}. Must be 'ANY' or 'ALL'. Returning unmodified list.")
            return filtered_list

    # Apply exclusion filtering if specified
    if exclude_items is not None:
        if exclude_filter_type.strip().upper() == 'ANY':
            filtered_list = [
                x for x in filtered_list
                if not any(item in x.get(key_string, '') for item in exclude_items)
            ]
        elif exclude_filter_type.strip().upper() == 'ALL':
            filtered_list = [
                x for x in filtered_list
                if not all(item in x.get(key_string, '') for item in exclude_items)
            ]
        else:
            print(f"Invalid 'exclude_filter_type': {exclude_filter_type}. Must be 'ANY' or 'ALL'. Returning unmodified list.")
            return filtered_list

    return filtered_list
