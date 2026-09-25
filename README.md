# Homework 3 — Handover: the emissions brief

**ECBS5294 — Working with Data · Session 3 · expected time 8–9 hours · due date and late window: on Moodle**

The estimate assumes you did Labs 5 and 6. It is a planning estimate: this cohort's timings will replace it. If you
are well past it, post on the Moodle forum — not a mark against you.

## Start here

| | |
|---|---|
| **The question** | For the 27 EU countries, 2010 to 2024: how much greenhouse gas per person, and per unit of GDP, by source sector? What changed, and who leads? |
| **The files** | Three sources in three formats, in `data/raw/`: Eurostat's emissions file (TSV, as Eurostat publishes it), Our World in Data's CO₂ file (CSV), the World Bank's population and GDP (cached API pages, JSON). Plus `country_codes.csv`, which maps each country's code across the three. |
| **What you start with** | A pipeline that runs and makes nothing. `pipeline.py` works; the five stages it runs are empty. |
| **What you hand in** | `hw3-submission.zip` (the pipeline, `docs/dictionary.md`, `NOTE.md`, `DIAGNOSIS.md`, `REFLECTION.md`, `AI_USE.md`, `GIT_LOG.txt`) and a video of up to two minutes, both on Moodle. |
| **First thing to do** | Run the pipeline and read what it prints. Then read **The analytical contract**, below, twice. |

## Get the project

In your terminal (Git Bash on Windows, Terminal on macOS), in the folder where you keep course work:

```bash
git clone https://github.com/earino/ecbs5294-hw03-emissions-brief.git
cd ecbs5294-hw03-emissions-brief
uv sync
uv run python pipeline.py
```

Open **this folder** in VS Code. The last command prints every stage as `not written yet`, then
`no gold table was written`. That is the starting point: the runner works, and there is nothing for it to run.

Everything the pipeline makes goes under `data/silver/`, `data/gold/` and `output/`. Those folders are deleted and
rebuilt on every run, and Git ignores them. `data/raw/` is committed on purpose and is never edited.

## The brief

A ministry's analysis unit is taking over the EU emissions file from a colleague who has left. They want **one gold
table and one note**: greenhouse-gas emissions per person and per unit of GDP for the EU countries, from 2010 to the
latest year, by source sector, and a note a minister's adviser can read without knowing SQL.

The three sources arrive as they are. They disagree with each other in places, on purpose and by accident. Your job
is to build the table from code, prove it with checks that can fail, and say in plain words what the number means
and what it cannot tell you.

## The analytical contract

Two careful analysts given this brief would still build two different tables, because it leaves choices open. These
are the ministry's choices. **They are decisions, not discoveries: follow them exactly.** They are also in
`scripts/contract.py`, as constants you import.

