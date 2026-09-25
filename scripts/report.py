"""Silver -> gold: the brief's table, the cross-source comparison, the reconciliation table.   YOUR WORK: run().

The pipeline runs this only after every check family has passed or quarantined. Silver is there as silver.eurostat,
silver.owid, silver.worldbank. The EU-27 membership and the three codes of each country: data/raw/country_codes.csv.

Gold, three tables - their grain and columns are the brief's (README, "Gold"), because the ministry will read them:

  intensity         one row per (geo, year, src_crf), 2010-2024: the 27 members, plus geo = 'EU27' computed from
                    them. Columns, in this order:
                      geo, iso3, country, year, src_crf, sector, ghg_mt, population, gdp_ppp_usd,
                      t_per_person          tonnes CO2e per person            = ghg_mt * 1e6 / population
                      t_per_million_usd     tonnes CO2e per million int. $    = ghg_mt * 1e12 / gdp_ppp_usd
                    Denominators are the country's own national population and GDP, same year, for every sector.
                    A member-year-sector with no Eurostat value is not a row: it is excluded, and you count it.
                    EU27 is a ratio of sums: the members' emissions over the 27 members' population (GDP) -
                    never the average of 27 ratios.
  owid_vs_eurostat  one row per (geo, year) for the 27, 2010-2024: eurostat_total_mt (TOTX4_MEMO),
                    owid_ghg_excl_lucf_mt, residual_mt (Eurostat minus OWID), residual_share (residual / Eurostat).
                    Add columns that explain the residual as far as the documentation goes.
  reconciliation    one row per identity: identity, left_label, left_value, right_label, right_value, gap,
                    tolerance, holds. At least: the EU-27 numerator against Eurostat's own EU27_2020 row, and each
                    EU-27 denominator against the World Bank's own EUU row, for 2010 and 2024.

Print what the note needs: the reconciliation table, and the numbers you will quote.
"""
from scripts.contract import (EU_AGGREGATE_EUROSTAT, EU_AGGREGATE_WORLDBANK, FINAL_YEAR, FIRST_YEAR, GOLD, RAW,
                              SECTORS, TOTAL, TOTAL_LABEL)


def run(con):
    raise NotImplementedError   # delete this line when you start

    # YOUR WORK: build three tables - intensity, owid_vs_eurostat, reconciliation - and print what the note needs.

    # ---- supplied: persistence --------------------------------------------------------------------------------
    con.execute(f"COPY (SELECT * FROM intensity ORDER BY geo = 'EU27', geo, year, src_crf) "
                f"TO '{GOLD['intensity']}' (HEADER)")
    con.execute(f"COPY (SELECT * FROM owid_vs_eurostat ORDER BY geo, year) TO '{GOLD['owid_vs_eurostat']}' (HEADER)")
    con.execute(f"COPY (SELECT * FROM reconciliation) TO '{GOLD['reconciliation']}' (HEADER)")
