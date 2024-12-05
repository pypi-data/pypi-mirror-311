import json
import requests
import pandas as pd
import ast
from ast import literal_eval
import numpy as np
def extract_alternative_titles(alternative_titles_list):
    if isinstance(alternative_titles_list, list) and alternative_titles_list:
        return " | ".join([alt_title['alternativeTitle'] for alt_title in alternative_titles_list if 'alternativeTitle' in alt_title])
    return ""

def extract_editions(editions_list):
    if isinstance(editions_list, list) and editions_list:
        return " | ".join(editions_list)
    return ""

def tenantlogin(okapi, tenant, username, password):
    myobj = {"username": username, "password": password}
    data = json.dumps(myobj)
    header = {"x-okapi-tenant": tenant}
    x = requests.post(okapi + "/authn/login", data=data, headers=header)
    if "x-okapi-token" in x.headers:
        token = x.headers["x-okapi-token"]
        print("Connected!")
        return token
    else:
        print("Please check the Tenant information")


# return a list that contains 3 df [df_instances,df_holdings,df_item]
def makeDfList (url,header_dict,token,query):
    limit="?limit=2147483646"
    response_instances = requests.get(url+"/instance-storage/instances"+limit+f"&query={query}", headers=header_dict).json()
    df_instances = pd.json_normalize(response_instances, record_path='instances')
    print("df_instances Done!")
    return df_instances


def make_items(url, header_dict, token,query):
    limit = "?limit=2147483646"

    response_instances = requests.get(url + "/item-storage/items" + limit+f"&query={query}", headers=header_dict).json()
    df_items = pd.json_normalize(response_instances, record_path='items')
    print("df_items Done!")
    return df_items


def make_holdings(url, header_dict, token,query):
    limit = "?limit=2147483646"

    response_instances = requests.get(url + "/holdings-storage/holdings" + limit+f"&query={query}", headers=header_dict).json()
    df_holdings = pd.json_normalize(response_instances, record_path='holdingsRecords')
    print("df_holdings Done!")
    return df_holdings

# Function to extract and concatenate 'value's
def series(row):
    if not row:  # Check if the list is empty
        return ''
    return '|'.join(d.get('value', '') for d in row)

def extract_identifier_values(identifier_list):
    if not identifier_list:  # Check if the list is empty
        return ''
    # Extract the 'value' from each dictionary and join them with a pipe
    return '|'.join(d.get('value', '') for d in identifier_list)

def safe_parse(x):
    """
    Safely parse a string representation of a list of dictionaries into an actual list.
    If parsing fails, return an empty list.
    """
    if isinstance(x, str):
        try:
            # Try to parse using ast.literal_eval
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            try:
                # If ast.literal_eval fails, try json.loads
                return json.loads(x)
            except json.JSONDecodeError:
                # If both parsing methods fail, return an empty list
                return []
    elif isinstance(x, list):
        # If it's already a list, return as is
        return x
    else:
        # For any other type, return an empty list
        return []

def extract_contributor_names(contributor_list):
    """
    Extract the 'name' from each dictionary in the contributor_list and concatenate them with a pipe.
    If the list is empty, return NaN.
    """
    if not contributor_list:
        # Return NaN for empty lists
        return pd.NA
    # Extract 'name' from each dictionary, handling missing 'name' keys
    names = [d.get('name', '') for d in contributor_list if 'name' in d]
    # Join the names with a pipe separator
    concatenated_names = '|'.join(names)
    # If concatenated_names is empty, return NaN
    return concatenated_names if concatenated_names else pd.NA

def extract_subject_values(subject_list):
    """
    Extract the 'value' from each dictionary in the subject_list and concatenate them with a pipe.
    If the list is empty, return NaN.
    """
    if not subject_list:
        # Return NaN for empty lists
        return pd.NA
    # Extract 'value' from each dictionary, handling missing 'value' keys
    values = [d.get('value', '') for d in subject_list if 'value' in d]
    # Join the values with a pipe separator
    concatenated_values = '|'.join(values)
    # If concatenated_values is empty, return NaN
    return concatenated_values if concatenated_values else pd.NA

def extract_classification_numbers(classification_list):
    """
    Extract the 'classificationNumber' from each dictionary in the classification_list
    and concatenate them with a pipe ('|'). If the list is empty, return NaN.
    """
    if not classification_list:
        # Return NaN for empty lists
        return pd.NA
    # Extract 'classificationNumber' from each dictionary, handling missing keys
    numbers = [d.get('classificationNumber', '') for d in classification_list if 'classificationNumber' in d]
    # Join the numbers with a pipe separator
    concatenated_numbers = '|'.join(numbers)
    # If concatenated_numbers is empty, return NaN
    return concatenated_numbers if concatenated_numbers else pd.NA


