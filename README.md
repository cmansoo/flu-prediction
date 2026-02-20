# Influenze Forecasting

## Overview
Using the CDC FluSurv Influenza-like Ilness (ILI) data, we aim to forecast weekly influenza-associated hospitalization. The objective is to build an automated data pipeline that extracts and processes data with subsequent predictive modeling.

This project demonstrates application of Python and machine learning algorithms in the healthcare sector.

---

## Data Source
- **CDC FluSurv-NET**: Weekly influenza hospitalization counts ([link](https://www.cdc.gov/fluview/overview/influenza-hospitalization-surveillance.html)). The data canbe accessed by [Delphi Epidata API](https://cmu-delphi.github.io/delphi-epidata/api/fluview.html). 

**Flusurv** Database contains 4 datasets:
- fluview
- fluview metadata
- fluview clinical
- flusurv

**Important Definitions/Variables**

Definition of ILI: ILI is defined as fever (temperature of 100°F [37.8°C] or greater) and a cough and/or a sore throat without a known cause other than influenza.

The fluview endpoint provides two percentage metrics: ili (unweighted) and wili (weighted).
- Unweighted (`ili`): Calculated simply as the number of ILI cases divided by the total number of patients seen.
- Weighted (`wili`): To produce a representative estimate for larger regions (like National or HHS Regions), the CDC weights the state-level data by state population. This corrects for the fact that some states may have higher provider participation rates than others relative to their actual population.

<!-- - **CDC FluSight Forecast Hub**: Historical truth data and benchmark forecasts ([GitHub link](https://github.com/cdcepi/Flusight-forecast-data))
- Additional features (optional): environmental data, mobility data, seasonal indicators.
- (Option 1, CDC SODA API) https://dev.socrata.com/ - use the API v4
- (Option 2 for extracting data) Delphi Epidata API — flusurv endpoint https://cmu-delphi.github.io/delphi-epidata/api/flusurv.html

Data source https://data.cdc.gov/Public-Health-Surveillance/Weekly-United-States-Hospitalization-Metrics-by-Ju/aemt-mg7g/about_data


******* THE FluSurv-NET data can only be access by Delphi Epidata API
WE USE DELPHI EPIDATA
Installation pip install "git+https://github.com/cmu-delphi/epidatpy.git#egg=epidatpy" <- this is the main API for covid we dont want this -->


<!-- Their webased API https://cmu-delphi.github.io/delphi-epidata/api/fluview.html -->


---

---
<!-- OData API

Feature	OData v4	SODA v1
URL	/api/odata/v4/<dataset_id>	/resource/<dataset_id>.json
Query syntax	OData $top, $filter, $select, $orderby	SODA $limit, $where, $select, $order
Authentication	Usually none for public datasets	Usually none for public datasets
Output	JSON (or XML)	JSON (or CSV)

OData v4 is standardized for RESTful querying and is fully supported by Python. -->

---



## Project Structure
```
Flu_prediction/
│
├── data/
│   ├── raw/           # Raw CSV/JSON pulled from CDC (not committed to Git)
│   └── processed/     # Cleaned data, ready for modeling (optional)
│
├── src/               # Python scripts
│   ├── extract.py     # Pulls data from CDC APIs
│   ├── transform.py   # Cleans, preprocesses, creates features
│   ├── train.py       # Train forecasting models
│   ├── predict.py     # Generate forecasts
│   └── utils.py       # Helper functions
│
├── notebooks/         # Jupyter notebooks for exploration
│   └── exploratory.ipynb
│
├── models/            # Saved models (.pkl, .joblib) — ignored by Git
│
├── venv/              # Virtual environment (ignored by Git)
│
├── .gitignore         # Ignore venv, data, models
├── requirements.txt   # Python dependencies
└── README.md          # Project overview and instructions
```

---

## Getting Started

1. **Clone the repo**:

```bash
git clone https://github.com/yourusername/influenza-forecasting-pipeline.git
cd influenza-forecasting-pipeline
```
2. **Create Virtual Environment**

```bash
python -m venv venv
.\venv\Scripts\activate.bat # activate your venv
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```
