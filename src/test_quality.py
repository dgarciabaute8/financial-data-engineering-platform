from ingestion.sec_parser import (load_raw_company_facts, parse_financial_facts, create_financial_dataframe, )

from quality.data_quality import (validate_required_columns, validate_concepts, validate_units, validate_nulls, find_duplicate_records, find_logical_duplicates, analyze_logical_duplicates, )

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

required_columns = [
    "company_cik",
    "entity_name",
    "concept",
    "unit",
    "end_date",
    "value",
    "form",
    "accession_number",
    "filed_date",
]

print("=== DATA QUALITY REPORT ===")

missing_columns = validate_required_columns(df, required_columns)

print("\nMissing columns:")
print(missing_columns)

unexpected_concepts = validate_concepts(df, concepts)

print("\nUnexpected concepts:")
print(unexpected_concepts)

unexpected_units = validate_units(df)

print("\nUnexpected units:")
print(unexpected_units)

nulls = validate_nulls(df, required_columns)

print("\nCritical nulls:")
print(nulls)

'''duplicates = find_duplicate_records(df)

print("\nDuplicate records:")
print(duplicates)

print("\n=== POTENCIAL DUPLICATES ===")

potencial_duplicates = df[df.duplicated(subset=["company_cik", "concept", "end_date", "value", ], keep=False, )].sort_values(["concept", "end_date", "filed_date", ])
print(potencial_duplicates.to_string(index=False))'''

instant_key = [
    "company_cik",
    "concept",
    "end_date",
    "value",
]

period_key = [
    "company_cik",
    "concept",
    "start_date",
    "end_date",
    "value",
]

logical_duplicates = find_logical_duplicates(df, instant_key)
print("\nLogical duplicates (instant):")
print(len(logical_duplicates))
print(logical_duplicates.groupby("concept").size())

logical_duplicates = find_logical_duplicates(df, period_key)
print("\nLogical duplicates (period):")
print(len(logical_duplicates))
print(logical_duplicates.groupby("concept").size())

INSTANT_CONCEPTS = ["Assets", "Liabilities", "StockholdersEquity", "CashAndCashEquivalentsAtCarryingValue", ]
PERIOD_CONCEPTS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "OperatingIncomeLoss", "NetIncomeLoss", ]

instant_duplicates = analyze_logical_duplicates(df[df["concept"].isin(INSTANT_CONCEPTS)], ["company_cik", "concept", "end_date", ], )
print("\n=== INSTANT LOGICAL DUPLICATES ===")
print(instant_duplicates.head(20).to_string(index=False))

period_duplicates = analyze_logical_duplicates(df[df["concept"].isin(PERIOD_CONCEPTS)], ["company_cik", "concept", "start_date", "end_date", ], )
print("\n=== PERIOD LOGICAL DUPLICATES ===")
print(period_duplicates.head(20).to_string(index=False))

