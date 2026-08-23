import pandas as pd

from src.ingestion.sec_parser import (load_raw_company_facts, parse_financial_facts, create_financial_dataframe, save_financial_dataframe,)

file_path = "data/raw/sec/companyfacts_0000320193.json"

data = load_raw_company_facts(file_path)

concepts = [
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "CashAndCashEquivalentsAtCarryingValue",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "OperatingIncomeLoss",
    "NetIncomeLoss",
]

financial_records = parse_financial_facts(data, concepts)

df = create_financial_dataframe(financial_records)

output_path = save_financial_dataframe(df)

print("\nSilver dataset saved to:")
print(output_path)