import requests
import pandas as pd
from datetime import date

VALID_ENDPOINTS = {"fluview", "fluview_clinical", "flusurv", "fluview_meta"}
ENDPOINT_MAIN_PARAM = {
    "fluview": "regions",
    "fluview_clinical": "regions",
    "flusurv": "locations",
    "fluview_meta": None
}
# reference: https://cmu-delphi.github.io/delphi-epidata/api/geographic_codes.html
FLUSURV_LOCATIONS = [
    "CA", "CO", "CT", "GA", "IA", "ID", "MD", "MI", "MN",
    "NM", "OH", "OK", "OR", "RI", "SD", "TN",
    "NY_albany", "NY_rochester", "UT"
]

FLUSURV_TO_FLUVIEW = {
    "NY_albany": "Albany_NY",
    "NY_rochester": "Rochester_NY"
}


def fetch_epidata(endpoint, start_week, end_week, **kwargs):
    """
    Fetch epidata using Delphi Epidata API. Returns a pandas DataFrame.

    Parameters:
    - endpoint: str, one of "fluview", "fluview_clinical", "flusurv", "fluview_meta"
    - start_week: str, in format "YYYYWW" (e.g. "202001" for the first week of 2020)
    - end_week: str, in format "YYYYWW" (e.g. "202052" for the last week of 2020)
    - Main parameter (required for all endpoints except fluview_meta):
        fluview / fluview_clinical - regions (str or [str])="nat"
        flusurv - locations (str or [str])="nat"
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
        params[main_param] = kwargs.pop(main_param)

    # add additional parameters if provided    
    params.update(kwargs)
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("epidata", [])
        return pd.DataFrame(data)
    else:
        print(f"Error fetching data: {response.status_code}. Response: {response.text}")
        return pd.DataFrame()
    

def fetch_and_merge_flu_data(start_week, end_week, locations):
    """
    Fetch FluView, FluView Clinical, and FluSurv data for any user-selected locations.
    
    Parameters:
    - start_week, end_week: epiweek strings (YYYYWW)
    - locations: list of location codes (states, regions, or cities)
    
    Returns:
    - merged pandas DataFrame with epiweek + region
    """

    # Fetch FluView and FluView Clinical
    fluview_df = fetch_epidata(
        endpoint="fluview",
        start_week=start_week,
        end_week=end_week,
        regions=locations
    )
    
    fluview_clinical_df = fetch_epidata(
        endpoint="fluview_clinical",
        start_week=start_week,
        end_week=end_week,
        regions=locations
    )

    # Fetch FluSurv
    flusurv_df = pd.DataFrame(columns=["epiweek", "region"])
    flusurv_locations = [loc for loc in locations if loc in FLUSURV_LOCATIONS]

    if flusurv_locations:
        flusurv_df = fetch_epidata(
            endpoint="flusurv",
            start_week=start_week,
            end_week=end_week,
            locations=flusurv_locations
        )
        flusurv_df = flusurv_df.rename(columns={"location": "region"})
        flusurv_df["region"] = flusurv_df["region"].replace(FLUSURV_TO_FLUVIEW)

    skipped_locations = [loc for loc in locations if loc not in FLUSURV_LOCATIONS]
    if skipped_locations:
        print(f"Skipped FluSurv locations: {skipped_locations}")

    # Merge datasets on epiweek + region
    merged_df = (
        fluview_df
        .merge(fluview_clinical_df, on=["epiweek", "region"], how="left")
        .merge(flusurv_df, on=["epiweek", "region"], how="left")
    )
    
    return merged_df


# Example usage: query 15 years of data until today
if __name__ == "__main__":
    today = date.today()
    iso_year, iso_week, _ = today.isocalendar()
    start_week = f"{iso_year - 15}{iso_week:02d}"
    end_week = f"{iso_year}{iso_week:02d}"
    locations = ["MN", "NY_albany", "NY_rochester", "TN"]

    merged_df = fetch_and_merge_flu_data(start_week, end_week, locations)
    print(merged_df.head())