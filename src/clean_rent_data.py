"""
Clean RTB average monthly rent data for analysis.

This script reads the raw quarterly RTB rent dataset, standardises column names,
creates useful time variables, filters to the broad all-bedroom/all-property
view, and saves a cleaned CSV for analysis.
"""

from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/rtb_average_monthly_rent_quarterly.csv")
CLEANED_DATA_DIR = Path("data/cleaned")
CLEANED_DATA_PATH = CLEANED_DATA_DIR / "rtb_average_monthly_rent_quarterly_cleaned.csv"
COUNTY_DATA_PATH = CLEANED_DATA_DIR / "rtb_county_average_rent_quarterly.csv"


IRISH_COUNTIES = {
    "Carlow",
    "Cavan",
    "Clare",
    "Cork",
    "Donegal",
    "Dublin",
    "Galway",
    "Kerry",
    "Kildare",
    "Kilkenny",
    "Laois",
    "Leitrim",
    "Limerick",
    "Longford",
    "Louth",
    "Mayo",
    "Meath",
    "Monaghan",
    "Offaly",
    "Roscommon",
    "Sligo",
    "Tipperary",
    "Waterford",
    "Westmeath",
    "Wexford",
    "Wicklow",
}


def standardise_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise raw column names to snake_case.
    """
    renamed = df.rename(
        columns={
            "STATISTIC Label": "statistic",
            "Quarter": "quarter",
            "Number of Bedrooms": "bedrooms",
            "Property Type": "property_type",
            "Location": "location",
            "UNIT": "unit",
            "VALUE": "rent_eur",
        }
    )

    return renamed


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add year, quarter number, and ordered period columns.
    """
    cleaned = df.copy()

    cleaned["year"] = cleaned["quarter"].str[:4].astype(int)
    cleaned["quarter_number"] = cleaned["quarter"].str[-1].astype(int)
    cleaned["period"] = pd.PeriodIndex(cleaned["quarter"], freq="Q")

    return cleaned


def clean_rent_data(raw_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load and clean the raw rent dataset.
    """
    df = pd.read_csv(raw_path)

    cleaned = standardise_column_names(df)
    cleaned = add_time_columns(cleaned)

    cleaned["rent_eur"] = pd.to_numeric(cleaned["rent_eur"], errors="coerce")

    cleaned = cleaned.sort_values(
        ["location", "property_type", "bedrooms", "period"]
    ).reset_index(drop=True)

    return cleaned


def create_county_level_dataset(cleaned: pd.DataFrame) -> pd.DataFrame:
    """
    Create a focused county-level dataset for headline analysis.

    This keeps:
    - county-level locations only
    - all bedrooms
    - all property types
    - non-missing rent values
    """
    county_data = cleaned[
        (cleaned["location"].isin(IRISH_COUNTIES))
        & (cleaned["bedrooms"] == "All bedrooms")
        & (cleaned["property_type"] == "All property types")
        & (cleaned["rent_eur"].notna())
    ].copy()

    county_data = county_data.sort_values(["location", "period"]).reset_index(
        drop=True
    )

    return county_data


def save_cleaned_data(
    cleaned: pd.DataFrame,
    county_data: pd.DataFrame,
    output_dir: Path = CLEANED_DATA_DIR,
) -> tuple[Path, Path]:
    """
    Save cleaned full and county-level datasets.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(CLEANED_DATA_PATH, index=False)
    county_data.to_csv(COUNTY_DATA_PATH, index=False)

    return CLEANED_DATA_PATH, COUNTY_DATA_PATH


if __name__ == "__main__":
    cleaned_data = clean_rent_data()
    county_level_data = create_county_level_dataset(cleaned_data)

    cleaned_path, county_path = save_cleaned_data(
        cleaned=cleaned_data,
        county_data=county_level_data,
    )

    print(f"Saved cleaned data to: {cleaned_path}")
    print(f"Saved county-level data to: {county_path}")

    print("\nCleaned dataset shape:")
    print(cleaned_data.shape)

    print("\nCounty-level dataset shape:")
    print(county_level_data.shape)

    print("\nCounty-level preview:")
    print(county_level_data.head())