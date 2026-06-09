from pathlib import Path

import pandas as pd

from src.analyse_rent_trends import (
    create_county_growth_table,
    create_dublin_premium_table,
    create_dublin_vs_non_dublin,
    create_latest_county_snapshot,
    create_national_quarterly_average,
    create_top_latest_counties,
)


def sample_county_data() -> pd.DataFrame:
    data = pd.DataFrame(
        {
            "quarter": [
                "2020Q1",
                "2020Q1",
                "2020Q1",
                "2020Q2",
                "2020Q2",
                "2020Q2",
            ],
            "period": pd.PeriodIndex(
                ["2020Q1", "2020Q1", "2020Q1", "2020Q2", "2020Q2", "2020Q2"],
                freq="Q",
            ),
            "period_start": pd.PeriodIndex(
                ["2020Q1", "2020Q1", "2020Q1", "2020Q2", "2020Q2", "2020Q2"],
                freq="Q",
            ).to_timestamp(),
            "location": [
                "Dublin",
                "Cork",
                "Galway",
                "Dublin",
                "Cork",
                "Galway",
            ],
            "rent_eur": [2000.0, 1200.0, 1000.0, 2200.0, 1300.0, 1100.0],
        }
    )

    return data


def test_create_national_quarterly_average() -> None:
    df = sample_county_data()

    national = create_national_quarterly_average(df)

    assert len(national) == 2
    assert national.loc[0, "average_rent_eur"] == 1400.0
    assert national.loc[1, "average_rent_eur"] == 1533.3333333333333


def test_create_dublin_vs_non_dublin() -> None:
    df = sample_county_data()

    comparison = create_dublin_vs_non_dublin(df)

    assert set(comparison["region_group"]) == {"Dublin", "Non-Dublin average"}

    latest = comparison[comparison["period"] == pd.Period("2020Q2")]
    dublin_value = latest[latest["region_group"] == "Dublin"]["average_rent_eur"].iloc[0]
    non_dublin_value = latest[
        latest["region_group"] == "Non-Dublin average"
    ]["average_rent_eur"].iloc[0]

    assert dublin_value == 2200.0
    assert non_dublin_value == 1200.0


def test_create_dublin_premium_table() -> None:
    df = sample_county_data()
    comparison = create_dublin_vs_non_dublin(df)

    premium = create_dublin_premium_table(comparison)

    latest = premium[premium["period"] == pd.Period("2020Q2")].iloc[0]

    assert latest["dublin_premium_eur"] == 1000.0
    assert round(latest["dublin_premium_percent"], 2) == 83.33


def test_create_latest_county_snapshot() -> None:
    df = sample_county_data()

    latest = create_latest_county_snapshot(df)

    assert len(latest) == 3
    assert latest.iloc[0]["location"] == "Dublin"
    assert latest.iloc[0]["rent_eur"] == 2200.0


def test_create_top_latest_counties() -> None:
    df = sample_county_data()
    latest = create_latest_county_snapshot(df)

    top_latest = create_top_latest_counties(latest, top_n=2)

    assert len(top_latest) == 2
    assert list(top_latest["location"]) == ["Dublin", "Cork"]


def test_create_county_growth_table() -> None:
    df = sample_county_data()

    growth = create_county_growth_table(df)

    dublin = growth[growth["location"] == "Dublin"].iloc[0]

    assert dublin["first_rent_eur"] == 2000.0
    assert dublin["latest_rent_eur"] == 2200.0
    assert dublin["absolute_growth_eur"] == 200.0
    assert dublin["percentage_growth"] == 10.0


def test_expected_project_files_exist() -> None:
    assert Path("src/clean_rent_data.py").exists()
    assert Path("src/analyse_rent_trends.py").exists()
    assert Path("README.md").exists()
    assert Path("data_sources.md").exists()