| | The decision |
|---|---|
| **Gas** | All greenhouse gases, in CO₂ equivalent: Eurostat's `airpol = GHG`. |
| **Unit** | Million tonnes of CO₂ equivalent: Eurostat's `unit = MIO_T`. Silver has one unit, and its column says which (`ghg_mt`). |
| **Sectors** | Six Eurostat source sectors that do not overlap, and the national total they add up to (table below). No other sector is in scope. |
| **Scope** | Territorial emissions, **excluding land use** (LULUCF, `CRF4`) and **excluding international aviation and shipping** (memo items, `CRF1D1A`, `CRF1D1B`). The Eurostat total that matches is `TOTX4_MEMO`. |
| **Membership** | The EU-27 as of 2020, the same 27 in every year: the 27 rows of `data/raw/country_codes.csv`. Eurostat's own `EU27_2020` row and the World Bank's own `EUU` row are groups of countries: keep them in silver, flagged `is_aggregate`, and use them only to check your sums. |
| **Period** | 2010 to **2024**. 2024 is the latest year that all three sources report for all 27 countries: Eurostat's `TOTX4_MEMO`, OWID's `total_ghg_excluding_lucf`, and the World Bank's population and GDP all have 2024 for every member. "Latest" is never your decision. |
| **Per person** | Sector emissions ÷ the country's national population (World Bank `SP.POP.TOTL`), same year. Unit: **tonnes CO₂e per person**. |
| **Per unit of GDP** | Sector emissions ÷ the country's national GDP, PPP, constant 2021 international dollars (World Bank `NY.GDP.MKTP.PP.KD`), same year. Unit: **tonnes CO₂e per million international dollars**. Every sector is divided by the *national* population and GDP: what each sector produces is out of scope. |
| **The EU-27 figure** | A ratio of sums: the 27 members' emissions added up, divided by the 27 members' population (or GDP) added up. Never the average of 27 ratios. |
| **Country codes** | Use `country_codes.csv` to match the three sources. Never build a mapping yourself. |
| **Missing data** | A member-year-sector with no Eurostat value — the file says `:`, or has no row for it — stays out of the ratios and is **counted**; the note says how many. A member-year with no population or GDP would leave that year's ratios out, counted the same way. |
| **Domain rules** | Emissions are never negative: in this file, negative values occur only outside the seven codes (in land use and the one total that includes it, and in two memo items on long-term carbon storage). Population and GDP are above zero. A year sits inside its file's own window: OWID 1990–2024, Eurostat and World Bank 2010–2024. An observation in scope that breaks a rule is **quarantined**: written to that source's rejects file with a reason, counted, and the run goes on. |
| **The reconciliation check** | Inside Eurostat, where both sides come from the same file: for every country and year, the six sectors add up to `TOTX4_MEMO`, to **0.0001 Mt**; for every code and year, the 27 members add up to `EU27_2020`, to **0.0005 Mt**. `MIO_T` values are published to five decimals, so these are the source's rounding. Compare **within the tolerance, never with `==`**: `abs(sectors - total) <= TOLERANCE_SECTORS_MT`. A failure **stops** the run, with the gap in the message. |
| **The cross-source comparison** | Reported, **never a check**: OWID's `total_ghg_excluding_lucf` against Eurostat's `TOTX4_MEMO`, same 27 countries, same years, as a residual per country-year (Eurostat minus OWID). Explain it as far as the two sources' own documentation goes, and report the rest as unexplained. The two series are scoped differently, so they legitimately disagree: no tolerance applies, the size of the residual is not graded, and no further investigation is asked for or credited. |

The six sectors and the total (labels from `data/raw/codelist_src_crf.tsv`):

| Code | Sector |
|---|---|
| `CRF1` | Energy — every fuel burnt, including transport (`CRF1A3`) and the fuel burnt on farms (`CRF1A4C`) |
| `CRF2` | Industrial processes and product use |
| `CRF3` | Agriculture — livestock and soils, not farm fuel |
| `CRF5` | Waste management |
| `CRF6` | Other sectors |
| `CRF_INDCO2` | Indirect CO₂ |
| `TOTX4_MEMO` | Total (excluding LULUCF and memo items) |

These are Eurostat's **source sectors** — where the gas comes out, by process — not economic sectors. A haulage
company's diesel is Energy, not "transport services". Say so in the note if the reader could take them for industries.

## What is supplied

So that your hours go to the course's skills, the plumbing is done:

- **`pipeline.py`** — the runner. It deletes and rebuilds `data/silver/`, `data/gold/` and `output/`; runs the three
  cleaners; makes every silver file queryable as `silver.<name>`; runs the four check families and **stops at the
  first family that reports `stop`**; runs the report; and writes `output/checks_report.json` every time, even when
  a run stops or crashes. Do not edit it.
- **`scripts/contract.py`** — the contract above, as constants: the codes, the years, the windows, the tolerances,
  and where every file goes. Do not edit it.
- **Five scaffolds**, each with a docstring that states its input, the key and grain at every step, the columns of
  what it writes, and what it must return; the lines that save its tables are supplied at the bottom:
  `scripts/clean_eurostat.py`, `scripts/clean_owid.py`, `scripts/clean_worldbank.py`, `scripts/checks.py`,
  `scripts/report.py`.
- **`data/raw/country_codes.csv`** — the EU-27, with each country's code in all three sources.
- **The cached World Bank pages**, all of them, and the `country` metadata page. `clean_worldbank.py` reads each
  page as a **parent** (one row per page, the metadata and the list of records) and turns its list into **child**
  rows **in SQL with `unnest`** — not with a Python loop — with the page's number carried down to every record. The
  lines that save its tables, the page counts included, are supplied.
