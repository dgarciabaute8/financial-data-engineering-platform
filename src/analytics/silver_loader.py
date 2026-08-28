from pathlib import Path 

import pandas as pd

def load_silver_company(cik: str, input_dir: str = "data/processed/silver",) -> pd.DataFrame:
    """
    Load a company's Silver financial dataset from Parquet.

    Parameters
    ----------
    cik : str
        SEC Central Index Key of the company.

    input_dir : str
        Directory containing Silver Parquet files.

    Returns
    -------
    pd.DataFrame
        Financial facts for the requested company.
    """

    input_path = Path(input_dir)

    file_path = input_path / f"companyfacts_{cik}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver dataset not found: {file_path}")

    return pd.read_parquet(file_path)


def load_silver_companies(companies: dict[str, str], input_dir: str = "data/processed/silver",) -> pd.DataFrame:
    """
    Load and combine Silver datasets for multiple companies.

    Parameters
    ----------
    companies : dict[str, str]
        Mapping between company name and SEC CIK.

    input_dir : str
        Directory containing Silver Parquet files.

    Returns
    -------
    pd.DataFrame
        Combined financial dataset for all companies.
    """

    dataframes = []

    for company_name, cik in companies.items():
        df = load_silver_company(cik=cik, input_dir=input_dir,)

        df = df.copy()

        df["company"] = company_name
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True,)