import time
import external.api_client as externalAPI


def fetch_all_assemblies(env, client, aircraftId=None, batch_size=100, max_retries=5, backoff_factor=2, log_interval=100, debug=False):
    """
    Fetch all assemblies from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - aircraftId (str, optional): Optional aircraft ID to filter assemblies by a specific aircraft.
    - batch_size (int): The number of assemblies to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 5000 assemblies.

    Returns:
    - list: A list of all fetched assemblies.
    """
    all_assemblies = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Assembly Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch assemblies using the external API
            response = externalAPI.get_all_assemblies_for_aircraft(env, client, aircraftId=aircraftId, limit=batch_size, offset=offset, debug=debug)

            # Check if we have valid entries in the response
            if response and 'entries' in response and response['entries']:
                all_assemblies.extend(response['entries'])
                offset += batch_size
                total_count += len(response['entries'])

                # Log progress after every log_interval assemblies
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} assemblies so far...")

                # If fewer than batch_size entries are returned, stop the loop
                if len(response['entries']) < batch_size:
                    run = False

            else:
                # Stop if no entries are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
                # Exponential backoff before retrying
                wait_time = backoff_factor ** retry_count
                print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
                time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} assemblies.")
    return all_assemblies


def fetch_all_aircraft_details(env, client, batch_size=100, max_retries=5, backoff_factor=2, log_interval=100, debug=False):
    """
    Fetch all aircraft details from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - batch_size (int): The number of aircraft details to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 5000 aircraft details.

    Returns:
    - list: A list of all fetched aircraft details.
    """
    all_aircraft_details = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Aircraft Details Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch aircraft details using the external API
            response = externalAPI.search_aircraft(env, client, limit=batch_size, offset=offset, debug=debug)

            # Check if we have valid entries in the response
            if response and 'entries' in response and response['entries']:
                all_aircraft_details.extend(response['entries'])
                offset += batch_size
                total_count += len(response['entries'])

                # Log progress after every log_interval aircraft details
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} aircraft details so far...")

                # If fewer than batch_size entries are returned, stop the loop
                if len(response['entries']) < batch_size:
                    run = False

            else:
                # Stop if no entries are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            # Exponential backoff before retrying
            wait_time = backoff_factor ** retry_count
            print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
            time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} aircraft details.")
    return all_aircraft_details


def fetch_all_aircraft_part_maintenance_policy_types(env, client, aircraftPartTypeId=None, batch_size=20, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all aircraft part maintenance policy types from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - aircraftPartTypeId (str, optional): Optional aircraft part type ID to filter policy types.
    - batch_size (int): The number of policy types to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 5000 policy types.

    Returns:
    - list: A list of all fetched policy types.
    """
    all_policy_types = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Aircraft Part Maintenance Policy Type Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch policy types using the external API
            response = externalAPI.get_all_aircraft_part_maintenance_policy_types(env, client, limit=batch_size, offset=offset, aircraftPartTypeId=aircraftPartTypeId, debug=debug)

            # Check if we have valid items in the response
            if response and 'items' in response and response['items']:
                all_policy_types.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress after every log_interval policy types
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} policy types so far...")

                # If fewer than batch_size items are returned, stop the loop
                if len(response['items']) < batch_size:
                    run = False

            else:
                # Stop if no items are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            else:
                # Exponential backoff before retrying
                wait_time = backoff_factor ** retry_count
                print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
                time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} policy types.")
    return all_policy_types


def fetch_all_companies(env, client, filter=None, batch_size=20, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all companies from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - filter (str, optional): A filter string based on company roles.
    - batch_size (int): The number of companies to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 5000 companies.

    Returns:
    - list: A list of all fetched companies.
    """
    all_companies = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Companies Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch companies using the external API
            response = externalAPI.get_all_companies(env, client, limit=batch_size, offset=offset, filter=filter, debug=debug)

            # Check if we have valid items in the response
            if response and 'items' in response and response['items']:
                all_companies.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress after every log_interval companies
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} companies so far...")

                # If fewer than batch_size items are returned, stop the loop
                if len(response['items']) < batch_size:
                    run = False

            else:
                # Stop if no items are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            else:
                # Exponential backoff before retrying
                wait_time = backoff_factor ** retry_count
                print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
                time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} companies.")
    return all_companies