- **Permission to reuse**: the Block 5 lecture's Eurostat parser — run on this very file, and in the Lab 5
  starter's `notebooks/lecture.ipynb` — or your own Lab 5 parser, verbatim; and what the Block 4 lecture ran on the
  World Bank pages (the Lab 4 starter's `notebooks/lecture.ipynb`). Say in a comment where it came from.
  One difference from the waste file: a missing value here may carry a mark that is not in Eurostat's flag list,
  `: @C` (28 cells, all Croatia's `CRF1D2`, a memo item outside the brief). A Lab 5 parser that rejects unknown
  flags will set them aside as unreadable. Either is acceptable; say in your accounting which you did.

## The pipeline you build

| Stage | Script (yours) | Reads | Writes | One row is |
|---|---|---|---|---|
| silver | `clean_eurostat.py` | `env_air_gge_ghg.tsv` | `silver.eurostat`, `silver.rejects_eurostat` | one `(geo, year, src_crf)` |
| silver | `clean_owid.py` | `owid_co2.csv` | `silver.owid`, `silver.rejects_owid` | one `(iso3, year)` |
| silver | `clean_worldbank.py` | the eight indicator pages, `country_page1.json` | `silver.worldbank`, `silver.rejects_worldbank` | one `(iso3, year, indicator)`, with the page it came from |
| | | | `silver.worldbank_page_counts` | one `(indicator, page)`: the records the page promises, and the records read from it |
| checks | `checks.py` | silver | `output/checks_report.json` | one check |
| gold | `report.py` | silver | `gold.intensity`, `gold.owid_vs_eurostat`, `gold.reconciliation` | see **Gold** |

The silver columns are in each cleaner's docstring. A key check is written against the key of the table it checks:
`silver.eurostat` is a country-year-**sector** table, so country-year is not its key.

### The accounting

Every raw observation lands in **exactly one** destination, decided in this order:

1. **rejected** — the cell cannot be read (not a number, and not `:`);
2. **excluded** — outside the brief's scope (another unit, another sector code, a country that is not one of the 27
   and not the EU aggregate);
3. **quarantined** — inside the scope but breaks a domain rule;
4. **aggregate** — `EU27_2020` or `EUU`: kept in silver, `is_aggregate = true`;
5. **retained** — everything else. A `:` is retained as NULL, and counted.

Each cleaner returns its accounting as a dictionary, and the runner prints it:
`in = rejected + excluded + quarantined + aggregate + retained`. Eurostat counts observations (one country, sector,
unit and year); OWID counts rows; the World Bank counts JSON records, and also returns `records_expected`, the total
its pages say they hold. The count family checks that it adds up and that it matches what is on disk.

The World Bank is also counted **page by page**. Each page's metadata promises `per_page` records, and the last
page what is left of `total`. `silver.worldbank_page_counts` sets that beside the records your child table holds
with that page's number — a `GROUP BY` that works only because every record carries its page.

### Gold

`report.py` writes three tables, with these columns, because the ministry will open them:

- **`gold.intensity`** — one row per `(geo, year, src_crf)`, 2010–2024, for the 27 members and a row
  `geo = 'EU27'` computed from them: `geo, iso3, country, year, src_crf, sector, ghg_mt, population, gdp_ppp_usd,
  t_per_person, t_per_million_usd`.
- **`gold.owid_vs_eurostat`** — one row per `(geo, year)` for the 27, 2010–2024: `eurostat_total_mt,
  owid_ghg_excl_lucf_mt, residual_mt, residual_share`, and any columns that explain the residual.
- **`gold.reconciliation`** — one row per identity: `identity, left_label, left_value, right_label, right_value,
  gap, tolerance, holds`. At least: the EU-27's emissions against Eurostat's own `EU27_2020` row, and the EU-27's
  population and GDP against the World Bank's own `EUU` row, for 2010 and 2024.

## The checks report

`checks.py` has four empty functions, one per family. Each returns a list of records, and the runner writes every
record to `output/checks_report.json`. **This format is required**: a program grades it.

| Field | What it holds |
|---|---|
| `family` | `key`, `domain`, `count` or `reconciliation` — the family of the function returning it |
| `check` | a short name you choose, e.g. `silver_eurostat_key` |
| `subject` | the table and the key or columns checked, e.g. `silver.eurostat (geo, year, src_crf)`. **Name the silver table** — `eurostat`, `owid` or `worldbank`. |
| `observed` | the number the check computed |
| `threshold` | what that number is compared against |
| `action` | `stop`, `quarantine`, `dedupe`, `exclude`, `flag` or `pass` |
| `detail` | optional: one line a person can act on — which country-year, which page, how big the gap. The harness does not grade it; a person reads it. |

What each family checks, and what it does when the check fails:

| Family | Checks | When it fails |
|---|---|---|
| **key** | every silver table's key is unique and never NULL, the page counts' `(indicator, page)` included | `stop` (or `dedupe`, if your cleaner removed exact duplicates and counted them) |
| **domain** | no silver row breaks a domain rule, and the rows that did were quarantined | `quarantine`, and the run goes on |
| **count** | the accounting adds up and matches the files; every World Bank record the pages promise was read, page by page — `detail` names the page that falls short — and in total; every one of the 27 × 15 country-years is there in every source | `stop` if something simply is not there; `exclude` if it is accounted for and left out of the ratios |
| **reconciliation** | the two Eurostat identities in the contract | `stop`, naming the country-year and the gap |

**Comparing numbers.** Counts are whole numbers and compare exactly. Sums of tonnes are floating-point numbers and
**never compare with `==`**: a reconciliation computes the gap, `abs(a - b)`, and compares it with the contract's
tolerance — `abs(sectors - total) <= TOLERANCE_SECTORS_MT`, `abs(members - eu) <= TOLERANCE_EU27_MT` (both in
`scripts/contract.py`). Put the gap in `observed`, the tolerance in `threshold`, and the country-year and the gap in
`detail`, so the message says where and by how much. On the course's clean files, `sectors == total` is false for
280 of the 420 geo-years and `members == eu` for 80 of the 105 code-years: a check written with `==` stops a correct
pipeline, and the harness grades that as a failed clean run.

### How your checks are graded

The course runs a program, the **mutation harness**, on your submission:

1. It runs your pipeline on the course's **unchanged** raw files. Every family must report at least one record, all
   of them `pass`, and your checks together must name all three silver tables. A check that fails on clean data, a
   pipeline that crashes or stops, a cleaner or report still `not written yet`, or a report that is missing or
   malformed fails here, and the corruptions are not run.
2. It then runs your pipeline four more times, each on a fresh copy with **one raw file corrupted in one way**,
   designed for one family:

   | Family | The corruption | Caught when |
   |---|---|---|
   | key | one raw row duplicated | the key family says `stop` or `dedupe` |
   | domain | an impossible value, and a year outside its file's window | the domain family says `quarantine` |
   | count | one country-year removed from one source | the count family says `stop` or `exclude` |
   | reconciliation | one Eurostat sector value doubled | the reconciliation family says `stop` |

   A family **catches** its corruption only when its own record has one of those actions, **its subject names the
   corrupted silver table**, and **its observed value moved** from the clean run. A stop by the wrong family is a
   miss: a key corruption stopped by your reconciliation check means your key check did not work.

**Try it yourself before you submit.** Copy the project to a scratch folder, break one raw file there, and run it:

```bash
cd ..
cp -r ecbs5294-hw03-emissions-brief hw3-scratch
cd hw3-scratch
# edit ONE file in data/raw/ here: this copy is yours to break
uv run python pipeline.py
```

Read `output/checks_report.json`. Did the right family say the right thing, about the right table? Then delete
`hw3-scratch`. Never break `data/raw/` in your real project.

## The order of work

Evidence first: a cleaner erases the evidence of what it cleaned, so look before you write it.

**Required here, as in the labs:** every cleaner returns the **full accounting** (all five destinations, adding up
to what came in), and `checks.py` has **all four families** — key, domain, count and reconciliation. The harness
corrupts one file for each family, so a missing family is a missed family. Lab 5 is where you practised the
accounting (its section E prints the four destinations, counted from `rejects.csv` and silver) and Lab 6 the families
(the domain family, with its quarantine rules, in the lab's early-start minutes). If you missed either lab, or it
ended before you finished, start from the Block 5
and Block 6 slides and the course site's *SQL and pipeline reference*, sections 8–10: a `CASE` that sends each row to
exactly one destination, and a reconciliation compared within a tolerance.

1. Run the starter. Read the contract and `scripts/contract.py`.
2. **Before you write a cleaner**, open each raw file and look: `head` in the terminal, then `DESCRIBE`, row counts,
   and the census (`SELECT x, COUNT(*) … GROUP BY x`) of every column that is a dimension. Paste what surprised you
   into the trap log in `DIAGNOSIS.md` **now**, with the query and its output.
3. `clean_eurostat.py`, with its full accounting. Run the pipeline after every change: it takes seconds.
4. `clean_worldbank.py`, in three steps, then `clean_owid.py`, each with its full accounting:
   1. **Predict first**, in the trap log's World Bank entry, before you write the `unnest`: what one row of the
      child table is, its key, and how many rows each page should give. The metadata says it: `per_page`, and on
      the last page what is left of `total`.
   2. **The query**: one row per page (the parent), and `unnest` its list of records beside the page's number, so
      every record keeps its page — the course site's reference, section 7, *a list inside a record*.
   3. **The page counts**: the records each page promises beside the records your table holds with that page, as
      `silver.worldbank_page_counts`. The count family compares them.
5. `checks.py`, all four families, one at a time. Then make **one** family of your choice fail on purpose in a
   scratch copy (the recipe is under *Try it yourself* above) and paste what it reported into that family's trap-log
   entry. The grader's harness breaks all four; one by hand is how you learn to read what it will see.
6. `report.py`: gold, the comparison, the reconciliation table.
7. `docs/dictionary.md`, then `NOTE.md`.
8. **The fresh-clone test**: commit, then clone your own project into a new folder and run it from there. It proves
   your pipeline runs from what you committed, not from what happens to be on your disk:

   ```bash
   cd ..
   git clone ecbs5294-hw03-emissions-brief hw3-fresh
   cd hw3-fresh
   uv sync
   uv run python pipeline.py
   ```

9. The video, `REFLECTION.md`, `AI_USE.md`. Then `SUBMITTING.md`, exactly as written.

Commit after each stage works. The message says what the stage does and what it found: *"Clean Eurostat to silver:
MIO_T only, 27 members + EU27_2020; 240 ':' retained as NULL"* — not *"cleaner"*.

## What you hand in

1. **The pipeline**, running from a fresh clone: the bodies of the three cleaners, `checks.py`, and `report.py`.
2. **`docs/dictionary.md`** — the skeleton is supplied, with every silver table and its column names: fill in each
   table's key and, for every column, its type, meaning, unit, allowed values, what missing means, and what was done to
   it. Add a row for any column you keep beyond the listed ones. It is a tracked file on purpose: a
   dictionary written into `data/silver/` would not be in your zip.
3. **`NOTE.md`** — the note, with the reconciliation table as its appendix.
4. **`DIAGNOSIS.md`** — the trap log.
5. **`REFLECTION.md`** — the end-of-course reflection.
6. **`AI_USE.md`**, **`GIT_LOG.txt`**, and the zip, made as `SUBMITTING.md` says.
7. **A video of up to two minutes**, uploaded to Moodle beside the zip.

## The note

`NOTE.md`, **five to nine sentences**, for a ministry adviser who does not know SQL and will make a decision. It
must say:

- the metric: what is divided by what, for which countries and years, in which unit;
- the answer: the EU-27 per person and per unit of GDP in 2010 and 2024, and who leads in 2024 on each;
- what was left out, and how many (the missing sector values; anything quarantined);
- the assumptions a reader could miss (national denominators for every sector; territorial; land use, international
  aviation and shipping excluded);
- the reconciliation, in plain words: which totals agree with which, and to what precision;
- OWID against Eurostat, in one or two sentences: how far apart the two sources' totals are (the median residual, and
  the largest case), how much of it the two sources' documentation explains, and that the rest is unexplained;
- **what the data cannot answer**, as a claim about the data: *"this cannot tell you X, because the data has no Y."*
  "More research is needed" is not a claim.

Then one appendix: **A. The reconciliation table** — paste what `report.py` printed.

## The trap log

In `DIAGNOSIS.md`: **one entry per data issue that changed a number, or would have** had you not caught it — even
when your own query was never wrong. Each entry is a short five-part note, under its own heading:

```text
## Trap N — <source>: <the issue in one line>
1. Symptom: which number or shape was wrong (or would have been), and what you compared it with.
2. Cause: what the data does.
3. Evidence: the query you ran and what it returned, pasted.
4. Change: what your pipeline does about it, in which script, and only the lines that do it.
5. Verification: the check that now passes and would fail if the problem came back, by its check name.
```

The template at the top of `DIAGNOSIS.md` shows the five parts once; copy them for every trap. Its first line is a
lab-checkpoint line: leave it as it is.

**The World Bank entry opens with your prediction**, written before you write the `unnest` (step 4 of *The order of
work*), as a line of its own: `Prediction: one row is …; key …; rows per page …`. Leave it as you wrote it, even if
it was wrong: part 1 then says what the run showed instead. A wrong prediction costs nothing; a missing one is
missing evidence.

**Evidence lives in one place.** Each query's output is pasted once: in the trap log, under its trap's heading. The
heading is its name — *Trap 3* — and everything else points to it instead of pasting it again:

- part 5 of a trap **names the check** that would fail if the trap came back, by its `check` name in
  `output/checks_report.json`, and the number it observed. Do not paste the checks report: the grader's run prints it;
- a reconciliation's two numbers are pasted once, in Appendix A of `NOTE.md`; a trap's part 5 names the row;
- `docs/dictionary.md` says *see Trap 1* where a trap explains what was done to a column;
- the video shows one trap live, on your screen: it is the one place a trap is shown twice, on purpose.

## The video

Up to **two minutes**, your voice, opening with "Homework 3" and your repo's name. Scored on four elements:

| Element | Points | What earns them |
|---|---:|---|
| Symptom | 3 | Your pipeline running from a fresh clone, and the number the ministry gets |
| Cause | 5 | One trap that would have changed that number: what the data does, and why the naive query is wrong |
| Change | 3 | What your pipeline does about it, and where |
| Verification | 4 | A check failing on a corrupted copy, then passing on the real files |

## The reflection

`REFLECTION.md`: four prompts, four specifics. **300 words is a ceiling**, not a target. Re-read your three
homeworks' notes and trap logs first; that re-reading is the point, and the best preparation for the exam.

## Rules

- **Never edit `data/raw/`.** The raw data is the evidence; every cleaning step is code.
- The contract's decisions are the ministry's. A different unit, a different total, or a different final year is a
  different table, and it is graded as one.
- Do not edit `pipeline.py` or `scripts/contract.py`: the grading harness depends on both.
- Nothing you hand in lives in `data/silver/`, `data/gold/` or `output/`: the pipeline rebuilds them, and they are
  not in your zip.
- AI is allowed, and you are responsible for everything you submit. **AI writes SQL that runs. Running is not
  right.** Give it the schema and the grain, ask for the checks that would tell a right answer from a wrong one, and
  run them yourself. `AI_USE.md` says what you asked and how you checked the answer.

## Hints, if stuck

1. Before you write any cleaner, run the census of every dimension column: `unit`, `src_crf` and `geo` in Eurostat;
   `iso_code` in OWID; `countryiso3code`, and the first element of each page, in the World Bank files. Read every
   distinct value.
2. Put numbers side by side. Your silver total for one country in 2024 beside the same cell in the raw file. The sum
   of your 27 members beside `EU27_2020`. The records you read from each World Bank page beside what that
   page's metadata promises. The average of 27 ratios beside the ratio of the sums.
3. Every source has rows that are not the 27 countries, each with its own tell. The World Bank's first page is a
   quarter of the answer. Eurostat says every number twice, in two units. And `:` is not zero.

## Stretch

OWID's `consumption_co2` is CO₂ counted where goods are *consumed*, not where they are made. For 2023 (it has no
2024), compare it with `co2` for the 27: which members consume more CO₂ than they emit, and by how much? One
paragraph at the end of `NOTE.md`, marked *Stretch*. It is not graded; it is the best example in the course of data
that answers a question differently depending on how the question is asked.

