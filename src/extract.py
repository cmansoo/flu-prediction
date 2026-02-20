import requests
import pandas as pd

def extract_fluview(regions, start_epiweek, end_epiweek):
    """
    Extracts FluView data using Delphi Epidata API for specified regions and epiweeks.
    
    :param regions (str or list): List of regions to query (e.g., ["nat", "NY", "CA"])
    :param start_epiweek (int): start epiweek in the format YYYYWW (e.g., 202001 for the first week of 2020)
    :param end_epiweek (int): end epiweek in the format YYYYWW (e.g., 202052 for the last week of 2020)
    
    Returns: 
        a pd.DataFrame
    """
    # Delphi Epidata API endpoint
    url = "https://api.delphi.cmu.edu/epidata/fluview/"

    if isinstance(regions, list):
        regions = ",".join(regions)

    # query parameters
    params = {
        "regions": regions,
        "epiweeks": f"{start_epiweek}-{end_epiweek}",
        "format": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200: # status OK
        data = response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return pd.DataFrame(data)

def main():
    # Example usage
    regions = ["nat", "NY", "CA"]
    start_epiweek = 202001
    end_epiweek = 202052

    fluview_data = extract_fluview(regions, start_epiweek, end_epiweek)
    print(fluview_data)

if __name__ == "__main__":
    main()