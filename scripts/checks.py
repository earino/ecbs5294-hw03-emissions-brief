"""The four check families.   YOUR WORK: the four functions at the bottom.

The pipeline runs them after silver, in this order - key, domain, count, reconciliation - and STOPS the run at the
first family that returns a record with action "stop": gold is never built from silver that failed a check.

Each function receives
  con         the DuckDB connection. Silver is there: silver.eurostat, silver.owid, silver.worldbank, and
              silver.rejects_eurostat, silver.rejects_owid, silver.rejects_worldbank.
  accounting  what each cleaner returned: accounting["eurostat"]["in"], accounting["worldbank"]["records_expected"], ...
and returns a LIST of records, one per check, each made with record() below. pipeline.py writes every record to
output/checks_report.json, which is what the grading harness reads (README, "The checks report").

A record says what one check found:
  family     "key" | "domain" | "count" | "reconciliation" - the family of the function that returns it
  check      a short name you choose, e.g. "silver_eurostat_key"
  subject    the table and the key or columns it checked, e.g. "silver.eurostat (geo, year, src_crf)".
             NAME THE SILVER TABLE: eurostat, owid or worldbank.
  observed   the number the check computed: a count of bad rows, a gap in million tonnes, ...
  threshold  what the number is compared against
  action     what the pipeline does about it:
               "stop"        an invariant is broken; the run ends here and gold is not built
               "quarantine"  rows that break a domain rule were set aside in a rejects file, with a reason; go on
               "dedupe"      exact duplicate rows were removed and counted; go on
               "exclude"     a country-year has no usable value; it is left out of the ratios and counted; go on
               "flag"        worth a look, not a failure
               "pass"        nothing found
  detail     (optional) one line a person can act on: which country-year, how big the gap

The shape of one check - a query that returns a number, and a decision about it:

    n = con.execute("SELECT COUNT(*) FROM silver.some_table WHERE <what must never happen>").fetchone()[0]
    return [record("key", "some_check", "silver.some_table (its key)", n, 0, "stop" if n else "pass",
                   f"{n} rows that should not exist")]

Comparing numbers: counts are whole numbers and compare exactly (n == 0, read == expected). Sums of tonnes are
floating-point numbers and NEVER compare with ==. A reconciliation computes the gap, abs(a - b), and compares it with
the contract's tolerance:

    action = "stop" if gap > TOLERANCE_SECTORS_MT else "pass"      # the gap goes in observed, the tolerance in
                                                                    # threshold, where and how much in detail
On the clean files, sectors == total is false for 280 of 420 geo-years: == stops a correct pipeline.

All four families are required in this homework. Lab 6 is where you practised them; if you missed it, or it ended
before you finished one, see the Block 6 slides and the course site's "SQL and pipeline reference", sections 9 and 10.

On the course's unchanged raw files, every record must say "pass". Then break a copy of a raw file yourself - one
duplicated row, one impossible value, one missing country-year, one sector value doubled - and watch the right
family catch it (README, "The checks report").
"""
from scripts.contract import TOLERANCE_EU27_MT, TOLERANCE_SECTORS_MT  # noqa: F401 - the reconciliation tolerances

FAMILIES = ("key", "domain", "count", "reconciliation")
ACTIONS = ("stop", "quarantine", "dedupe", "exclude", "flag", "pass")


def record(family, check, subject, observed, threshold, action, detail=""):
    """One check result, in the format output/checks_report.json requires. SUPPLIED: do not edit."""
    assert family in FAMILIES, f"family must be one of {FAMILIES}, not {family!r}"
    assert action in ACTIONS, f"action must be one of {ACTIONS}, not {action!r}"
    return {"family": family, "check": check, "subject": subject, "observed": observed, "threshold": threshold,
            "action": action, "detail": detail}


def check_key(con, accounting):
    """KEY. Every silver table's key is unique and never NULL:
         silver.eurostat (geo, year, src_crf) - silver.owid (iso3, year) - silver.worldbank (iso3, year, indicator)
         - silver.worldbank_page_counts (indicator, page).
    When it fails: "stop". ("dedupe" only if your cleaner removed exact duplicates and counted them.)"""
    raise NotImplementedError


def check_domain(con, accounting):
    """DOMAIN. No silver row breaks a domain rule, and every row that did was quarantined with a reason:
         emissions >= 0; population and GDP > 0; the year inside the source's own window (contract.WINDOWS).
    When rows were quarantined: "quarantine", and the run goes on. A violation still in silver: "stop"."""
    raise NotImplementedError


def check_count(con, accounting):
    """COUNT. Nothing vanished:
         each source's accounting adds up - in = rejected + excluded + quarantined + aggregate + retained - and
         matches what is in silver and in the rejects file;
         every World Bank record the pages say exist was read: PAGE BY PAGE, from silver.worldbank_page_counts
         (records_read against records_expected; detail names the page that falls short, e.g. "SP.POP.TOTL page 2:
         read 990 of 1000"), and IN TOTAL, against accounting["worldbank"]["records_expected"];
         the completeness grid - 27 members x 2010-2024 - has every cell in every source.
    A cell that is simply not there: "stop". A cell accounted for (a missing value the source reports, a quarantined
    row), left out of the ratios and counted: "exclude". These are counts: they compare exactly."""
    raise NotImplementedError


def check_reconciliation(con, accounting):
    """RECONCILIATION, inside Eurostat, where both sides come from the same file:
         CRF1 + CRF2 + CRF3 + CRF5 + CRF6 + CRF_INDCO2 = TOTX4_MEMO, for every geo and year,
             to TOLERANCE_SECTORS_MT;
         the 27 members add up to EU27_2020, for every code and year, to TOLERANCE_EU27_MT.
    "Add up to" means within the tolerance: compare the gap abs(a - b) with it, never a == b. observed is the largest
    gap, threshold the tolerance.
    When either fails: "stop", naming the geo-year (or code-year) and the gap in detail."""
    raise NotImplementedError
