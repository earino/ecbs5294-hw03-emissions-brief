"""The brief's analytical contract, as constants. SUPPLIED: do not edit.

Every decision here is the ministry's, not yours (README, "The analytical contract"). Import what you need:

    from scripts.contract import RAW, SILVER, UNIT, SECTORS, TOTAL, FIRST_YEAR, FINAL_YEAR

The harness that grades your checks finds your silver tables by the names in SILVER, so keep them.
"""

# ---- the question ------------------------------------------------------------------------------------------------
GAS = "GHG"                    # Eurostat airpol: all greenhouse gases, in CO2 equivalent
UNIT = "MIO_T"                 # Eurostat unit: million tonnes (the file also carries THS_T, thousand tonnes)
SECTORS = {                    # Eurostat src_crf: the six source sectors, which do not overlap ...
    "CRF1": "Energy",
    "CRF2": "Industrial processes and product use",
    "CRF3": "Agriculture",
    "CRF5": "Waste management",
    "CRF6": "Other sectors",
    "CRF_INDCO2": "Indirect CO2",
}
TOTAL = "TOTX4_MEMO"           # ... and the national total they add up to: excluding LULUCF and memo items
TOTAL_LABEL = "Total (excluding LULUCF and memo items)"
CODES = (*SECTORS, TOTAL)      # the seven src_crf codes in scope

FIRST_YEAR = 2010
FINAL_YEAR = 2024              # the latest year all three sources have for all 27 countries

EU_AGGREGATE_EUROSTAT = "EU27_2020"   # Eurostat's own EU-27 row: kept in silver, is_aggregate = true
EU_AGGREGATE_WORLDBANK = "EUU"        # the World Bank's "European Union": kept in silver, is_aggregate = true

INDICATORS = {                 # World Bank indicator id -> what it is
    "SP.POP.TOTL": "population (persons)",
    "NY.GDP.MKTP.PP.KD": "GDP, PPP (constant 2021 international $)",
}

# ---- domain rules: an observation inside the scope that breaks one is QUARANTINED (rejects file, with a reason) --
WINDOWS = {                    # the years each raw file can hold; a year outside its window is impossible data
    "owid": (1990, 2024),
    "eurostat": (2010, 2024),
    "worldbank": (2010, 2024),
}
# emissions >= 0 (in this file, negative values occur only outside the seven codes: in land use and the total that
# includes it, and in two memo items on long-term carbon storage); population > 0; GDP > 0.

# ---- reconciliation tolerances, from the source's rounding (MIO_T is published to 5 decimals = 0.00001 Mt) -------
TOLERANCE_SECTORS_MT = 0.0001  # six sectors vs TOTX4_MEMO: seven rounded numbers
TOLERANCE_EU27_MT = 0.0005     # 27 members vs EU27_2020: twenty-eight rounded numbers

# ---- where things are ------------------------------------------------------------------------------------------
RAW = {
    "owid": "data/raw/owid_co2.csv",
    "eurostat": "data/raw/env_air_gge_ghg.tsv",
    "worldbank_pages": "data/raw/api/worldbank/{indicator}_page*.json",   # .format(indicator="SP.POP.TOTL")
    "worldbank_countries": "data/raw/api/worldbank/country_page1.json",
    "country_codes": "data/raw/country_codes.csv",
}
SILVER = {                     # the pipeline registers each as silver.<name>: silver.eurostat, silver.owid, ...
    "owid": "data/silver/owid.parquet",
    "eurostat": "data/silver/eurostat.parquet",
    "worldbank": "data/silver/worldbank.parquet",
    "worldbank_page_counts": "data/silver/worldbank_page_counts.csv",   # one row per (indicator, page): read vs promised
}
REJECTS = {                    # quarantined and rejected observations, one file per source, with a reason
    "owid": "data/silver/rejects_owid.csv",
    "eurostat": "data/silver/rejects_eurostat.csv",
    "worldbank": "data/silver/rejects_worldbank.csv",
}
REJECTS_COLUMNS = "source, entity, year, item, raw_value, destination, reason"   # every rejects file, this order
GOLD = {                       # registered as gold.<name>
    "intensity": "data/gold/intensity.csv",
    "owid_vs_eurostat": "data/gold/owid_vs_eurostat.csv",
    "reconciliation": "data/gold/reconciliation.csv",
}
