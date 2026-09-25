"""World Bank population and GDP (cached API pages, JSON) -> silver.worldbank.   YOUR WORK: the body of run().

Also writes silver.worldbank_page_counts, the pages' own ledger (below).

Input   data/raw/api/worldbank/SP.POP.TOTL_page1.json ... _page4.json         population
        data/raw/api/worldbank/NY.GDP.MKTP.PP.KD_page1.json ... _page4.json   GDP, PPP, constant 2021 international $
        Each file is ONE page of an API response, exactly as received: a two-element JSON array,
        [ {page, pages, per_page, total, ...}, [ record, record, ... ] ]. One page is not the answer.
        data/raw/api/worldbank/country_page1.json - the same shape; one record per economy, with its region.
        A region of "Aggregates" marks a group of countries.

Parent and child - a list inside a record, on real pages:
  pages   the PARENT: one row per page file - the whole response. Its key is (indicator, page).
          read_text(glob) reads each file as ONE row, the file's text in `content`; CAST(content AS JSON) makes it
          a document: ->0 is the metadata, ->1 the list of records.
  records the CHILD: one row per JSON record, made IN SQL with unnest - not with a Python loop. Select the page's
          number BESIDE the unnest, so every record keeps the page it came from (the course site's reference,
          section 7: "a list inside a record"). Key: (country, indicator, date). Look at countryiso3code before
          you call it a key.
  BEFORE you write this query, write your prediction in the trap log (README, "The trap log"): what one row of
  the child table is, its key, and how many rows each page should give - the metadata says it: per_page, and on
  the last page what is left of total.

Key and grain - write them in docs/dictionary.md:
  silver             one row per (iso3, year, indicator): the 27 members (data/raw/country_codes.csv, column
                     worldbank_id) and the World Bank's own EU aggregate, EUU. Columns:
                       iso3          countryiso3code
                       year          INTEGER, from date
                       indicator     SP.POP.TOTL or NY.GDP.MKTP.PP.KD
                       value         DOUBLE: persons, or constant 2021 international $
                       is_aggregate  true for EUU only - from the country metadata's region, not a list you wrote
                       page          INTEGER: the page the record came from - carried down from its parent
  page counts        one row per (indicator, page), every page you read. Columns:
                       indicator, page
                       records_expected  what the page's metadata promises: per_page, or on the last page what is
                                         left of total
                       records_read      the rows of YOUR child table that carry this page, counted with GROUP BY
                     check_count compares the two, page by page (README, "The checks report").

Every record lands in exactly ONE destination, in this order (README, "The accounting"):
  rejected     a date that is not a year, or a value that is not a number
  excluded     neither one of the 27 nor EUU
  quarantined  one of them but impossible: a value at or below zero, or a year outside 2010-2024
  aggregate    EUU - kept with is_aggregate = true
  retained     everything else (a null value is retained as NULL, and counted)
Rejected and quarantined records go to data/silver/rejects_worldbank.csv with a reason.

You may reuse what the Block 4 lecture ran on these pages (the Lab 4 starter's notebooks/lecture.ipynb). It skipped
the metadata element; here you keep it, and carry its page down.

run(con) must return the accounting: a dict with the keys "in", "rejected", "excluded", "quarantined",
"aggregate", "retained" - counts of records - and "records_expected": what the pages' own metadata says the total
is, summed over the two indicators.
"""
from scripts.contract import EU_AGGREGATE_WORLDBANK, INDICATORS, RAW, REJECTS, REJECTS_COLUMNS, SILVER, WINDOWS


def run(con):
    raise NotImplementedError   # delete this line when you start

    # Write AS before every column alias: `year` and `source` are SQL keywords, and DuckDB refuses them bare.
    # YOUR WORK: build three tables:
    #   worldbank_silver       - the silver columns above, page included
    #   worldbank_rejects      - REJECTS_COLUMNS: source, entity, year, item, raw_value, destination, reason
    #   worldbank_page_counts  - indicator, page, records_expected, records_read
    # RAW["worldbank_pages"].format(indicator="SP.POP.TOTL") is the glob for one indicator's pages.

    # ---- supplied: persistence --------------------------------------------------------------------------------
    con.execute(f"COPY (SELECT iso3, year, indicator, value, is_aggregate, page FROM worldbank_silver "
                f"ORDER BY iso3, year, indicator) TO '{SILVER['worldbank']}' (FORMAT parquet)")
    con.execute(f"COPY (SELECT {REJECTS_COLUMNS} FROM worldbank_rejects) TO '{REJECTS['worldbank']}' (HEADER)")
    con.execute(f"COPY (SELECT indicator, page, records_expected, records_read FROM worldbank_page_counts "
                f"ORDER BY indicator, page) TO '{SILVER['worldbank_page_counts']}' (HEADER)")

    accounting = {"in": ..., "rejected": ..., "excluded": ..., "quarantined": ..., "aggregate": ..., "retained": ...,
                  "records_expected": ...}
    return accounting
