import pandas as pd 

CONCEPT_COLUMN_MAPPING = {
    "Assets": "assets",
    "Liabilities": "liabilities",
    "StockholdersEquity": "equity",
    "CashAndCashEquivalentsAtCarryingValue": "cash",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "revenue",
    "OperatingIncomeLoss": "operating_income",
    "NetIncomeLoss": "net_income",
}

def build_gold_financial_statements(silver_df: pd.DataFrame,) -> pd.DataFrame:
    """
    Transform the Silver financial facts dataset into a
    company-level financial statements dataset.

    Parameters
    ----------
    silver_df : pd.DataFrame
        Combined Silver financial dataset.

    Returns
    -------
    pd.DataFrame
        Gold financial statements dataset.
    """

    df = silver_df.copy()

    # Keep only the financial concepts required
    # for the Gold financial statements dataset.
    df = df[df["concept"].isin(CONCEPT_COLUMN_MAPPING)].copy()

    # Map SEC concept names to business-friendly column names.
    df["financial_metric"] = df["concept"].map(CONCEPT_COLUMN_MAPPING)

    # Use fiscal year as the reporting period.
    df["period"] = df["fiscal_year"].astype("Int64")

    # Convert the long-format financial facts into
    # a wide analytical structure.
    gold_df = df.pivot_table(index=["company", "period",], columns="financial_metric", values="value", aggfunc="first",).reset_index()

    # Remove the column index created by pivot_table.
    gold_df.columns.name = None

    return gold_df