def locations(url, header_dict, token):
    limit = "?limit=2000000"

    response_instances = requests.get(url + "/locations" + limit, headers=header_dict).json()
    df_location = pd.json_normalize(response_instances, record_path='locations')
    print("locations Done!")
    return df_location


def mtypes(url, header_dict, token):
    limit = "?limit=2000000"

    response_instances = requests.get(url + "/material-types" + limit, headers=header_dict).json()
    df_mtypes = pd.json_normalize(response_instances, record_path='mtypes')
    print("mtypes Done!")
    return df_mtypes


def statisticalcode(url, header_dict, token):
    limit = "?limit=2000"

    response_instances = requests.get(url + "/statistical-codes" + limit, headers=header_dict).json()
    df_statcode = pd.json_normalize(response_instances, record_path='statisticalCodes')
    print("statisticalCode Done!")
    return df_statcode


def parse_publication_info_adaptive(publication_data):
    try:
        # Check if the data is already a list (or convert from string if necessary)
        if isinstance(publication_data, str):
            publication_data = literal_eval(publication_data.replace("'", '"'))
        elif not isinstance(publication_data, list):
            raise ValueError("Unsupported data format")

        if publication_data and isinstance(publication_data, list) and len(publication_data) > 0:
            publication_info = publication_data[0]
            publisher = publication_info.get('publisher', None)
            place = publication_info.get('place', None)
            date_of_publication = publication_info.get('dateOfPublication', None)
            return publisher, place, date_of_publication
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"Unexpected error during parsing: {e}")
    return None, None, None


def extract_publication_frequencies(freq_list):
    """
    Extract the publication frequencies from the list and concatenate them with a pipe ('|').
    If the list is empty, return NaN.
    """
    if not freq_list:
        # Return NaN for empty lists
        return np.nan
    # Clean and extract frequency strings, removing any leading/trailing whitespace
    cleaned_frequencies = [freq.strip() for freq in freq_list if isinstance(freq, str)]
    # Join the frequencies with a pipe separator
    concatenated_frequencies = '|'.join(cleaned_frequencies)
    # If concatenated_frequencies is empty, return NaN
    return concatenated_frequencies if concatenated_frequencies else np.nan

def extract_uris(access_list):
    """
    Extract the 'uri' from each dictionary in the access_list
    and concatenate them with a pipe ('|'). If the list is empty, return NaN.
    """
    if not access_list:
        # Return NaN for empty lists
        return np.nan
    # Extract 'uri' from each dictionary, handling missing 'uri' keys
    uris = [access.get('uri', '') for access in access_list if 'uri' in access]
    # Remove any empty strings resulting from missing 'uri' keys
    uris = [uri for uri in uris if uri]
    # Join the URIs with a pipe separator
    concatenated_uris = '|'.join(uris)
    # If concatenated_uris is empty, return NaN
    return concatenated_uris if concatenated_uris else np.nan

def clean_and_concatenate_languages(lang_list):
    """
    Clean each language code by stripping whitespace and concatenate them using a pipe ('|').
    If the list is empty, return NaN.
    """
    if not lang_list:
        # Return NaN for empty lists
        return np.nan
    # Clean each language code by stripping whitespace
    cleaned_langs = [lang.strip() for lang in lang_list if isinstance(lang, str)]
    # Remove any empty strings resulting from stripping
    cleaned_langs = [lang for lang in cleaned_langs if lang]
    if not cleaned_langs:
        return np.nan
    # Concatenate the cleaned language codes with a pipe separator
    concatenated_langs = '|'.join(cleaned_langs)
    return concatenated_langs

def extract_and_concatenate_notes(notes_list):
    """
    Extract the 'note' field from each dictionary in the notes_list and concatenate them with a pipe ('|').
    If the list is empty or no 'note' fields are found, return NaN.
    """
    if not isinstance(notes_list, list) or not notes_list:
        # Return NaN for empty or non-list entries
        return np.nan
    # Extract 'note' from each dictionary, handling missing 'note' keys
    notes = [d.get('note', '').strip() for d in notes_list if 'note' in d and d.get('note')]
    # Remove any empty strings resulting from missing 'note' keys
    notes = [note for note in notes if note]
    if not notes:
        return np.nan
    # Join the notes with a pipe separator
    concatenated_notes = '|'.join(notes)
    return concatenated_notes

