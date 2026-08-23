import pandas as pd
from src.quality.data_quality import (deduplicate_financial_facts, )

INSTANT_CONCEPTS = ["Assets", "Liabilities", "StockholdersEquity", "CashAndCashEquivalentsAtCarryingValue", ]
PERIOD_CONCEPTS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "OperatingIncomeLoss", "NetIncomeLoss", ]

def test_instant_fact_keeps_latest_filing():

    df = pd.DataFrame({
        "company_cik": ["0000320193", "0000320193", "0000320193"],
        "concept": ["Assets", "Assets", "Assets", ],
        "start_date": [None, None, None, ],
        "end_date": pd.to_datetime(["2025-09-27", "2025-09-27", "2025-09-27", ]),
        "value": [359241000000, 359241000000, 360000000000, ],
        "filed_date": pd.to_datetime(["2025-10-31", "2026-01-30", "2026-05-01", ]), })

    result = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS, )

    assert len(result) == 1

    assert result.iloc[0]["value"] == 360000000000

    assert (result.iloc[0]["filed_date"] == pd.Timestamp("2026-05-01"))


def test_period_fact_keeps_latest_filing():

    df = pd.DataFrame({
            "company_cik": ["0000320193", "0000320193", "0000320193", ],
            "concept": ["NetIncomeLoss", "NetIncomeLoss", "NetIncomeLoss", ],
            "start_date": pd.to_datetime(["2025-01-01", "2025-01-01", "2025-01-01", ]),
            "end_date": pd.to_datetime(["2025-03-31", "2025-03-31", "2025-03-31", ]),
            "value": [24000000000, 24000000000, 25000000000, ],
            "filed_date": pd.to_datetime(["2025-05-01", "2025-08-01", "2026-02-01", ]),})

    result = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS, )

    assert len(result) == 1

    assert result.iloc[0]["value"] == 25000000000

    assert (result.iloc[0]["filed_date"] == pd.Timestamp("2026-02-01"))


def test_different_periods_are_not_deduplicated():

    df = pd.DataFrame({
            "company_cik": ["0000320193", "0000320193", ],
            "concept": ["NetIncomeLoss", "NetIncomeLoss", ],
            "start_date": pd.to_datetime(["2025-01-01", "2025-01-01", ]),
            "end_date": pd.to_datetime(["2025-03-31", "2025-06-30", ]),
            "value": [24000000000, 50000000000, ],
            "filed_date": pd.to_datetime(["2025-05-01", "2025-08-01", ]),})

    result = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS, )

    assert len(result) == 2


def test_different_concepts_are_not_deduplicated():

    df = pd.DataFrame({
            "company_cik": ["0000320193", "0000320193", ],
            "concept": ["Assets", "Liabilities", ],
            "start_date": [None, None, ],
            "end_date": pd.to_datetime(["2025-09-27", "2025-09-27", ]),
            "value": [359241000000, 285000000000, ],
            "filed_date": pd.to_datetime(["2025-10-31", "2025-10-31", ]),})

    result = deduplicate_financial_facts(df, INSTANT_CONCEPTS, PERIOD_CONCEPTS)

    assert len(result) == 2