## Git thread

Session 3's habit: **raw is committed, generated is ignored.** `git status` before every commit: if it lists anything
under `data/silver/`, `data/gold/` or `output/`, something is wrong — the pipeline makes those. A clean `git status`
and the fresh-clone test are part of the grade.

## Submitting

`SUBMITTING.md`, exactly as written. Do not expect graded feedback on this homework before the exam: when the late
window closes, a self-check key is posted on Moodle. The mock exam is posted after Session 3; its key comes with this
self-check key. Sit the mock before its key arrives; then compare your homework with the self-check key and your mock
with its key.

## If you got lost: how to reset

Both of these **destroy work**. Read before running.

**Discard uncommitted changes (destructive)** — throw away edits and new files; keep your commits:

```bash
git restore --staged --worktree .    # every tracked file back to the last commit, staged or not
git clean -fd                        # and remove new, untracked files
```

> ⚠️ Permanently deletes uncommitted changes, staged or not, and any new untracked files.

**Full reset to the starter state (destructive)** — back to exactly what you cloned; throws away your commits too:

```bash
git reset --hard origin/main
git clean -fdx
```

> ⚠️ Discards your local commits and uncommitted changes. The `-x` also removes ignored files — `data/silver/`,
> `data/gold/`, `output/`, the `.venv/` environment — so the folder matches a fresh clone. `uv sync` rebuilds the
> environment in a minute.
