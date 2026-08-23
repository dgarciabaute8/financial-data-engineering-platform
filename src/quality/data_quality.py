import pandas as pd 


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    missing_columns = [column for column in required_columns if column not in df.columns]

    return missing_columns


def validate_concepts(df: pd.DataFrame, expected_concepts: list[str]) -> list[str]:
    unexpected_concepts = sorted(set(df["concept"]) - set(expected_concepts))

    return unexpected_concepts


def validate_units(df: pd.DataFrame, expected_unit: str = "USD") -> list[str]:
    unexpected_units = sorted(set(df["unit"]) - {expected_unit})

    return unexpected_units


def validate_nulls(df: pd.DataFrame, required_columns: list[str]) -> dict[str, int]:
    null_counts = df[required_columns].isnull().sum()

    return {column: int(count) for column, count in null_counts.items() if count > 0}


def find_duplicate_records(df: pd.DataFrame) -> int:

    return int(df.duplicated().sum())


def find_logical_duplicates(df: pd.DataFrame, key_columns: list[str]) -> pd.DataFrame:
    duplicated = df[df.duplicated(subset=key_columns, keep=False)].copy()

    return duplicated.sort_values(key_columns)


def analyze_logical_duplicates(df: pd.DataFrame, key_columns: list[str], ) -> pd.DataFrame:
    analysis = (df.groupby(key_columns).agg(
        record_count=("filed_date", "size"),
        first_filed_date=("filed_date", "min"),
        last_filed_date=("filed_date", "max"),
        distinct_values=("value", "unique"), ).reset_index())

    return analysis[analysis["record_count"] > 1].sort_values("record_count", ascending=False, )