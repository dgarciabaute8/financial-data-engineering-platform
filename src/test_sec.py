from ingestion.sec_api import save_raw_company_facts

file_path = save_raw_company_facts("0000320193")

print(f"Raw data saved to: {file_path}")