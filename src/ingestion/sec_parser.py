import json
import pandas as pd
from pathlib import Path

def load_raw_company_facts(file_path: str | Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def parse_concept_records(data: dict, concept: str, unit: str = "USD") -> list[dict]:
    us_gaap = data["facts"]["us-gaap"]
    concept_data = us_gaap[concept]
    records = concept_data["units"][unit]
    parsed_records = []

    for record in records:
        parsed_record = {
            "company_cik": data["cik"],
            "entity_name": data["entityName"],
            "concept": concept,
            "unit": unit,
            "start_date": record.get("start"),
            "end_date": record.get("end"),
            "value": record["val"],
            "fiscal_year": record.get("fy"),
            "fiscal_period": record.get("fp"),
            "form": record.get("form"),
            "accession_number": record.get("accn"),
            "filed_date": record.get("filed"),
            "frame": record.get("frame"),
        }

        parsed_records.append(parsed_record)

    return parsed_records


def parse_financial_facts(data: dict, concepts: list[str], unit: str = "USD") -> list[dict]:
    all_records = []

    for concept in concepts:
        records = parse_concept_records(data, concept, unit)
        all_records.extend(records)

    return all_records


def create_financial_dataframe(financial_records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(financial_records)
    date_columns = ["start_date", "end_date", "filed_date",]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    df["value"] = pd.to_numeric(df["value"])
    df["company_cik"] = df["company_cik"].astype(str)

    return df


def save_financial_dataframe(df: pd.DataFrame, output_path: str | Path = "data/processed/financial_facts.csv") -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    return output_path