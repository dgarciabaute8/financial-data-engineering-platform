from src.analytics.silver_loader import load_silver_companies

COMPANIES = {
    "Apple": "0000320193",
    "Microsoft": "0000789019",
    "Amazon": "0001018724",
    "Alphabet": "0001652044",
}


df = load_silver_companies(COMPANIES)

print("=" * 60)
print("COMBINED SILVER DATASET")
print("=" * 60)

print("\nRows:")
print(len(df))

print("\nCompanies:")
print(df["company"].value_counts())

print("\nConcepts:")
print(df["concept"].value_counts())

print("\nColumns:")
print(df.columns.tolist())