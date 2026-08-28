import pandas as pd

from src.analytics.silver_loader import load_silver_companies
from src.analytics.gold_financial_statements import build_gold_financial_statements

COMPANIES = {
    "Apple": "0000320193",
    "Microsoft": "0000789019",
    "Amazon": "0001018724",
    "Alphabet": "0001652044",
}


def test_gold_financial_statements_returns_dataframe():

    silver_df = load_silver_companies(COMPANIES)

    gold_df = build_gold_financial_statements(silver_df)

    assert isinstance(gold_df, pd.DataFrame)


def test_gold_contains_expected_columns():

    silver_df = load_silver_companies(COMPANIES)

    gold_df = build_gold_financial_statements(silver_df)

    expected_columns = {
        "company",
        "period",
        "assets",
        "liabilities",
        "equity",
        "cash",
        "revenue",
        "operating_income",
        "net_income",
    }

    assert expected_columns.issubset(set(gold_df.columns))


def test_gold_contains_all_companies():

    silver_df = load_silver_companies(COMPANIES)

    gold_df = build_gold_financial_statements(silver_df)

    assert set(gold_df["company"].unique()) == {
        "Apple",
        "Microsoft",
        "Amazon",
        "Alphabet",
    }


def test_gold_has_unique_company_period():

    silver_df = load_silver_companies(COMPANIES)

    gold_df = build_gold_financial_statements(silver_df)

    duplicates = gold_df.duplicated(subset=["company", "period"]).sum()

    assert duplicates == 0