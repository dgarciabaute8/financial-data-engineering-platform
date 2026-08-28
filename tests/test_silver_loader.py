import pandas as pd

from src.analytics.silver_loader import (load_silver_company, load_silver_companies,)


COMPANIES = {
    "Apple": "0000320193",
    "Microsoft": "0000789019",
    "Amazon": "0001018724",
    "Alphabet": "0001652044",
}


def test_load_silver_company():

    df = load_silver_company(cik="0000320193")

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 578


def test_load_silver_companies():

    df = load_silver_companies(COMPANIES)

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 2125

    assert set(df["company"].unique()) == {
        "Apple",
        "Microsoft",
        "Amazon",
        "Alphabet",
    }


def test_all_companies_have_records():

    df = load_silver_companies(COMPANIES)

    company_counts = df["company"].value_counts()

    assert company_counts["Apple"] == 578
    assert company_counts["Microsoft"] == 587
    assert company_counts["Amazon"] == 579
    assert company_counts["Alphabet"] == 381