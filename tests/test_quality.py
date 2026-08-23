import pandas as pd

from src.quality.data_quality import (validate_required_columns, validate_concepts, validate_units, validate_nulls, find_duplicate_records, )


def create_valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "company_cik": ["0000320193", "0000320193"],
            "entity_name": ["Apple Inc.", "Apple Inc."],
            "concept": ["Assets", "Liabilities"],
            "unit": ["USD", "USD"],
            "end_date": pd.to_datetime(["2025-09-27", "2025-09-27"]),
            "value": [359241000000, 285000000000],
            "form": ["10-K", "10-K"],
            "accession_number": ["0001", "0002"],
            "filed_date": pd.to_datetime(["2025-10-31", "2025-10-31"]),
        })


def test_required_columns_are_present():

    df = create_valid_dataframe()

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

    result = validate_required_columns(df, required_columns, )

    assert result == []


def test_concepts_are_valid():

    df = create_valid_dataframe()

    expected_concepts = [
        "Assets",
        "Liabilities",
    ]

    result = validate_concepts(df, expected_concepts, )

    assert result == []


def test_units_are_valid():

    df = create_valid_dataframe()

    result = validate_units(df, expected_unit="USD", )

    assert result == []


def test_required_columns_have_no_nulls():

    df = create_valid_dataframe()

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

    result = validate_nulls(df, required_columns, )

    assert result == {}


def test_dataframe_has_no_duplicate_records():

    df = create_valid_dataframe()

    result = find_duplicate_records(df)

    assert result == 0


def test_unexpected_unit_is_detected():

    df = create_valid_dataframe()

    df.loc[0, "unit"] = "EUR"

    result = validate_units(df, expected_unit="USD", )

    assert result == ["EUR"]


def test_missing_required_column_is_detected():

    df = create_valid_dataframe()

    df = df.drop(columns=["value"])

    result = validate_required_columns(df, ["company_cik", "concept", "value"], )

    assert result == ["value"]


def test_required_null_is_detected():

    df = create_valid_dataframe()

    df.loc[0, "value"] = None

    result = validate_nulls(df, ["company_cik", "concept", "value"], )

    assert result == {"value": 1}
