# Data dictionary — silver

One section per silver table. A skeptical reader uses this page to check your gold table without reading your code:
for every column, what it holds, in what unit, which values it may take, what a missing value means, and what your
cleaner did to get it there. Fill in every cell; "n/a" is an answer, an empty cell is not. Where a trap in `DIAGNOSIS.md`
explains a column, write *see Trap N* instead of repeating its evidence.

## `silver.eurostat` — `data/silver/eurostat.parquet`

**One row is:** …  **Key:** …  **Rows:** …  **Made by:** `scripts/clean_eurostat.py` from `data/raw/env_air_gge_ghg.tsv`

| Column | Type | Meaning | Unit | Allowed values | Missing means | What was done to it |
|---|---|---|---|---|---|---|
| `geo` | | | | | | |
| `year` | | | | | | |
| `src_crf` | | | | | | |
| `ghg_mt` | | | | | | |
| `flag` | | | | | | |
| `is_aggregate` | | | | | | |

## `silver.owid` — `data/silver/owid.parquet`

**One row is:** …  **Key:** …  **Rows:** …  **Made by:** `scripts/clean_owid.py` from `data/raw/owid_co2.csv`

| Column | Type | Meaning | Unit | Allowed values | Missing means | What was done to it |
|---|---|---|---|---|---|---|
| `iso3` | | | | | | |
| `country` | | | | | | |
| `year` | | | | | | |
| `ghg_excl_lucf_mt` | | | | | | |
| *any other column you keep* | | | | | | |

## `silver.worldbank` — `data/silver/worldbank.parquet`

**One row is:** …  **Key:** …  **Rows:** …  **Made by:** `scripts/clean_worldbank.py` from `data/raw/api/worldbank/`

| Column | Type | Meaning | Unit | Allowed values | Missing means | What was done to it |
|---|---|---|---|---|---|---|
| `iso3` | | | | | | |
| `year` | | | | | | |
| `indicator` | | | | | | |
| `value` | | | | | | |
| `is_aggregate` | | | | | | |
| `page` | | | | | | |

## `silver.worldbank_page_counts` — `data/silver/worldbank_page_counts.csv` (supplied: check it against your table)

**One row is:** one page of one indicator's API response — the parent the records came from. **Key:** `(indicator,
page)`. **Rows:** one per page read; 8 on the course's files. **Made by:** `scripts/clean_worldbank.py`, from each
page's metadata and the child table of records.

| Column | Type | Meaning | Unit | Allowed values | Missing means | What was done to it |
|---|---|---|---|---|---|---|
| `indicator` | VARCHAR | the World Bank indicator the page belongs to | — | `SP.POP.TOTL`, `NY.GDP.MKTP.PP.KD` | never missing | from the page |
| `page` | INTEGER | the page's number | — | 1 to the metadata's `pages` | never missing | the metadata's `page` |
| `records_expected` | INTEGER | the records the page's metadata promises | records | `per_page`; on the last page, what is left of `total` | never missing | `least(per_page, total - per_page * (page - 1))` |
| `records_read` | INTEGER | the records of the child table that carry this page | records | 0 to `per_page` | never missing | counted with `GROUP BY` on the page each record carries |

## The rejects files — `data/silver/rejects_<source>.csv`

What one row is, and every `reason` your cleaners can write:

| Source | Reason | Destination | How many on the course's raw files |
|---|---|---|---|
| | | | |
