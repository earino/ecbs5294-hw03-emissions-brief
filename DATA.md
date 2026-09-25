# Data in this repository

Everything under `data/raw/` is real, public data, committed on purpose and **never edited**. Where it came from, its license, and exactly what was changed for this course:

## EU-27 country codes across three sources

**Made for this course.** The 27 EU member states (as of 2020), one row each: the code Eurostat uses (`geo`,
which is ISO 3166-1 alpha-2 except Greece, `EL`), the ISO 3166-1 alpha-3 code Our World in Data uses
(`iso_code`), the World Bank's country `id`, and the English name. Written by hand from the three sources' own
documentation; checked by `check_values.py` in HW3's solution against every source. **License:** CC BY 4.0,
as the course materials.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `country_codes.csv` | 550 | `939e982ec15ae39c…` |

## Eurostat — municipal waste (env_wasmun) and greenhouse-gas emissions (env_air_gge)

**Source:** Eurostat, dissemination API (SDMX 2.1, TSV). Municipal waste by waste management operations,
`env_wasmun`: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/env_wasmun/?format=TSV&compressed=false&startPeriod=2010` (fetched 2026-09-19, SHA-256 `efe7d4fa295909d0…`). Greenhouse gas emissions by source sector, `env_air_gge`:
retrieved through Eurostat's asynchronous extraction of the full dataset from 2010 (the synchronous request for a
file this size is queued by Eurostat, and the old bulk-download URL is retired). Code lists for the dimensions
and the observation flags: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/<LIST>?format=TSV`.

**License:** Eurostat data are reusable under **CC BY 4.0** (Eurostat copyright and reuse policy). Attribution:
*Source: Eurostat, env_wasmun / env_air_gge*, © European Union.

**Changes made for this course:** `env_wasmun.tsv` is unmodified. `env_air_gge_ghg.tsv` keeps only the rows whose
pollutant is `GHG` (all greenhouse gases in CO₂ equivalent), in both units, every source sector, every country;
the header line and every kept row are byte-for-byte as Eurostat published them. The four `codelist_*.tsv` files
are Eurostat's labels for the codes, unmodified.

**How to read the raw files:** the first column packs several dimensions separated by commas (its header says
which, e.g. `freq,unit,airpol,src_crf,geo\TIME_PERIOD`); each year is a column; a value may carry a flag after a
space (`628 e`); `:` means not available and may itself carry a flag (`: m`). Flag meanings: `codelist_obs_flag.tsv`.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `codelist_obs_flag.tsv` | 2,417 | `5631f76c7c9b8e00…` |
| `codelist_src_crf.tsv` | 7,516 | `085697dd09782f1a…` |
| `env_air_gge_ghg.tsv` | 1,355,639 | `e4d0fe960b1c4b13…` |

## Our World in Data — CO₂ and greenhouse-gas emissions

**Source:** Our World in Data, *CO₂ and Greenhouse Gas Emissions* dataset, https://github.com/owid/co2-data —
data file `https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv` (fetched 2026-09-19, SHA-256 `7f78e2b218ce4bb8…`); codebook `https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv` (fetched 2026-09-19, SHA-256 `33b4f5e00efd58c7…`).

**Authors:** Pablo Rosado, Hannah Ritchie, Max Roser, Edouard Mathieu, Bobbie Macdonald (Our World in Data).

**License:** Our World in Data's own work is licensed **CC BY 4.0**. Each underlying series keeps the terms of
its original source, named per column in `owid_codebook.csv` (the `source` column): the CO₂ series come from the
Global Carbon Budget (CC BY 4.0); the greenhouse-gas totals from Jones et al., *National contributions to climate
change* (CC BY 4.0); population and GDP from the sources OWID lists. Cite OWID and the named source when reusing.

**Changes made for this course:** a subset of 15 of the file's columns; years 1990 onward; rows sorted by
country and year. `countries.csv` is a further subset: only the rows that are countries, kept by the filter Lab 1 builds (the
file's aggregate rows — `World`, the continents, the income groups and the like — are gone). No values were edited.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `owid_co2.csv` | 790,518 | `8af6dcc277a5b174…` |
| `owid_codebook.csv` | 3,478 | `f74086edb7064dcd…` |

## World Bank — World Development Indicators API, cached pages

**Source:** World Bank Indicators API v2 (https://api.worldbank.org/v2). Requests:
`/country/all/indicator/SP.POP.TOTL?format=json&date=2010:2024&per_page=1000&page=N` (population) and the same
for `NY.GDP.MKTP.PP.KD` (GDP, PPP, constant 2021 international dollars), pages 1 to 4 each; and
`/country?format=json&per_page=400&page=1`, the country metadata. First page: `https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2010:2024&per_page=1000&page=1` (fetched 2026-09-19, SHA-256 `706c1f6ed0f69fb8…`).

**Response shape:** every file is a two-element JSON array. Element 0 is metadata (`page`, `pages`, `per_page`,
`total`). Element 1 is the records. **Each file is one page**: page 1 holds 1,000 of the 3,975 records. The
metadata file's `region` field is `"Aggregates"` for rows that are groups of countries (`WLD`, `EUU`, income
groups), not countries.

**License:** **CC BY 4.0**. Attribution: *World Bank, World Development Indicators*.

**Changes made for this course:** none. Each file is one API response exactly as received.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `NY.GDP.MKTP.PP.KD_page1.json` | 246,180 | `ac1f903c97821cda…` |
| `NY.GDP.MKTP.PP.KD_page2.json` | 233,836 | `8d79d86879dc0aff…` |
| `NY.GDP.MKTP.PP.KD_page3.json` | 233,851 | `1d6b69a4156776b2…` |
| `NY.GDP.MKTP.PP.KD_page4.json` | 230,626 | `b1c3af3d12bf8fc0…` |
| `SP.POP.TOTL_page1.json` | 210,269 | `706c1f6ed0f69fb8…` |
| `SP.POP.TOTL_page2.json` | 197,327 | `649de57d4a1ebad7…` |
| `SP.POP.TOTL_page3.json` | 197,141 | `4039e5bf43ba298e…` |
| `SP.POP.TOTL_page4.json` | 194,617 | `542c48f24a13b6c2…` |
| `country_page1.json` | 113,590 | `d29d57f8adf954c5…` |
