# Irish Rental Affordability Analysis

This project analyses Irish rental market data to identify regional rent trends, county-level differences, and affordability pressure patterns.

The goal is to produce a compact data-analysis and consulting-style project using public rental data, Python, pandas, matplotlib, and clear written interpretation.

## Research Question

How have rents changed across Irish regions over time, and what do the patterns suggest about regional affordability pressure?

## Dataset

The project uses the RTB Average Monthly Rent Report dataset, downloaded from the CSO PxStat open data portal.

Focused analysis dataset:

Source: Residential Tenancies Board / CSO PxStat
Table code: RIQ02
Frequency: Quarterly
Quarter range: 2007Q4 to 2025Q4
Locations: 26 Irish counties
Bedroom filter: All bedrooms
Property type filter: All property types

The raw dataset is not committed to GitHub because it is large. The source and cleaning choices are documented in data_sources.md.

## Headline Findings

Using the county-level filtered dataset:

- Average county-level monthly rent increased from EUR 778 in 2007Q4 to EUR 1,336 in 2025Q4.
- This represents an estimated county-average increase of EUR 558, or 71.8%, across the analysed period.
- Dublin had the highest latest county average rent at EUR 2,165 per month in 2025Q4.
- Donegal had the lowest latest county average rent at EUR 1,001 per month in 2025Q4.
- Cavan showed the fastest rent growth since 2007Q4, with growth of 91.9%.
- In 2025Q4, Dublin rents were approximately 66.2% higher than the non-Dublin county average.

## Generated Outputs

The analysis script generates:

- figures/national_average_rent_trend.png
- figures/dublin_vs_non_dublin_rent_trend.png
- figures/dublin_rent_premium_over_non_dublin.png
- figures/latest_county_rents.png
- figures/top_10_latest_highest_rent_counties.png
- figures/county_rent_growth_since_2007.png
- reports/key_findings.md
- reports/executive_summary.md

## Project Structure

irish-rent-analysis/
  data/
    raw/
    cleaned/
  figures/
    county_rent_growth_since_2007.png
    dublin_rent_premium_over_non_dublin.png
    dublin_vs_non_dublin_rent_trend.png
    latest_county_rents.png
    national_average_rent_trend.png
    top_10_latest_highest_rent_counties.png
  notebooks/
  reports/
    executive_summary.md
    key_findings.md
  slides/
  src/
    clean_rent_data.py
    analyse_rent_trends.py
  tests/
    test_rent_analysis.py
  README.md
  data_sources.md
  requirements.txt

## Workflow

The project currently has two main scripts.

### 1. Clean the raw RTB dataset

Run:

python -m src.clean_rent_data

This creates:

- data/cleaned/rtb_average_monthly_rent_quarterly_cleaned.csv
- data/cleaned/rtb_county_average_rent_quarterly.csv

### 2. Analyse county-level rent trends

Run:

python -m src.analyse_rent_trends

This creates the charts and key findings report.

### 3. Run tests

Run:

python -m pytest

Current test result:

7 passed

## Tools

- Python
- pandas
- NumPy
- matplotlib
- pytest
- Jupyter Notebook
- GitHub

## Current Status

Completed:

- Repository setup
- Data source documentation
- Raw RTB rent dataset loaded locally
- Cleaning script
- County-level cleaned dataset
- Initial rent trend analysis
- Six generated charts
- Markdown key findings report
- Executive summary
- Test suite with 7 passing tests

Planned next steps:

- Add exploratory notebooks
- Write a 1-page PDF executive summary
- Create a 5-7 slide consulting deck
- Add income, inflation, and housing supply data for a fuller affordability analysis
- Add limitations and recommendations in a more polished final report

## Limitations

- The analysis uses registered tenancy data.
- Some locations have missing or suppressed values due to insufficient data.
- The current analysis focuses on county-level trends only.
- The current affordability interpretation does not include household income data.
- The analysis is descriptive and does not claim causality.
- Rent values are not adjusted for inflation in the current version.

## Disclaimer

This project is for educational and portfolio purposes. It does not provide housing policy advice, financial advice, or legal advice.
