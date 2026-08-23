import pandas as pd 

INSTANT_CONCEPTS = ["Assets", "Liabilities", "StockholdersEquity", "CashAndCashEquivalentsAtCarryingValue", ]
PERIOD_CONCEPTS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "OperatingIncomeLoss", "NetIncomeLoss", ]

def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    """
    Validate that all required columns are present in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    required_columns : list[str]
        List of columns that must exist in the DataFrame.

    Returns
    -------
    list[str]
        List containing the columns that are missing.
        Returns an empty list if all required columns are present.
    """

    # Compare the required columns against the columns
    # available in the DataFrame.
    missing_columns = [column for column in required_columns if column not in df.columns]

    return missing_columns


def validate_concepts(df: pd.DataFrame, expected_concepts: list[str]) -> list[str]:
    """
    Validate that the DataFrame only contains expected
    US GAAP financial concepts.

    Parameters
    ----------
    df : pd.DataFrame
        Financial DataFrame to validate.

    expected_concepts : list[str]
        List of financial concepts expected in the dataset.

    Returns
    -------
    list[str]
        List of concepts found in the DataFrame that were not
        included in the expected concepts.
        Returns an empty list if all concepts are valid.
    """

    # Get the concepts present in the DataFrame and compare them
    # against the expected concepts.
    # Using sets allows us to identify values that exist in the
    # DataFrame but are not part of the expected list.
    unexpected_concepts = sorted(set(df["concept"]) - set(expected_concepts))

    return unexpected_concepts


def validate_units(df: pd.DataFrame, expected_unit: str = "USD") -> list[str]:
    """
    Validate that all financial records use the expected unit.

    Parameters
    ----------
    df : pd.DataFrame
        Financial DataFrame to validate.

    expected_unit : str, optional
        Expected unit for financial values.
        Defaults to "USD".

    Returns
    -------
    list[str]
        List of unexpected units found in the DataFrame.
        Returns an empty list if all records use the expected unit.
    """

    # Get all unique units present in the DataFrame
    # and compare them against the expected unit.
    unexpected_units = sorted(set(df["unit"]) - {expected_unit})

    return unexpected_units


def validate_nulls(df: pd.DataFrame, required_columns: list[str]) -> dict[str, int]:
    """
    Validate required columns for null or missing values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    required_columns : list[str]
        Columns where null values are not expected.

    Returns
    -------
    dict[str, int]
        Dictionary containing each column with null values
        and the number of null records found.
        Returns an empty dictionary if no null values are found.
    """

    # Count the number of null values in each required column.
    null_counts = df[required_columns].isnull().sum()

    # Convert the Pandas integer values to standard Python integers
    # and keep only columns where at least one null value exists.
    return {column: int(count) for column, count in null_counts.items() if count > 0}


def find_duplicate_records(df: pd.DataFrame) -> int:
    """
    Count completely duplicated records in the DataFrame.

    A record is considered a duplicate when all of its column
    values are identical to another record.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    Returns
    -------
    int
        Number of duplicated records found.
    """

    return int(df.duplicated().sum())


def find_logical_duplicates(df: pd.DataFrame, key_columns: list[str]) -> pd.DataFrame:
    """
    Find records that share the same logical key.

    Unlike exact duplicates, logical duplicates can have different
    values in other columns while still representing the same
    business or financial record according to the selected key.

    Parameters
    ----------
    df : pd.DataFrame
        Financial DataFrame to validate.

    key_columns : list[str]
        Columns that define the logical uniqueness of a record.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all records involved in logical
        duplicates, sorted by the key columns.
    """

    # Identify every row whose combination of key columns appears
    # more than once.
    duplicated = df[df.duplicated(subset=key_columns, keep=False)].copy()

    # Sort the duplicated records by their logical key
    return duplicated.sort_values(key_columns)


def analyze_logical_duplicates(df: pd.DataFrame, key_columns: list[str], ) -> pd.DataFrame:
    """
    Analyze records that share the same logical key.

    This function helps investigate whether multiple records with
    the same logical key are legitimate SEC filings or potential
    data quality problems.

    Parameters
    ----------
    df : pd.DataFrame
        Financial DataFrame to analyze.

    key_columns : list[str]
        Columns that define the logical uniqueness of a record.

    Returns
    -------
    pd.DataFrame
        Summary of logical duplicates including:
        - Number of records sharing the key.
        - First filing date.
        - Last filing date.
        - Distinct reported values.
    """

    # Group records by the selected logical key and calculate
    # summary statistics for each group.
    analysis = (df.groupby(key_columns).agg(
        record_count=("filed_date", "size"),
        first_filed_date=("filed_date", "min"),
        last_filed_date=("filed_date", "max"),
        distinct_values=("value", "nunique"), ).reset_index())

    # Keep only keys that appear more than once.
    return analysis[analysis["record_count"] > 1].sort_values("record_count", ascending=False, )


def deduplicate_financial_facts(df: pd.DataFrame, instant_concepts: list[str], period_concepts: list[str], ) -> pd.DataFrame:

    instant_df = df[df["concept"].isin(instant_concepts)].copy()
    period_df = df[df["concept"].isin(period_concepts)].copy()

    instant_df = (instant_df.sort_values("filed_date").drop_duplicates(subset=["company_cik", "concept", "end_date", ], keep="last", ))
    period_df = (period_df.sort_values("filed_date").drop_duplicates(subset=["company_cik", "concept", "start_date", "end_date", ], keep="last", ))

    result = pd.concat([instant_df, period_df], ignore_index=True, )

    return result


def validate_data(df: pd.DataFrame) -> dict:
    """
    Run all data quality checks on the financial dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Financial DataFrame to validate.

    Returns
    -------
    dict
        Data quality report containing the result of each check.
    """

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

    expected_concepts = INSTANT_CONCEPTS + PERIOD_CONCEPTS

    missing_columns = validate_required_columns(df, required_columns, )
    unexpected_concepts = validate_concepts(df, expected_concepts, )
    unexpected_units = validate_units(df, expected_unit="USD", )
    nulls = validate_nulls(df, required_columns, )
    duplicate_records = find_duplicate_records(df)

    return {"missing_columns": missing_columns, 
            "unexpected_concepts": unexpected_concepts,
            "unexpected_units": unexpected_units,
            "critical_nulls": nulls,
            "duplicate_records": duplicate_records, 
            }


def is_quality_valid(quality_report: dict) -> bool:
    """
    Determine whether the dataset passes all critical
    data quality checks.

    Parameters
    ----------
    quality_report : dict
        Data quality report generated by validate_data().

    Returns
    -------
    bool
        True if all critical checks pass, otherwise False.
    """

    return (
        not quality_report["missing_columns"]
        and not quality_report["unexpected_concepts"]
        and not quality_report["unexpected_units"]
        and not quality_report["critical_nulls"]
        and quality_report["duplicate_records"] == 0

    )



