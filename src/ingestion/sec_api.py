import os 
from pathlib import Path
import json

import requests 
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# User-Agent required by the SEC API.
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")


def get_company_facts(cik: str) -> dict:
    """
    Retrieve company facts from the SEC API.

    Parameters
    ----------
    cik : str
        SEC Central Index Key (CIK) of the company.
        The CIK must be provided as a 10-digit string.

    Returns
    -------
    dict
        Company facts returned by the SEC API in JSON format.
    """

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    # The SEC requires requests to include a descriptive User-Agent.
    headers = {"User-Agent": SEC_USER_AGENT}

    # Send the request to the SEC API.
    response = requests.get(url, headers=headers, timeout=30)

    # Raise an exception if the request was not successful
    response.raise_for_status()

    # Convert the API response from JSON into a Python dictionary.
    return response.json()


def save_raw_company_facts(cik: str, output_dir: str = "data/raw/sec") -> Path:
    """
    Retrieve company facts from the SEC API and save the raw response
    as a JSON file.

    This function represents the raw ingestion layer of the pipeline:
    data is obtained from the external SEC API and stored without
    transforming or cleaning it.

    Parameters
    ----------
    cik : str
        SEC Central Index Key (CIK) of the company.

    output_dir : str
        Directory where the raw JSON file will be stored.
        Defaults to "data/raw/sec".

    Returns
    -------
    Path
        Path to the JSON file containing the raw SEC data.
    """

    # Retrieve the company facts from the SEC API.
    data = get_company_facts(cik)

    # Create the output directory if it does not already exist.
    # parents=True also creates any missing parent directories.
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build the output filename using the company's CIK.
    file_path = output_path / f"companyfacts_{cik}.json"

    # Save the API response as a JSON file.
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    # Return the path so that other parts of the pipeline
    # can use the generated raw file.
    return file_path