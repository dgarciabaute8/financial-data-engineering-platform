import os 
from pathlib import Path

import requests 
from dotenv import load_dotenv

load_dotenv()

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")


def get_company_facts(cik: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    headers = {"User-Agent": SEC_USER_AGENT}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()

def save_raw_company_facts(cik: str, output_dir: str = "data/raw/sec") -> Path:
    data = get_company_facts(cik)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"companyfacts_{cik}.json"

    import json
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    return file_path