def fetch_username(uuid, headers,okapi):
    """
    Fetches the username for a given user UUID using the provided headers.

    Parameters:
    - uuid (str): The user UUID.
    - headers (dict): The authentication headers.

    Returns:
    - str or np.nan: The username if found; otherwise, NaN.
    """
    url = f'{okapi}/users/{uuid}'
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get('username', np.nan)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred for UUID {uuid}: {http_err}')  # Log the error
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred for UUID {uuid}: {conn_err}')  # Log the error
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error for UUID {uuid}: {timeout_err}')  # Log the error
    except requests.exceptions.RequestException as req_err:
        print(f'General error for UUID {uuid}: {req_err}')  # Log the error
    except ValueError as json_err:
        print(f'JSON decoding failed for UUID {uuid}: {json_err}')  # Log the error
    return np.nan


# Define the revised mapping function
def map_uuids_to_names(uuid_entry, mapping_dict, separator='|'):
    """
    Maps a list of UUIDs to their corresponding names.

    Parameters:
    - uuid_entry: list of UUIDs, a single UUID string, or NaN
    - mapping_dict: dictionary mapping UUIDs to names
    - separator: string to separate multiple names

    Returns:
    - Mapped names as a string separated by the separator, or NaN
    """
    # Handle list-like entries first
    if isinstance(uuid_entry, (list, tuple, np.ndarray)):
        if not uuid_entry:
            return np.nan
        # Remove any NaN entries within the list
        cleaned_uuids = [uuid for uuid in uuid_entry if pd.notna(uuid)]
        if not cleaned_uuids:
            return np.nan
        # Map UUIDs to names
        name_list = [mapping_dict.get(uuid, f'Unknown UUID: {uuid}') for uuid in cleaned_uuids]
        if not name_list:
            return np.nan
        return separator.join(name_list)

    # Then handle NaN entries
    if pd.isna(uuid_entry):
        return np.nan

    # Handle string entries that might represent lists
    if isinstance(uuid_entry, str):
        try:
            # Attempt to parse the string to a list
            parsed = ast.literal_eval(uuid_entry)
            if isinstance(parsed, list):
                if not parsed:
                    return np.nan
                # Remove any NaN entries within the parsed list
                cleaned_uuids = [uuid for uuid in parsed if pd.notna(uuid)]
                if not cleaned_uuids:
                    return np.nan
                # Map UUIDs to names
                name_list = [mapping_dict.get(uuid, f'Unknown UUID: {uuid}') for uuid in cleaned_uuids]
                if not name_list:
                    return np.nan
                return separator.join(name_list)
            else:
                # If it's not a list after parsing, treat it as a single UUID
                return mapping_dict.get(uuid_entry, f'Unknown UUID: {uuid_entry}')
        except (ValueError, SyntaxError):
            # If parsing fails, treat the entire string as a single UUID
            return mapping_dict.get(uuid_entry, f'Unknown UUID: {uuid_entry}')

    # Handle other types: assume it's a single UUID
    return mapping_dict.get(uuid_entry, f'Unknown UUID: {uuid_entry}')

# Function to parse string representations of lists
def parse_uuid_entry(entry):
    if isinstance(entry, str):
        try:
            parsed = ast.literal_eval(entry)
            if isinstance(parsed, list):
                return parsed
            else:
                return [parsed]
        except (ValueError, SyntaxError):
            # If parsing fails, treat the entire string as a single UUID
            return [entry]
    elif isinstance(entry, list):
        return entry
    else:
        # For any other type, return as a single-element list
        return [entry]


def make_loans(url, header_dict, token, page_limit=1000):
    loans = []
    page = 0
    while True:
        offset = page * page_limit
        query = f"?limit={page_limit}&offset={offset}"
        response = requests.get(url + "/circulation/loans" + query, headers=header_dict)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
        data = response.json()
        if not data['loans']:  # If no more data, break the loop
            break
        loans.extend(data['loans'])
        page += 1  # Increment to fetch the next page

    df_loans = pd.json_normalize(loans)
    print("df_loans Done!")
    return df_loans


def fetch_loan_type_name(uuid, header_dict,okapi):
    """
    Fetches the loan type name for a given UUID from the loan-types endpoint.

    Parameters:
        uuid (str): The UUID of the loan type.
        header_dict (dict): The headers including authentication token.

    Returns:
        str: The name of the loan type if found, else None.
    """
    url = f'{okapi}/loan-types/{uuid}'
    try:
        response = requests.get(url, headers=header_dict)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        data = response.json()
        return data.get('name')  # Adjust the key based on the actual response structure
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for UUID {uuid}: {http_err}")  # Python 3.6
    except Exception as err:
        print(f"Other error occurred for UUID {uuid}: {err}")  # Python 3.6
    return None