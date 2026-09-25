"""Eurostat greenhouse-gas emissions (raw TSV) -> silver.eurostat.   YOUR WORK: the body of run().

Input   data/raw/env_air_gge_ghg.tsv - Eurostat's bulk file as published: the first column packs five dimensions
        (its header says which, in order), each year is a column, a flag may be glued to a value after a space,
        and ':' means "not available" (it may carry a flag too). Flag meanings: data/raw/codelist_obs_flag.tsv.
        Sector names: data/raw/codelist_src_crf.tsv.

Key and grain, stage by stage - write the key of each stage in docs/dictionary.md:
  raw     one row per (freq, unit, airpol, src_crf, geo); the years are columns.
  long    one observation per (freq, unit, airpol, src_crf, geo, year). The accounting counts at THIS grain.
  silver  one row per (geo, year, src_crf): the 27 members (data/raw/country_codes.csv) and EU27_2020, the seven
          codes in contract.CODES, unit MIO_T only. Columns, in this order:
            geo           Eurostat's code (Greece is EL)
            year          INTEGER
            src_crf       one of contract.CODES
            ghg_mt        DOUBLE, million tonnes CO2 equivalent; NULL where the file says ':'
            flag          the flag letters, kept (NULL if none)
            is_aggregate  true for EU27_2020 only

Every observation lands in exactly ONE destination, in this order (README, "The accounting"):
  rejected     the cell cannot be read: not a number and not ':'
  excluded     outside the brief's scope: another unit, another sector code, a geography that is neither one of
               the 27 nor EU27_2020
  quarantined  inside the scope but impossible: negative emissions, or a year outside 2010-2024
  aggregate    EU27_2020 - kept in silver with is_aggregate = true
  retained     everything else: one of the 27, in scope, possible (a ':' is retained as NULL, and counted)
Rejected and quarantined observations go to data/silver/rejects_eurostat.csv with a reason.
The full accounting is required here, as in Lab 5: one CASE that sends each observation to exactly one destination
(if you missed Lab 5 or did not finish it: the Block 5 slides; the course site's "SQL and pipeline reference",
section 8).

You may reuse the Block 5 lecture's parser - run on this very file (the Lab 5 starter's notebooks/lecture.ipynb) -
or your Lab 5 parser, verbatim.
Read the file with every cell as text (all_varchar = true) before you cast anything.

run(con) must return the accounting: a dict with the keys "in", "rejected", "excluded", "quarantined",
"aggregate", "retained" - counts of long observations - and anything else you want printed with it.
"""
from scripts.contract import CODES, EU_AGGREGATE_EUROSTAT, GAS, RAW, REJECTS, REJECTS_COLUMNS, SILVER, UNIT, WINDOWS


def run(con):
    raise NotImplementedError   # delete this line when you start

    # Write AS before every column alias: `year` and `source` are SQL keywords, and DuckDB refuses them bare.
    # YOUR WORK: read the raw file as text; split and unpivot it to the long grain; separate the flag and keep it;
    # turn ':' into NULL and cast; send every observation to one destination; build two tables:
    #   eurostat_silver   - the silver columns above
    #   eurostat_rejects  - REJECTS_COLUMNS: source, entity, year, item, raw_value, destination, reason

    # ---- supplied: persistence --------------------------------------------------------------------------------
    con.execute(f"COPY (SELECT geo, year, src_crf, ghg_mt, flag, is_aggregate FROM eurostat_silver "
                f"ORDER BY geo, year, src_crf) TO '{SILVER['eurostat']}' (FORMAT parquet)")
    con.execute(f"COPY (SELECT {REJECTS_COLUMNS} FROM eurostat_rejects) TO '{REJECTS['eurostat']}' (HEADER)")

    accounting = {"in": ..., "rejected": ..., "excluded": ..., "quarantined": ..., "aggregate": ..., "retained": ...}
    return accounting
