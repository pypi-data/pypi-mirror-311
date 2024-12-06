from common.config_utils import get_api_config
from common.auth import make_authenticated_request


def get_aircraft_details(env, client, aircraftId, debug=False):
    """
    GET: Retrieve details for a specific aircraft by its aircraft ID.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - aircraftId (str): The unique ID of the aircraft to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The aircraft details in JSON format, including specifications, configurations, and other relevant metadata.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft/{aircraftId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_all_assemblies_for_aircraft(env, client, aircraftId=None, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all assemblies, with optional filtering by aircraft ID, and pagination.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - aircraftId (str, optional): The ID of the aircraft to filter assemblies.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of all assemblies in JSON format, filtered by aircraft ID if provided.
    """
    config = get_api_config(env, client)
    url = "/external-api/assemblies"

    # Adding query parameters for aircraftId, limit, and offset if provided
    params = {}
    if aircraftId:
        params['aircraftId'] = aircraftId
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_assembly_details(env, client, assemblyId, debug=False):
    """
    GET: Retrieve detailed information for a specific assembly by its assembly ID.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - assemblyId (str): The unique ID of the assembly to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The assembly details in JSON format, including metadata like assembly configuration, parts, and other relevant information.
    """
    config = get_api_config(env, client)
    url = f"/external-api/assemblies/{assemblyId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def search_aircraft(env, client, search_params=None, limit=None, offset=None, order_by=None, order=None, debug=False):
    """
    GET: Search for aircraft based on certain criteria with optional pagination and sorting.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - search_params (dict, optional): A dictionary of search parameters (e.g., model, year, manufacturer). Default is None.
    - limit (int, optional): The number of results to return per page. Default is None.
    - offset (int, optional): The starting point for pagination. Default is None.
    - order_by (str, optional): The field by which to sort the results (e.g., 'msn', 'registration', 'operator'). Default is None.
    - order (str, optional): The order of sorting, either 'ASC' or 'DESC'. Default is None.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The search results, including aircraft that match the given criteria.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft/search"

    # Construct query parameters
    params = search_params or {}

    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if order_by:
        params['orderBy'] = order_by
    if order:
        if order.upper() not in ['ASC', 'DESC']:
            raise ValueError("Invalid order value. Must be 'ASC' or 'DESC'.")
        params['order'] = order.upper()

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_analysis_contexts_for_aircraft(env, client, aircraftId, limit=None, offset=None, debug=False):
    """
    GET: Retrieve all available analysis contexts for a specific aircraft with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftId (str): The unique ID of the aircraft to retrieve analysis contexts for.
    - limit (int, optional): The number of results to return per page. Default is None.
    - offset (int, optional): The starting point for pagination. Default is None.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of available analysis contexts for the aircraft in JSON format,
            each containing information about performance, maintenance, or other analysis contexts.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft/{aircraftId}/analysis-contexts"

    # Construct query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_base_analysis_context_for_aircraft(env, client, aircraftId, debug=False):
    """
    GET: Retrieve the base analysis context for a specific aircraft.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftId (str): The unique ID of the aircraft to retrieve the base analysis context for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The base analysis context in JSON format, including core performance and operational metrics.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft/{aircraftId}/analysis-contexts/base"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_all_portfolios(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all portfolios with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of portfolios in JSON format, including portfolio details like names, IDs, and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/portfolios"

    # Construct query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_portfolio_details(env, client, portfolioId, debug=False):
    """
    GET: Retrieve detailed information for a specific portfolio by its portfolio ID.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - portfolioId (str): The unique ID of the portfolio to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The portfolio details in JSON format, including information such as the assets within the portfolio, performance data, and other relevant details.
    """
    config = get_api_config(env, client)
    url = f"/external-api/portfolio/{portfolioId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_cashflows(env, client, analysis_contextId, debug=False):
    """
    GET: Retrieve cashflow data for a specific analysis context.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - analysis_contextId (str): The unique ID of the analysis context for which to retrieve cashflows.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The cashflow data in JSON format, including detailed financial metrics, timelines, and other relevant data.
    """
    config = get_api_config(env, client)
    url = f"/external-api/calculation/{analysis_contextId}/cashflows"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_maintenance_summary(env, client, analysis_contextId, debug=False):
    """
    GET: Retrieve maintenance summary data for a specific analysis context.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - analysis_contextId (str): The unique ID of the analysis context for which to retrieve the maintenance summary.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The maintenance summary data in JSON format, including maintenance schedules, costs, and other relevant details.
    """
    config = get_api_config(env, client)
    url = f"/external-api/calculation/{analysis_contextId}/maintenance-summary"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_all_companies(env, client, limit=None, offset=None, filter=None, debug=False):
    """
    GET: Retrieve a list of all companies with optional pagination and filtering.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - filter (str, optional): A filter string based on company roles.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of companies in JSON format, including company details like names, IDs, and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/companies"

    # Construct query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if filter is not None:
        params['filter'] = filter

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_company_details(env, client, companyId, debug=False):
    """
    GET: Retrieve detailed information for a specific company by its company ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - companyId (str): The unique ID of the company to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The company details in JSON format, including name, address, industry, and other relevant information.
    """
    config = get_api_config(env, client)
    url = f"/external-api/companies/{companyId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_company(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new company.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): A dictionary containing the new company details (e.g., name, address, industry).
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created company details in JSON format, including its unique ID and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/companies"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_company(env, client, companyId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing company's details.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - companyId (str): The unique ID of the company to be updated.
    - data (dict): A dictionary containing the updated company details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated company details in JSON format, including the updated metadata.
    """
    config = get_api_config(env, client)
    url = f"/external-api/companies/{companyId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_company(env, client, companyId, debug=False):
    """
    DELETE: Delete a specific company by its company ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - companyId (str): The unique ID of the company to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the delete operation in JSON format, or an error message if the deletion failed.
    """
    config = get_api_config(env, client)
    url = f"/external-api/companies/{companyId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_all_countries(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all countries with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of countries in JSON format, including country details like name, code, and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/countries"

    # Construct query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_country_details(env, client, countryId, debug=False):
    """
    GET: Retrieve detailed information for a specific country by its country ID.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - countryId (str): The unique ID of the country for which details are to be retrieved.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing detailed information about the country,
            such as the country name, country code, geographic information, and other attributes.
    """
    config = get_api_config(env, client)
    url = f"/external-api/countries/{countryId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_country(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new country record in the system.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - data (dict): A dictionary containing the new country details such as country name, country code, and other relevant attributes.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing the newly created country's details, including the unique country ID and other metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/countries"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_country(env, client, countryId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing country's details.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - countryId (str): The unique ID of the country to update.
    - data (dict): A dictionary containing the updated country details, such as updated country name, country code, and other attributes.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing the updated country's details.
    """
    config = get_api_config(env, client)
    url = f"/external-api/countries/{countryId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_country(env, client, countryId, debug=False):
    """
    DELETE: Delete a specific country by its country ID.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - countryId (str): The unique ID of the country to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response confirming the deletion or providing error information if the operation fails.
    """
    config = get_api_config(env, client)
    url = f"/external-api/countries/{countryId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_lease_list(env, client, assemblyId, debug=False):
    """
    GET: Retrieve a list of leases for a specific assembly.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - assemblyId (str): The unique ID of the assembly for which to retrieve the list of leases.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing a list of leases for the given assembly, including lease details like start date, end date, and lessee information.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leases/assembly/{assemblyId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_lease_details(env, client, leaseId, debug=False):
    """
    GET: Retrieve detailed information for a specific lease by its lease ID.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - leaseId (str): The unique ID of the lease to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing details about the lease, such as lease start and end dates, lessee information, financial terms, and maintenance agreements.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leases/{leaseId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_contracted_lease(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new contracted lease in the system.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - data (dict): A dictionary containing the details of the new contracted lease, such as start date, end date, terms, and lessee details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing the newly created contracted lease details, including the unique lease ID and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/leases/contracted"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def create_structuring_lease(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new structuring lease in the system.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - data (dict): A dictionary containing the details of the new structuring lease, such as terms and structuring specifics.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing the newly created structuring lease details, including the unique lease ID and metadata.
    """
    config = get_api_config(env, client)
    url = "/external-api/leases/structuring"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_lease(env, client, leaseId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing lease by its lease ID.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - leaseId (str): The unique ID of the lease to update.
    - data (dict): A dictionary containing the updated lease details, such as updated terms, lessee information, and financial agreements.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response containing the updated lease details.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leases/{leaseId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_lease(env, client, leaseId, debug=False):
    """
    DELETE: Delete a specific lease by its lease ID.

    Parameters:
    - env (str): The environment in which the API is hosted.
    - client (str): The specific client identifier.
    - leaseId (str): The unique ID of the lease to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response confirming the deletion or providing error information if the operation fails.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leases/{leaseId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_engine_snapshot_info(env, client, engineSnapshotId, debug=False):
    """
    GET: Retrieve detailed information for a specific engine snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineSnapshotId (str): The unique ID of the engine snapshot to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The engine snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-snapshots/{engineSnapshotId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_engine_snapshot_list(env, client, engineId=None, debug=False):
    """
    GET: Retrieve a list of all engine snapshots.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineId (str): Optional. If included, only snapshots related to that engine Id are returned.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of engine snapshots in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/engine-snapshots"
    if engineId:
        url = url + f"?engineId={engineId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_engine_snapshot(env, client, engineId, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new engine snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineId (str): The unique ID of the engine for which the snapshot is being created.
    - data (dict): A dictionary containing the engine snapshot details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created engine snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-snapshots/{engineId}"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_engine_snapshot(env, client, engineSnapshotId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing engine snapshot by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineSnapshotId (str): The unique ID of the engine snapshot to update.
    - data (dict): A dictionary containing the updated engine snapshot details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated engine snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-snapshots/{engineSnapshotId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_engine_snapshot(env, client, engineSnapshotId, debug=False):
    """
    DELETE: Delete a specific engine snapshot by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineSnapshotId (str): The unique ID of the engine snapshot to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response confirming the deletion.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-snapshots/{engineSnapshotId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_lease_snapshot_list(env, client, leaseId, debug=False):
    """
    GET: Retrieve a list of lease snapshots for a specific lease.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - leaseId (str): The unique ID of the lease to retrieve snapshots for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of lease snapshots for the given lease in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leaseSnapshots/lease/{leaseId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_lease_snapshot_details(env, client, leaseSnapshotId, debug=False):
    """
    GET: Retrieve detailed information for a specific lease snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - leaseSnapshotId (str): The unique ID of the lease snapshot to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The lease snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leaseSnapshots/{leaseSnapshotId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_lease_snapshot(env, client, leaseId, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new lease snapshot for a specific lease.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - leaseId (str): The unique ID of the lease for which the snapshot is being created.
    - data (dict): A dictionary containing the lease snapshot details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created lease snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leaseSnapshots/{leaseId}"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_lease_snapshot(env, client, leaseSnapshotId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing lease snapshot by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - leaseSnapshotId (str): The unique ID of the lease snapshot to update.
    - data (dict): A dictionary containing the updated lease snapshot details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated lease snapshot details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leaseSnapshots/{leaseSnapshotId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_lease_snapshot(env, client, leaseSnapshotId, debug=False):
    """
    DELETE: Delete a specific lease snapshot by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - leaseSnapshotId (str): The unique ID of the lease snapshot to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A JSON response confirming the deletion.
    """
    config = get_api_config(env, client)
    url = f"/external-api/leaseSnapshots/{leaseSnapshotId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def add_aircraft_to_portfolio(env, client, portfolioId, aircraftId, debug=False):
    """
    POST: Add an aircraft to a specific portfolio.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - portfolioId (str): The unique ID of the portfolio to add the aircraft to.
    - aircraftId (str): The unique ID of the aircraft to be added to the portfolio.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the operation in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/portfolios/addAircraftToPortfolio/{portfolioId}/{aircraftId}"

    return make_authenticated_request(config, url, method='POST', debug=debug)


def remove_aircraft_from_portfolio(env, client, portfolioId, aircraftId, debug=False):
    """
    DELETE: Remove an aircraft from a specific portfolio.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - portfolioId (str): The unique ID of the portfolio from which the aircraft is to be removed.
    - aircraftId (str): The unique ID of the aircraft to be removed from the portfolio.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the operation in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/portfolios/removeAircraftFromPortfolio/{portfolioId}/{aircraftId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_sovereign_ratings(env, client, countryId, debug=False):
    """
    GET: Retrieve all sovereign ratings for a specific country.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - countryId (str): The unique ID of the country for which to retrieve sovereign ratings.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of sovereign ratings in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/countries/{countryId}/sovereign-ratings"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_one_sovereign_rating(env, client, sovereignRatingId, debug=False):
    """
    GET: Retrieve a specific sovereign rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - sovereignRatingId (str): The unique ID of the sovereign rating to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The sovereign rating details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/sovereign-ratings/{sovereignRatingId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_sovereign_rating(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new sovereign rating.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): A dictionary containing the details of the new sovereign rating.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created sovereign rating details in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/sovereign-ratings"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_sovereign_rating(env, client, sovereignRatingId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing sovereign rating.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - sovereignRatingId (str): The unique ID of the sovereign rating to update.
    - data (dict): A dictionary containing the updated sovereign rating details.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated sovereign rating details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/sovereign-ratings/{sovereignRatingId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_sovereign_rating(env, client, sovereignRatingId, debug=False):
    """
    DELETE: Delete a specific sovereign rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - sovereignRatingId (str): The unique ID of the sovereign rating to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the deletion in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/sovereign-ratings/{sovereignRatingId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_aircraft_part_maintenance_policy_type_info(env, client, aircraftPartMaintenancePolicyTypeId, debug=False):
    """
    GET: Retrieve detailed information for a specific aircraft part maintenance policy type.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartMaintenancePolicyTypeId (str): The unique ID of the aircraft part maintenance policy type.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The detailed information about the aircraft part maintenance policy type in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-maintenance-policy-types/{aircraftPartMaintenancePolicyTypeId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_all_aircraft_part_maintenance_policy_types(env, client, limit=None, offset=None, aircraftPartTypeId=None, debug=False):
    """
    GET: Retrieve a list of all aircraft part maintenance policy types with optional pagination and filtering by aircraft part type.

    Parameters:
    - env (str): The environment where the external API is hosted (e.g., 'production').
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - aircraftPartTypeId (str, optional): The ID of the aircraft part type to filter maintenance policies.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of maintenance policy types in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-part-maintenance-policy-types"

    # Construct query parameters
    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset
    if aircraftPartTypeId:
        params['aircraftPartTypeId'] = aircraftPartTypeId

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_aircraft_part_maintenance_policy_type(env, client, aircraftPartTypeId, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new aircraft part maintenance policy type for a specific aircraft part type.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartTypeId (str): The unique ID of the aircraft part type.
    - data (dict): The details of the new aircraft part maintenance policy type.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created aircraft part maintenance policy type in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-maintenance-policy-types/{aircraftPartTypeId}"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_aircraft_part_maintenance_policy_type(env, client, aircraftPartMaintenancePolicyTypeId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing aircraft part maintenance policy type.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartMaintenancePolicyTypeId (str): The unique ID of the aircraft part maintenance policy type.
    - data (dict): The updated details of the aircraft part maintenance policy type.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated aircraft part maintenance policy type in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-maintenance-policy-types/{aircraftPartMaintenancePolicyTypeId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_aircraft_part_maintenance_policy_type(env, client, aircraftPartMaintenancePolicyTypeId, debug=False):
    """
    DELETE: Delete a specific aircraft part maintenance policy type.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartMaintenancePolicyTypeId (str): The unique ID of the aircraft part maintenance policy type to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the deletion in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-maintenance-policy-types/{aircraftPartMaintenancePolicyTypeId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_aircraft_part_snapshot_info(env, client, aircraftPartSnapshotId, debug=False):
    """
    GET: Retrieve detailed information for a specific aircraft part snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartSnapshotId (str): The unique ID of the aircraft part snapshot.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The detailed information about the aircraft part snapshot in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-snapshots/{aircraftPartSnapshotId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_aircraft_part_snapshot_list(env, client, aircraftPartId=None, debug=False):
    """
    GET: Retrieve a list of all aircraft part snapshots.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartId (str): Optional. If included, only snapshots related to that part Id are returned.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of all available aircraft part snapshots in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-part-snapshots"
    if aircraftPartId:
        url = url + f"?aircraftPartId={aircraftPartId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_aircraft_part_snapshot(env, client, aircraftPartId, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new aircraft part snapshot for a specific aircraft part.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartId (str): The unique ID of the aircraft part.
    - data (dict): The details of the new aircraft part snapshot.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created aircraft part snapshot in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-snapshots/{aircraftPartId}"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_aircraft_part_snapshot(env, client, aircraftPartSnapshotId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing aircraft part snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartSnapshotId (str): The unique ID of the aircraft part snapshot.
    - data (dict): The updated details of the aircraft part snapshot.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated aircraft part snapshot in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-snapshots/{aircraftPartSnapshotId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_aircraft_part_snapshot(env, client, aircraftPartSnapshotId, debug=False):
    """
    DELETE: Delete a specific aircraft part snapshot.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartSnapshotId (str): The unique ID of the aircraft part snapshot to be deleted.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the deletion in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-snapshots/{aircraftPartSnapshotId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_aircraft_appraisal_info(env, client, aircraftAppraisalId, debug=False):
    """
    GET: Retrieve detailed information for a specific aircraft appraisal by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftAppraisalId (str): The unique ID of the aircraft appraisal to retrieve.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: Detailed information about the aircraft appraisal in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-appraisals/{aircraftAppraisalId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_aircraft_appraisal_list(env, client, limit=None, offset=None, aircraftId=None, debug=False):
    """
    GET: Retrieve a list of all aircraft appraisals, with optional pagination and filtering by aircraft ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - aircraftId (str, optional): Filter results by aircraft ID.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of aircraft appraisals in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-appraisals"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset
    if aircraftId:
        params['aircraftId'] = aircraftId

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_aircraft_appraisal(env, client, aircraftId, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new aircraft appraisal for a specific aircraft.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftId (str): The unique ID of the aircraft to appraise.
    - data (dict): The details of the new aircraft appraisal.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created aircraft appraisal in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-appraisals/{aircraftId}"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_aircraft_appraisal(env, client, aircraftAppraisalId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing aircraft appraisal.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftAppraisalId (str): The unique ID of the aircraft appraisal.
    - data (dict): The updated details of the aircraft appraisal.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated aircraft appraisal in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-appraisals/{aircraftAppraisalId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_aircraft_appraisal(env, client, aircraftAppraisalId, debug=False):
    """
    DELETE: Delete a specific aircraft appraisal by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftAppraisalId (str): The unique ID of the aircraft appraisal to be deleted.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the deletion in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-appraisals/{aircraftAppraisalId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_appraiser_info(env, client, appraiserId, debug=False):
    """
    GET: Retrieve detailed information for a specific appraiser by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - appraiserId (str): The unique ID of the appraiser to retrieve.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: Detailed information about the appraiser in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/appraisers/{appraiserId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_appraiser_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all appraisers, with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of appraisers in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/appraisers"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_appraiser(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new appraiser.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): The details of the new appraiser.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The newly created appraiser in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/appraisers"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_appraiser(env, client, appraiserId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing appraiser by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - appraiserId (str): The unique ID of the appraiser to update.
    - data (dict): The updated details of the appraiser.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated appraiser details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/appraisers/{appraiserId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_appraiser(env, client, appraiserId, debug=False):
    """
    DELETE: Delete a specific appraiser by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - appraiserId (str): The unique ID of the appraiser to be deleted.
    - debug (bool): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the deletion in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/appraisers/{appraiserId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_aircraft_model_info(env, client, aircraftModelId, debug=False):
    """
    GET: Retrieve details for a specific aircraft model by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftModelId (str): The unique ID of the aircraft model to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The aircraft model details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-models/{aircraftModelId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_aircraft_model_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of aircraft models with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of aircraft models in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-models"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_aircraft_model(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new aircraft model.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): A dictionary containing the details of the aircraft model.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The details of the newly created aircraft model in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-models"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_aircraft_model(env, client, aircraftModelId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing aircraft model by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftModelId (str): The unique ID of the aircraft model to update.
    - data (dict): A dictionary containing the updated details of the aircraft model.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated aircraft model details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-models/{aircraftModelId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def get_engine_model_info(env, client, engineModelId, debug=False):
    """
    GET: Retrieve details for a specific engine model by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineModelId (str): The unique ID of the engine model to retrieve details for.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The engine model details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-models/{engineModelId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_engine_model_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of engine models with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of engine models in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/engine-models"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_engine_model(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new engine model.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): A dictionary containing the details of the engine model.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The details of the newly created engine model in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/engine-models"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_engine_model(env, client, engineModelId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing engine model by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - engineModelId (str): The unique ID of the engine model to update.
    - data (dict): A dictionary containing the updated details of the engine model.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The updated engine model details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/engine-models/{engineModelId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def get_income_statement_list_per_company(env, client, companyId, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of income statements with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - companyId (str): Company UUID for which income statements will be returned.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of income statements in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/financial-statements/income-statements"

    params = {
        "companyId": companyId
    }
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_income_statement_info(env, client, incomeStatementId, debug=False):
    """
    GET: Retrieve details for a specific income statement by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - incomeStatementId (str): The unique ID of the income statement to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The income statement details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/financial-statements/income-statements/{incomeStatementId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def delete_income_statement(env, client, incomeStatementId, debug=False):
    """
    DELETE: Delete a specific income statement by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - incomeStatementId (str): The unique ID of the income statement to delete.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the deletion.
    """
    config = get_api_config(env, client)
    url = f"/external-api/financial-statements/income-statements/{incomeStatementId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_balance_sheet_list_per_company(env, client, companyId, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of balance sheets with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - companyId (str): Company UUID for which balance sheets will be returned.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of balance sheets in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/financial-statements/balance-sheets"

    params = {
        "companyId": companyId
    }

    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_balance_sheet_info(env, client, balanceSheetId, debug=False):
    """
    GET: Retrieve details for a specific balance sheet by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - balanceSheetId (str): The unique ID of the balance sheet to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The balance sheet details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/financial-statements/balance-sheets/{balanceSheetId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def delete_balance_sheet(env, client, balanceSheetId, debug=False):
    """
    DELETE: Delete a specific balance sheet by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - balanceSheetId (str): The unique ID of the balance sheet to delete.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the deletion.
    """
    config = get_api_config(env, client)
    url = f"/external-api/financial-statements/balance-sheets/{balanceSheetId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_user_info(env, client, userId, debug=False):
    """
    GET: Retrieve detailed information for a specific user by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - userId (str): The unique ID of the user to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Detailed information about the user in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/users/{userId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_user_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all users with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of users in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/users"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_role_info(env, client, roleId, debug=False):
    """
    GET: Retrieve detailed information for a specific role by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - roleId (str): The unique ID of the role to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Detailed information about the role in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/roles/{roleId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_role_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all roles with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of roles in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/roles"

    params = {}
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_aircraft_part_type_info(env, client, aircraftPartTypeId, debug=False):
    """
    GET: Retrieve information for a specific aircraft part type by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartTypeId (str): The unique ID of the aircraft part type to retrieve.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: The aircraft part type details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-types/{aircraftPartTypeId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def get_aircraft_part_types_list(env, client, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all aircraft part types with optional pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: A paginated list of aircraft part types in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-part-types"

    params = {}
    if limit is not None:
        params['limit'] = limit
    if offset is not None:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def create_aircraft_part_type(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new aircraft part type.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): Data for the new aircraft part type.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the creation in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/aircraft-part-types"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_aircraft_part_type(env, client, aircraftPartTypeId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing aircraft part type by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - aircraftPartTypeId (str): The unique ID of the aircraft part type to update.
    - data (dict): Updated data for the aircraft part type.
    - debug (bool): Optional. If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the update in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/aircraft-part-types/{aircraftPartTypeId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def get_credit_model_list(env, client, limit=None, offset=None, name=None, debug=False):
    """
    Retrieve a list of credit models with optional pagination and filtering by name.

    Args:
        env (str): The environment where the external API is hosted.
        client (str): The client identifier for the API.
        limit (int, optional): The number of results to return per page.
        offset (int, optional): The starting point for pagination.
        name (str, optional): Name filter for credit models.
        debug (bool): Optional flag to enable debugging information.

    Returns:
        dict: A paginated list of credit models in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/risk/credit-models"
    params = {k: v for k, v in {'limit': limit, 'offset': offset, 'name': name}.items() if v is not None}

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_credit_model_info(env, client, creditModelId, debug=False):
    """
    Retrieve details for a specific credit model by its ID.

    Args:
        env (str): The environment where the external API is hosted.
        client (str): The client identifier for the API.
        creditModelId (str): The unique ID of the credit model to retrieve.
        debug (bool): Optional flag to enable debugging information.

    Returns:
        dict: Details of the specified credit model in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/risk/credit-models/{creditModelId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def generate_company_rating(env, client, companyId, creditModelId, balanceSheetId=None, incomeStatementId=None, debug=False):
    """
    Generate a company rating for a specific company by its ID, using optional financial statement references.

    Args:
        env (str): The environment where the external API is hosted.
        client (str): The client identifier for the API.
        companyId (str): The unique ID of the company to generate the rating for.
        creditModelId (str): The ID of the credit model to use.
        balanceSheetId (str, optional): The ID of the balance sheet to use in rating generation.
        incomeStatementId (str, optional): The ID of the income statement to use in rating generation.
        debug (bool): Optional flag to enable debugging information.

    Returns:
        dict: The generated company rating in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/risk/company-ratings/generate/{companyId}"
    params = {k: v for k, v in {
        'creditModelId': creditModelId,
        'balanceSheetId': balanceSheetId,
        'incomeStatementId': incomeStatementId
    }.items() if v is not None}

    return make_authenticated_request(config, url, method='POST', params=params, debug=debug)


def create_company_rating(env, client, companyId, creditModelId, effectiveDate, companyRating, debug=False):
    """
    Create a company rating for a specific company by its ID.

    Args:
        env (str): The environment where the external API is hosted.
        client (str): The client identifier for the API.
        companyId (str): The unique ID of the company to create the rating for.
        creditModelId (str): The ID of the credit model to associate with the rating.
        effectiveDate (str): The effective date of the rating.
        companyRating (float): The rating score for the company.
        debug (bool): Optional flag to enable debugging information.

    Returns:
        dict: Confirmation of the rating creation in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/risk/company-ratings/create/{companyId}"
    data = {
        'creditModelId': creditModelId,
        'effectiveDate': effectiveDate,
        'companyRating': companyRating
    }

    return make_authenticated_request(config, url, method='POST', json=data, debug=debug)


def get_all_wari_ratings(env, client, countryId=None, ratingAgencyId=None, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all WARI ratings for a country with optional countryId, ratingAgencyId, and pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - countryId (str, optional): Country UUID from which the WARI ratings will be returned.
    - ratingAgencyId (str, optional): Rating agency UUID from which the WARI ratings will be returned.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of WARI ratings in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/country-ratings/wari-ratings"

    params = {
        'countryId': countryId,
        'ratingAgencyId': ratingAgencyId
    }
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_wari_rating_info(env, client, wariRatingId, debug=False):
    """
    GET: Retrieve details for a specific WARI rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - wariRatingId (str): The unique ID of the WARI rating to retrieve.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The WARI rating details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/wari-ratings/{wariRatingId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_wari_rating(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new WARI rating.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): Data for the new WARI rating.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the creation in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/country-ratings/wari-ratings"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_wari_rating(env, client, wariRatingId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing WARI rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - wariRatingId (str): The unique ID of the WARI rating to update. 
    - data (dict): Updated data for the WARI rating.
    - debug (bool, optional): If True, prints the URL for debugging purposes.
    
    Returns:
    - dict: Confirmation of the update in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/wari-ratings/{wariRatingId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_wari_rating(env, client, wariRatingId, debug=False):
    """
    DELETE: Delete a specific WARI rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - wariRatingId: The unique ID of the WARI rating to be deleted.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the delete operation in JSON format, or an error message if the deletion failed.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/wari-ratings/{wariRatingId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)


def get_all_ihi_ratings(env, client, countryId=None, ratingAgencyId=None, limit=None, offset=None, debug=False):
    """
    GET: Retrieve a list of all IHI ratings for a country with optional countryId, ratingAgencyId, and pagination.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - countryId (str, optional): Country UUID from which the IHI ratings will be returned.
    - ratingAgencyId (str, optional): Rating agency UUID from which the IHI ratings will be returned.
    - limit (int, optional): The number of results to return per page.
    - offset (int, optional): The starting point for pagination.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A list of IHI ratings in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/country-ratings/ihi-ratings"

    params = {
        'countryId': countryId,
        'ratingAgencyId': ratingAgencyId
    }
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    return make_authenticated_request(config, url, method='GET', params=params, debug=debug)


def get_ihi_rating_info(env, client, ihiRatingId, debug=False):
    """
    GET: Retrieve details for a specific ihi rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - ihiRatingId (str): The unique ID of the IHI rating to retrieve.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: The IHI rating details in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/ihi-ratings/{ihiRatingId}"

    return make_authenticated_request(config, url, method='GET', debug=debug)


def create_ihi_rating(env, client, data, multiSend=False, sendSize=20, debug=False):
    """
    POST: Create a new IHI rating.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - data (dict): Data for the new IHI rating.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: Confirmation of the creation in JSON format.
    """
    config = get_api_config(env, client)
    url = "/external-api/country-ratings/ihi-ratings"

    return make_authenticated_request(config, url, method='POST', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def update_ihi_rating(env, client, ihiRatingId, data, multiSend=False, sendSize=20, debug=False):
    """
    PUT: Update an existing IHI rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - ihiRatingId (str): The unique ID of the IHI rating to update. 
    - data (dict): Updated data for the IHI rating.
    - debug (bool, optional): If True, prints the URL for debugging purposes.
    
    Returns:
    - dict: Confirmation of the update in JSON format.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/ihi-ratings/{ihiRatingId}"

    return make_authenticated_request(config, url, method='PUT', data=data, debug=debug, multiSend=multiSend, sendSize=sendSize)


def delete_ihi_rating(env, client, ihiRatingId, debug=False):
    """
    DELETE: Delete a specific IHI rating by its ID.

    Parameters:
    - env (str): The environment where the external API is hosted.
    - client (str): The client identifier for the API.
    - wariRatingId: The unique ID of the IHI rating to be deleted.
    - debug (bool, optional): If True, prints the URL for debugging purposes.

    Returns:
    - dict: A confirmation of the delete operation in JSON format, or an error message if the deletion failed.
    """
    config = get_api_config(env, client)
    url = f"/external-api/country-ratings/ihi-ratings/{ihiRatingId}"

    return make_authenticated_request(config, url, method='DELETE', debug=debug)