def fetch_all_balance_sheets_per_company(env, client, companyId, batch_size=20, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all balance sheets for a specific company from the external API using pagination, with retries,
    backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - companyId (str): UUID of the company for which balance sheets are fetched.
    - batch_size (int): The number of balance sheets to fetch per request. Default is 20.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 100 sheets.

    Returns:
    - list: A list of all fetched balance sheets.
    """
    all_balance_sheets = []
    offset = 0
    total_count = 0
    retry_count = 0
    log_count = 0
    run = True
    print(f"Starting Balance Sheets Extract for Company {companyId} from External API")

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch balance sheets for the specified company
            response = externalAPI.get_balance_sheet_list_per_company(
                env, client, companyId, limit=batch_size, offset=offset, debug=debug
            )

            # Validate response
            if response and 'items' in response and response['items']:
                all_balance_sheets.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress at intervals
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} balance sheets so far...")

                # Stop loop if fewer items than batch_size are returned
                if len(response['items']) < batch_size:
                    run = False

            else:
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print("Max retries reached. Stopping the fetch.")
                break
            else:
                # Exponential backoff
                wait_time = backoff_factor ** retry_count
                print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
                time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} balance sheets for Company {companyId}.")
    return all_balance_sheets


def fetch_all_income_statements_per_company(env, client, companyId, batch_size=20, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all income statements for a specific company from the external API using pagination, with retries,
    backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - companyId (str): UUID of the company for which income statements are fetched.
    - batch_size (int): The number of income statements to fetch per request. Default is 20.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 100 statements.

    Returns:
    - list: A list of all fetched income statements.
    """
    all_income_statements = []
    offset = 0
    total_count = 0
    retry_count = 0
    log_count = 0
    run = True
    print(f"Starting Income Statements Extract for Company {companyId} from External API")

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch income statements for the specified company
            response = externalAPI.get_income_statement_list_per_company(
                env, client, companyId, limit=batch_size, offset=offset, debug=debug
            )

            # Validate response
            if response and 'items' in response and response['items']:
                all_income_statements.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress at intervals
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} income statements so far...")

                # Stop loop if fewer items than batch_size are returned
                if len(response['items']) < batch_size:
                    run = False

            else:
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print("Max retries reached. Stopping the fetch.")
                break
            else:
                # Exponential backoff
                wait_time = backoff_factor ** retry_count
                print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
                time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} income statements for Company {companyId}.")
    return all_income_statements


def fetch_all_engine_models(env, client, batch_size=100, max_retries=5, backoff_factor=2, log_interval=100, debug=False):
    """
    Fetch all engine models from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - batch_size (int): The number of engine models to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 100 engine models.

    Returns:
    - list: A list of all fetched engine models.
    """
    all_engine_models = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Engine Models Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch engine models using the external API
            response = externalAPI.get_engine_model_list(env, client, limit=batch_size, offset=offset, debug=debug)

            # Check if we have valid entries in the response
            if response and 'items' in response and response['items']:
                all_engine_models.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress after every log_interval engine models
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} engine models so far...")

                # If fewer than batch_size items are returned, stop the loop
                if len(response['items']) < batch_size:
                    run = False

            else:
                # Stop if no items are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            # Exponential backoff before retrying
            wait_time = backoff_factor ** retry_count
            print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
            time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} engine models.")
    return all_engine_models


