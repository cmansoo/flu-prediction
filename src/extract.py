import requests
import pandas as pd

VALID_ENDPOINTS = {"fluview", "fluview_clinical", "flusurv", "fluview_meta"}
ENDPOINT_MAIN_PARAM = {
    "fluview": "regions",
    "fluview_clinical": "regions",
    "flusurv": "locations",
    "fluview_meta": None
}

def fetch_epidata(endpoint, start_week, end_week, **kwargs):
    """
    Fetch epidata using Delphi Epidata API. Returns a pandas DataFrame.

    Parameters:
    - endpoint: str, one of "fluview", "fluview_clinical", "flusurv", "fluview_meta"
    - start_week: str, in format "YYYYWW" (e.g. "202001" for the first week of 2020)
    - end_week: str, in format "YYYYWW" (e.g. "202052" for the last week of 2020)
    - Main parameter (required for all endpoints except fluview_meta):
        fluview / fluview_clinical → regions="nat"
        flusurv → locations="nat"
        - Additional parameters can be passed as keyword arguments (e.g. `issues`, `lag`, `auth`)

    """
    
    if endpoint not in VALID_ENDPOINTS:
        raise ValueError(f"Invalid endpoint: {endpoint}. Valid options are: {VALID_ENDPOINTS}")
        
    url = f"https://api.delphi.cmu.edu/epidata/{endpoint}/"
    params = {}

    # epiweek validation
    if endpoint != "fluview_meta" and (start_week is None or end_week is None):
        raise ValueError("start_week and end_week are required for this endpoint.")
    
    params["epiweeks"] = f"{start_week}-{end_week}"
    
    # validate main parameter
    main_param = ENDPOINT_MAIN_PARAM[endpoint]
    if main_param is not None:
        if main_param not in kwargs.keys():
            raise ValueError(f"Missing required parameter: {main_param} for endpoint {endpoint}.")
        params[main_param] = kwargs[main_param]

    # add addional parameters if provided    
    params.update(kwargs)
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("epidata", [])
        return pd.DataFrame(data)
    else:
        print(f"Error fetching data: {response.status_code}. Response: {response.text}")
        return pd.DataFrame()
    

# example usage
if __name__ == "__main__":
    df = fetch_epidata(
        endpoint="fluview",
        start_week="202001",
        end_week="202052",
        regions="nat"
    )
    display(df.head())

