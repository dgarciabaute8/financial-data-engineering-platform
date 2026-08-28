import pandas as pd

from src.quality.data_quality import (validate_data, is_quality_valid, deduplicate_financial_facts, INSTANT_CONCEPTS, PERIOD_CONCEPTS,)
from src.ingestion.sec_parser import save_silver_company_facts


def create_pipeline_dataframe() -> pd.DataFrame:
    return pd.DataFrame({
            "company_cik": ["0000320193", "0000320193"],
            "entity_name": ["Apple Inc.", "Apple Inc."],
            "concept": ["Assets", "Liabilities"],
            "unit": ["USD", "USD"],
            "start_date": [pd.NaT, pd.NaT],
            "end_date": pd.to_datetime(["2025-09-27", "2025-09-27"]),
            "value": [359241000000, 285000000000,],
            "fiscal_year": [2025, 2025],
            "fiscal_period": ["FY", "FY"],
            "form": ["10-K", "10-K"],
            "accession_number": ["0001", "0002"],
            "filed_date": pd.to_datetime(["2025-10-31", "2025-10-31"]),
            "frame": [None, None],})


def test_pipeline_data_passes_quality_gate():

    df = create_pipeline_dataframe()

    quality_report = validate_data(df)

    assert is_quality_valid(quality_report)


def test_pipeline_stops_when_quality_fails():

    df = create_pipeline_dataframe()

    df.loc[0, "unit"] = "EUR"

    quality_report = validate_data(df)

    assert not is_quality_valid(quality_report)


def create_dataframe_with_duplicates() -> pd.DataFrame:

    return pd.DataFrame({
            "company_cik": ["0000320193", "0000320193", "0000320193",],
            "entity_name": ["Apple Inc.", "Apple Inc.", "Apple Inc.",],
            "concept": ["Assets", "Assets", "Assets",],
            "unit": ["USD", "USD", "USD",],
            "start_date": [pd.NaT, pd.NaT, pd.NaT,],
            "end_date": pd.to_datetime(["2025-09-27", "2025-09-27", "2025-09-27",]),
            "value": [350000000000, 350000000000, 360000000000,],
            "fiscal_year": [2025, 2025, 2025,],
            "fiscal_period": ["FY", "FY", "FY",],
            "form": ["10-K", "10-K", "10-K",],
            "accession_number": ["0001", "0002", "0003",],
            "filed_date": pd.to_datetime(["2025-10-01", "2025-10-15", "2025-10-31",]),
            "frame": [None, None, None,],})


def test_pipeline_deduplicates_financial_facts():

    df = create_dataframe_with_duplicates()

    curated_df = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS,)

    assert len(curated_df) == 1

    record = curated_df.iloc[0]

    assert record["value"] == 360000000000

    assert record["filed_date"] == pd.Timestamp("2025-10-31")


def test_pipeline_saves_and_loads_silver(tmp_path):

    df = create_dataframe_with_duplicates()

    curated_df = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS,)

    silver_path = save_silver_company_facts(curated_df, cik="0000320193", output_dir=tmp_path,)

    silver_df = pd.read_parquet(silver_path)

    assert len(silver_df) == 1

    assert silver_df.iloc[0]["value"] == 360000000000

    assert silver_df.iloc[0]["concept"] == "Assets"