def fetch_all_aircraft_models(env, client, batch_size=100, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all aircraft models from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - batch_size (int): The number of aircraft models to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 100 aircraft models.

    Returns:
    - list: A list of all fetched aircraft models.
    """
    all_aircraft_models = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Aircraft Models Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch aircraft models using the external API
            response = externalAPI.get_aircraft_model_list(env, client, limit=batch_size, offset=offset, debug=debug)

            # Check if we have valid entries in the response
            if response and 'items' in response and response['items']:
                all_aircraft_models.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress after every log_interval aircraft models
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} aircraft models so far...")

                # If fewer than batch_size items are returned, stop the loop
                if len(response['items']) < batch_size:
                    run = False

            else:
                # Stop if no items are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            # Exponential backoff before retrying
            wait_time = backoff_factor ** retry_count
            print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
            time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} aircraft models.")
    return all_aircraft_models


def fetch_all_aircraft_part_types(env, client, batch_size=100, max_retries=5, backoff_factor=2, log_interval=20, debug=False):
    """
    Fetch all aircraft part types from the external API using pagination with retries, backoff, and logging.

    Parameters:
    - env (str): Client environment (e.g., 'preprod').
    - client (str): The client identifier for the external API.
    - batch_size (int): The number of aircraft models to fetch per request. Default is 100.
    - max_retries (int): Maximum number of retries in case of API failures. Default is 5.
    - backoff_factor (int): Factor by which to increase the wait time between retries. Default is 2.
    - log_interval (int): Interval for logging progress. Default is every 100 aircraft models.

    Returns:
    - list: A list of all fetched aircraft part types.
    """
    all_aircraft_part_types = []
    offset = 0
    total_count = 0
    retry_count = 0
    run = True
    log_count = 0
    print('Starting Aircraft Part Types Extract from External API')

    if batch_size > log_interval:
        log_interval = batch_size

    while run:
        try:
            # Fetch aircraft models using the external API
            response = externalAPI.get_aircraft_part_types_list(env, client, limit=batch_size, offset=offset, debug=debug)

            # Check if we have valid entries in the response
            if response and 'items' in response and response['items']:
                all_aircraft_part_types.extend(response['items'])
                offset += batch_size
                total_count += len(response['items'])

                # Log progress after every log_interval aircraft models
                if total_count // log_interval > log_count:
                    log_count += 1
                    print(f"Fetched {total_count} aircraft part types so far...")

                # If fewer than batch_size items are returned, stop the loop
                if len(response['items']) < batch_size:
                    run = False

            else:
                # Stop if no items are returned in the current batch
                print(f"Received empty or invalid response at offset {offset}. Stopping fetch.")
                break

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Stopping the fetch.")
                break
            # Exponential backoff before retrying
            wait_time = backoff_factor ** retry_count
            print(f"Retrying in {wait_time} seconds due to error: {str(e)}")
            time.sleep(wait_time)

    print(f"Finished fetching a total of {total_count} aircraft part types.")
    return all_aircraft_part_types


def check_assembly_dependencies(env: str, client: str, assemblyId: str, debug: bool = False) -> list[tuple]:
    """
    Function to check if an assembly has any dependencies (leases, analyses, etc.) to determine
    if it can be safely deleted.

    Parameters:
    env (str): The environment to check in (e.g., 'production', 'stage').
    client (str): The client for whom the assembly is being checked.
    assemblyId (str): The identifier of the assembly.
    debug (bool): Optional flag to enable debug logging.
    
    Returns:
    list[tuple]: A list of tuples with the count of leases, analyses, and tech specs (dependencies).
    """

    # Get assembly details
    assembly_details = externalAPI.get_assembly_details(env=env, client=client, assemblyId=assemblyId, debug=debug)

    # Extract aircraftId from the assembly details, required for fetching analyses.
    aircraftId = assembly_details.get("aircraftId")
    engineId_list = [engine['engineId'] for engine in assembly_details.get("engines")]
    partId_list = [part['aircraftPartId'] for part in assembly_details.get("parts")]

    # Fetch leases associated with the assembly
    leases = externalAPI.get_lease_list(env=env, client=client, assemblyId=assemblyId, debug=debug).get("items", [])
    count_of_leases = len(leases)

    # Fetch analyses associated with the aircraft
    analyses = externalAPI.get_analysis_contexts_for_aircraft(env=env, client=client, aircraftId=aircraftId, limit=None, offset=None, debug=debug).get("items", [])
    count_of_analyses = len(analyses)

    # Fetch Engines tech specs
    all_engine_snaps = []
    for engineId in engineId_list:
        engine_snaps = externalAPI.get_engine_snapshot_list(env=env, client=client, debug=debug, engineId=engineId).get("items", [])
        all_engine_snaps.append(engine_snaps)
    count_of_engine_snaps = len(all_engine_snaps)

    # Fetch Part Snapshots
    all_part_snaps = []
    for partId in partId_list:
        part_snaps = externalAPI.get_aircraft_part_snapshot_list(env=env, client=client, debug=debug, aircraftPartId=partId).get("items", [])
        all_part_snaps.append(part_snaps)
    count_of_part_snaps = len(all_part_snaps)

    # Return the results as a list of tuples
    return [("Leases", count_of_leases), ("Analyses", count_of_analyses), ("Engine Snaps", count_of_engine_snaps), ("Part Snaps", count_of_part_snaps)]
