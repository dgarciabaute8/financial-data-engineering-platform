import argparse

from src.ingestion.sec_api import save_raw_company_facts
from src.ingestion.sec_parser import (load_raw_company_facts, parse_financial_facts, create_financial_dataframe, save_silver_company_facts, )
from src.quality.data_quality import (deduplicate_financial_facts, validate_data, is_quality_valid, INSTANT_CONCEPTS, PERIOD_CONCEPTS, )
from src.config import COMPANIES

CONCEPTS = [
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "CashAndCashEquivalentsAtCarryingValue",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "OperatingIncomeLoss",
    "NetIncomeLoss",
]

def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Run the financial data engineering pipeline.")

    parser.add_argument("cik", help="SEC Central Index Key (CIK) of the company to process.",)

    return parser.parse_args()

def normalize_cik(cik: str) -> str:
    return cik.zfill(10)

def run_pipeline(cik: str) -> None:

    print("=" * 60)
    print("FINANCIAL DATA ENGINEERING PIPELINE")
    print("=" * 60)

    # 1. INGESTION
    print("\n[1/6] Ingestion")

    raw_path = save_raw_company_facts(cik)

    print(f"Raw data saved: {raw_path}")

    # 2. LOAD RAW
    print("\n[2/6] Loading raw data")

    raw_data = load_raw_company_facts(raw_path)

    print("Raw data loaded successfully")

    # 3. PARSING
    print("\n[3/6] Parsing")

    financial_records = parse_financial_facts(raw_data, CONCEPTS,)
    df = create_financial_dataframe(financial_records)

    print(f"Parsed records: {len(df)}")

    # 4. Data Quality
    print("\n[4/6] Data Quality")

    quality_report = validate_data(df)

    print("Missing columns:", quality_report["missing_columns"])
    print("Unexpected concepts:", quality_report["unexpected_concepts"])
    print("Unexpected units:", quality_report["unexpected_units"])
    print("Critical nulls:", quality_report["critical_nulls"])
    print("Duplicate records:", quality_report["duplicate_records"])

    if not is_quality_valid(quality_report):
        print("\nDATA QUALITY FAILED")
        raise ValueError(
            "Data quality checks failed. "
            "Pipeline stopped.")

    print("\nDATA QUALITY PASSED")


    # 5. DEDUPLICATION
    print("\n[5/6] Deduplication")

    records_before = len(df)

    curated_df = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS, )

    records_after = len(curated_df)

    print(f"Records before: {records_before}")
    print(f"Records after: {records_after}")
    print(f"Records removed: {records_before - records_after}")

    # 6. SAVE SILVER
    print("\n[6/6] Silver")

    silver_path = save_silver_company_facts(curated_df, cik, )

    print(f"Silver data saved: {silver_path}")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

if __name__ == "__main__":
    for company_name, cik in COMPANIES.items():
        print(f"\nProcessing company: {company_name}")
        print(f"CIK: {cik}")
        run_pipeline(cik)