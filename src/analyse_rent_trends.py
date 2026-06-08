"""
Analyse Irish county-level rent trends.

This script uses the cleaned county-level RTB rent dataset and generates:
- headline summary metrics
- rent trend charts
- regional comparison charts
- a Markdown key findings report
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


COUNTY_DATA_PATH = Path("data/cleaned/rtb_county_average_rent_quarterly.csv")
FIGURES_DIR = Path("figures")
REPORTS_DIR = Path("reports")
KEY_FINDINGS_PATH = REPORTS_DIR / "key_findings.md"


def ensure_output_dirs() -> None:
    """
    Ensure output folders exist.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_county_rent_data(path: Path = COUNTY_DATA_PATH) -> pd.DataFrame:
    """
    Load the cleaned county-level rent dataset.
    """
    df = pd.read_csv(path)
    df["period"] = pd.PeriodIndex(df["period"], freq="Q")
    df["period_start"] = df["period"].dt.to_timestamp()

    return df


def create_national_quarterly_average(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the average county rent by quarter.
    """
    national = (
        df.groupby(["period", "period_start"], as_index=False)["rent_eur"]
        .mean()
        .rename(columns={"rent_eur": "average_rent_eur"})
    )

    return national


def create_dublin_vs_non_dublin(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Dublin versus non-Dublin average rent by quarter.
    """
    comparison = df.copy()
    comparison["region_group"] = comparison["location"].apply(
        lambda location: "Dublin" if location == "Dublin" else "Non-Dublin average"
    )

    grouped = (
        comparison.groupby(["period", "period_start", "region_group"], as_index=False)[
            "rent_eur"
        ]
        .mean()
        .rename(columns={"rent_eur": "average_rent_eur"})
    )

    return grouped


def create_dublin_premium_table(comparison: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Dublin's rent premium over the non-Dublin average by quarter.
    """
    wide = comparison.pivot(
        index=["period", "period_start"],
        columns="region_group",
        values="average_rent_eur",
    ).reset_index()

    wide["dublin_premium_eur"] = wide["Dublin"] - wide["Non-Dublin average"]
    wide["dublin_premium_percent"] = (
        wide["dublin_premium_eur"] / wide["Non-Dublin average"]
    ) * 100

    return wide


def create_top_latest_counties(latest: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the highest-rent counties in the latest quarter.
    """
    return latest.head(top_n).copy()


def create_latest_county_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return latest available county rent values.
    """
    latest_period = df["period"].max()

    latest = (
        df[df["period"] == latest_period]
        .sort_values("rent_eur", ascending=False)
        .reset_index(drop=True)
    )

    return latest


def create_county_growth_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate rent growth from first available quarter to latest quarter by county.
    """
    first_period = df["period"].min()
    latest_period = df["period"].max()

    first = df[df["period"] == first_period][["location", "rent_eur"]].rename(
        columns={"rent_eur": "first_rent_eur"}
    )
    latest = df[df["period"] == latest_period][["location", "rent_eur"]].rename(
        columns={"rent_eur": "latest_rent_eur"}
    )

    growth = first.merge(latest, on="location", how="inner")
    growth["absolute_growth_eur"] = growth["latest_rent_eur"] - growth["first_rent_eur"]
    growth["percentage_growth"] = (
        growth["absolute_growth_eur"] / growth["first_rent_eur"]
    ) * 100

    growth = growth.sort_values("percentage_growth", ascending=False).reset_index(
        drop=True
    )

    return growth


def save_national_average_chart(national: pd.DataFrame) -> Path:
    """
    Save national average rent trend chart.
    """
    output_path = FIGURES_DIR / "national_average_rent_trend.png"

    plt.figure(figsize=(10, 6))
    plt.plot(national["period_start"], national["average_rent_eur"])
    plt.title("Average Monthly Rent Across Irish Counties")
    plt.xlabel("Quarter")
    plt.ylabel("Average monthly rent (EUR)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def save_dublin_vs_non_dublin_chart(comparison: pd.DataFrame) -> Path:
    """
    Save Dublin versus non-Dublin rent trend chart.
    """
    output_path = FIGURES_DIR / "dublin_vs_non_dublin_rent_trend.png"

    plt.figure(figsize=(10, 6))

    for region_group, group in comparison.groupby("region_group"):
        plt.plot(group["period_start"], group["average_rent_eur"], label=region_group)

    plt.title("Dublin vs Non-Dublin Average Monthly Rent")
    plt.xlabel("Quarter")
    plt.ylabel("Average monthly rent (EUR)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def save_dublin_premium_chart(premium: pd.DataFrame) -> Path:
    """
    Save Dublin rent premium over non-Dublin average chart.
    """
    output_path = FIGURES_DIR / "dublin_rent_premium_over_non_dublin.png"

    plt.figure(figsize=(10, 6))
    plt.plot(premium["period_start"], premium["dublin_premium_percent"])
    plt.title("Dublin Rent Premium over Non-Dublin Average")
    plt.xlabel("Quarter")
    plt.ylabel("Premium (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def save_top_latest_counties_chart(top_latest: pd.DataFrame) -> Path:
    """
    Save top 10 highest-rent counties chart.
    """
    output_path = FIGURES_DIR / "top_10_latest_highest_rent_counties.png"

    plot_data = top_latest.sort_values("rent_eur", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(plot_data["location"], plot_data["rent_eur"])
    plt.title(f"Top 10 Highest County Rents ({top_latest['quarter'].iloc[0]})")
    plt.xlabel("Average monthly rent (EUR)")
    plt.ylabel("County")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def save_latest_county_rents_chart(latest: pd.DataFrame) -> Path:
    """
    Save latest county rent bar chart.
    """
    output_path = FIGURES_DIR / "latest_county_rents.png"

    plot_data = latest.sort_values("rent_eur", ascending=True)

    plt.figure(figsize=(10, 8))
    plt.barh(plot_data["location"], plot_data["rent_eur"])
    plt.title(f"Latest County Average Monthly Rent ({latest['quarter'].iloc[0]})")
    plt.xlabel("Average monthly rent (EUR)")
    plt.ylabel("County")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def save_county_growth_chart(growth: pd.DataFrame) -> Path:
    """
    Save county percentage rent growth chart.
    """
    output_path = FIGURES_DIR / "county_rent_growth_since_2007.png"

    plot_data = growth.sort_values("percentage_growth", ascending=True)

    plt.figure(figsize=(10, 8))
    plt.barh(plot_data["location"], plot_data["percentage_growth"])
    plt.title("County Rent Growth from 2007Q4 to 2025Q4")
    plt.xlabel("Rent growth (%)")
    plt.ylabel("County")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def format_euro(value: float) -> str:
    """
    Format euro values.
    """
    return f"EUR {value:,.0f}"


def format_percent(value: float) -> str:
    """
    Format percentages.
    """
    return f"{value:.1f}%"


def create_key_findings_report(
    national: pd.DataFrame,
    latest: pd.DataFrame,
    growth: pd.DataFrame,
    chart_paths: list[Path],
) -> str:
    """
    Create a Markdown key findings report.
    """
    first_national = national.iloc[0]
    latest_national = national.iloc[-1]

    national_absolute_growth = (
        latest_national["average_rent_eur"] - first_national["average_rent_eur"]
    )
    national_percentage_growth = (
        national_absolute_growth / first_national["average_rent_eur"]
    ) * 100

    highest_latest = latest.iloc[0]
    lowest_latest = latest.iloc[-1]

    fastest_growth = growth.iloc[0]
    slowest_growth = growth.iloc[-1]

    chart_section = "\n".join(f"- `{path}`" for path in chart_paths)

    report = f"""# Irish Rental Affordability Analysis - Key Findings

## Dataset

This analysis uses the RTB Average Monthly Rent Report county-level quarterly dataset.

Focused dataset:

```text
Locations: 26 Irish counties
Quarter range: 2007Q4 to 2025Q4
Bedroom filter: All bedrooms
Property type filter: All property types
```

## Headline Findings

1. The average county-level monthly rent increased from {format_euro(first_national["average_rent_eur"])} in {first_national["period"]} to {format_euro(latest_national["average_rent_eur"])} in {latest_national["period"]}.

2. This represents an estimated national county-average increase of {format_euro(national_absolute_growth)}, or {format_percent(national_percentage_growth)}, across the analysed period.

3. The highest latest county average rent is {highest_latest["location"]} at {format_euro(highest_latest["rent_eur"])} per month in {highest_latest["quarter"]}.

4. The lowest latest county average rent is {lowest_latest["location"]} at {format_euro(lowest_latest["rent_eur"])} per month in {lowest_latest["quarter"]}.

5. The fastest rent growth since 2007Q4 is observed in {fastest_growth["location"]}, with growth of {format_percent(fastest_growth["percentage_growth"])}.

6. The slowest rent growth since 2007Q4 is observed in {slowest_growth["location"]}, with growth of {format_percent(slowest_growth["percentage_growth"])}.

## Charts Generated

{chart_section}

## Interpretation

The results suggest that Irish rent pressure has increased substantially over the analysed period. Dublin remains a high-rent market, but the county-level growth results also show that rent pressure is not limited to Dublin alone.

The analysis should be interpreted as a rent-trend study, not a full affordability study. A complete affordability analysis would require household income, disposable income, household composition, and local supply data.

## Limitations

- The analysis uses registered tenancy data.
- Missing or suppressed observations may affect some local comparisons.
- The current headline analysis uses county-level data only.
- The current affordability interpretation does not include income data.
- The analysis is descriptive and does not claim causality.
"""

    return report


def save_key_findings_report(report: str) -> Path:
    """
    Save the key findings report.
    """
    KEY_FINDINGS_PATH.write_text(report, encoding="utf-8")

    return KEY_FINDINGS_PATH


def run_analysis() -> dict[str, object]:
    """
    Run the full rent trend analysis.
    """
    ensure_output_dirs()

    county_data = load_county_rent_data()
    national = create_national_quarterly_average(county_data)
    comparison = create_dublin_vs_non_dublin(county_data)
    latest = create_latest_county_snapshot(county_data)
    growth = create_county_growth_table(county_data)
    premium = create_dublin_premium_table(comparison)
    top_latest = create_top_latest_counties(latest)

    chart_paths = [
        save_national_average_chart(national),
        save_dublin_vs_non_dublin_chart(comparison),
        save_dublin_premium_chart(premium),
        save_latest_county_rents_chart(latest),
        save_top_latest_counties_chart(top_latest),
        save_county_growth_chart(growth),
    ]

    report = create_key_findings_report(
        national=national,
        latest=latest,
        growth=growth,
        chart_paths=chart_paths,
    )
    report_path = save_key_findings_report(report)

    return {
        "county_data": county_data,
        "national": national,
        "dublin_vs_non_dublin": comparison,
        "latest": latest,
        "growth": growth,
        "dublin_premium": premium,
        "top_latest": top_latest,
        "chart_paths": chart_paths,
        "report_path": report_path,
    }


if __name__ == "__main__":
    outputs = run_analysis()

    print("Analysis complete.")
    print(f"Key findings report saved to: {outputs['report_path']}")
    print("Charts saved:")
    for chart_path in outputs["chart_paths"]:
        print(f"- {chart_path}")

    print("\nLatest county rents:")
    print(outputs["latest"][["location", "quarter", "rent_eur"]].head(10))

    print("\nTop 10 latest highest-rent counties:")
    print(outputs["top_latest"][["location", "quarter", "rent_eur"]])

    print("\nLatest Dublin rent premium:")
    print(
        outputs["dublin_premium"][
            ["period", "Dublin", "Non-Dublin average", "dublin_premium_percent"]
        ].tail(1)
    )

    print("\nFastest percentage growth:")
    print(
        outputs["growth"][
            ["location", "first_rent_eur", "latest_rent_eur", "percentage_growth"]
        ].head(10)
    )
