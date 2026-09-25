# Diagnosis note

**Explained to:** ______ · **Need help with:** ______ (write *nothing* if none). This line is your Moodle checkpoint.

One entry per trap, under its own heading (`## Trap N — <source>: <the issue in one line>`): copy the five parts
below for each. Fill in every part, short is fine. Part 3 is **pasted**: the query you ran and what it returned,
not a description of it. Paste the evidence *before* you change anything — a fix erases the output that
proves the cause. Each output is pasted **once**, here; the dictionary, the note and other traps say *see Trap N*.

The World Bank entry opens with one more line, written **before** you write the `unnest` and left as you wrote it:
`Prediction: one row is …; key …; rows per page …`.

1. **What was the symptom?** Which number or shape was wrong, and what did you compare it to?

2. **What was the actual cause?** Not what you changed — why the old query produced that number.

3. **What evidence showed that?** Paste the queries you ran and their output: the census, `DESCRIBE`, the row count
   before and after, `COUNT(*)` against `COUNT(DISTINCT …)`, the NULL count — whatever showed you the cause.

```text

```

4. **What did you change?** Name the script and paste only the lines that make the change — the filter, the `CASE`
   branch, the join condition. The whole script is in your zip.

```sql

```

5. **How did you verify it?** Name the check that passes now and would fail if the problem came back — its `check`
   name in `output/checks_report.json` — and the number it observed; the grader's run prints the report, so do not
   paste it. If the verification is a reconciliation, say which identity must hold (a sum, a ratio's two parts, a
   weighted mean) and name its row in Appendix A of `NOTE.md`, where its two numbers are pasted.

```text

```
