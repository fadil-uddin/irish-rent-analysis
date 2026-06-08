# Data Sources

## Primary Source: RTB Average Monthly Rent Report

Source: Residential Tenancies Board, hosted through the CSO PxStat open data portal.

Dataset used:

```text
RTB Average Monthly Rent Report
Table code: RIQ02
Frequency: Quarterly
Downloaded file name: rtb_average_monthly_rent_quarterly.csv
```

Purpose:

Analyse Irish rent trends across locations, quarters, bedroom categories, and property types.

Variables used:

```text
STATISTIC Label
Quarter
Number of Bedrooms
Property Type
Location
UNIT
VALUE
```

Project cleaning choices:

- Renamed raw columns into snake_case.
- Converted `VALUE` into numeric `rent_eur`.
- Created `year`, `quarter_number`, and `period` columns.
- Created a focused county-level dataset using:
  - `Number of Bedrooms = All bedrooms`
  - `Property Type = All property types`
  - county-level locations only
  - non-missing rent values only

Cleaned outputs generated locally:

```text
data/cleaned/rtb_average_monthly_rent_quarterly_cleaned.csv
data/cleaned/rtb_county_average_rent_quarterly.csv
```

Download date:

```text
8 June 2026
```

Coverage:

```text
Quarter range: 2007Q4 to 2025Q4
County-level locations: 26
County-level rows after filtering: 1,898
```

Dataset limitations:

- Coverage depends on registered tenancies.
- Some locations have missing or suppressed values due to insufficient data.
- Rent values describe recorded tenancy data and should not be interpreted as full affordability measures without income data.
- The county-level analysis intentionally removes towns and smaller local areas for a cleaner first version.
- The project does not claim causality.