"""Our World in Data CO2 and greenhouse gases (CSV) -> silver.owid.   YOUR WORK: the body of run().

Input   data/raw/owid_co2.csv - one row per (country, year), 1990-2024, and the rows are countries AND groups of
        countries (World, continents, income groups, the EU). What each column means: data/raw/owid_codebook.csv.

Key and grain - write them in docs/dictionary.md:
  raw     one row per (country, year).
  silver  one row per (iso3, year): the 27 members (data/raw/country_codes.csv, column iso3), EVERY year the file
          has - the period 2010-2024 is applied in gold, so silver keeps what the source said. Columns:
            iso3                OWID's iso_code
            country             OWID's name
            year                INTEGER
            ghg_excl_lucf_mt    total_ghg_excluding_lucf, million tonnes CO2 equivalent - the series the brief
                                compares with Eurostat
            ... and any other OWID column you keep for the note (co2, consumption_co2, ...), named with its unit.

Every row lands in exactly ONE destination, in this order (README, "The accounting"):
  rejected     a year or a kept value that is not a number
  excluded     not one of the 27 (a group of countries, a country outside the EU, ...)
  quarantined  one of the 27 but impossible: a negative emissions value, or a year outside the file's own
               window, 1990-2024
  retained     everything else
Rejected and quarantined rows go to data/silver/rejects_owid.csv with a reason.

run(con) must return the accounting: a dict with the keys "in", "rejected", "excluded", "quarantined",
"aggregate" (0 here: silver.owid has no aggregate rows), "retained" - counts of raw rows.
"""
from scripts.contract import RAW, REJECTS, REJECTS_COLUMNS, SILVER, WINDOWS


def run(con):
    raise NotImplementedError   # delete this line when you start

    # Write AS before every column alias: `year` and `source` are SQL keywords, and DuckDB refuses them bare.
    # YOUR WORK: build two tables:
    #   owid_silver   - the silver columns above
    #   owid_rejects  - REJECTS_COLUMNS: source, entity, year, item, raw_value, destination, reason

    # ---- supplied: persistence --------------------------------------------------------------------------------
    con.execute(f"COPY (SELECT * FROM owid_silver ORDER BY iso3, year) TO '{SILVER['owid']}' (FORMAT parquet)")
    con.execute(f"COPY (SELECT {REJECTS_COLUMNS} FROM owid_rejects) TO '{REJECTS['owid']}' (HEADER)")

    accounting = {"in": ..., "rejected": ..., "excluded": ..., "quarantined": ..., "aggregate": 0, "retained": ...}
    return accounting
