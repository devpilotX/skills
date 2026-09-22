---
name: numbers-check
description: Verify quantitative work, arithmetic, units, statistics, and proofs, and recompute rather than trust. Use when the user asks to check a calculation, verify maths, review a financial model or spreadsheet, check a statistic or a percentage, validate a proof, work out unit conversions, estimate a quantity, or asks whether a number is plausible. Also use whenever a task involves arithmetic that a wrong answer would make harmful, since language models make confident arithmetic errors. Recomputes every figure with a script instead of in prose, carries units through the calculation, sanity checks the result against an independent estimate, and refuses causal claims from correlational data. Triggers on check my maths, verify this calculation, is this number right, check my model, does this add up, validate this proof, estimate how many, what are the odds, statistical significance, is this percentage correct, sanity check this figure, convert these units, did I calculate this right, check this spreadsheet.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Numbers check

Arithmetic written as prose is unverifiable and frequently wrong. This skill computes with a script,
carries units, and checks the answer a second way.

## Fit to the project

The project is the figure and the workbook it came from. Read them in this order before recomputing:

1. Read what kind of number it is. Money, a rate, a probability, a physical quantity, or a proof.
   Each has its own trap list in `references/checks.md`, and money in particular decides that the
   script must use a decimal type rather than binary floating point.
2. Read the inputs and their provenance. Which figures are given, which were retrieved, which are the
   author's assumptions. An input with no source is where a wrong answer usually enters, so flag it
   before trusting the chain built on it.
3. Read the units on every input and on the answer the question wants. A rate asked for and a
   quantity delivered is a dropped unit, and that mismatch is worth catching before any arithmetic.
4. Read the tooling that is present. If the project already has a spreadsheet, a notebook, or a
   language with a decimal library, compute in that so the check matches how the number was made.
When nothing has been established, restate the question quantitatively in step 1 and list the inputs
with their units before touching a calculator.

## When to stay off

Skip the full treatment for trivial mental arithmetic, a rounded figure the user called an estimate,
or a number nobody will act on. Writing a script to confirm that two plus two is four wastes the
user's attention and buries the checks that matter.

Saying "stop", "skip the cross-check", or "just execute" is the off switch. Give the figure and move
on. It stays off for the rest of the session unless the user asks for verification again.

The script this skill writes is source code, so it follows the `code-craft` contract: units named in
the variables, comments that say why a step exists, and no dead branches. A checkable script that is
itself unreadable defeats the point of showing your work.

## Non-negotiables

1. Compute with a tool, not in prose. Write and run a short script for anything beyond trivial mental arithmetic, and show the script. A script is checkable and a paragraph of numbers is not.
2. Carry units through every step and cancel them explicitly. Most real errors are unit errors, not arithmetic errors.
3. Check every result a second, independent way. An order of magnitude estimate, a different decomposition, or a boundary case. Two methods agreeing is weak evidence and still much better than one.
4. Never invent an input. Every figure is supplied by the user, retrieved with a citation, or labelled `ASSUMPTION:` with the reasoning and the sensitivity attached.
5. State precision honestly. A result computed from a figure with one significant digit does not have four. Do not report precision the inputs cannot support.
6. Separate what the numbers show from what they imply. Correlation is not causation, and a statistically significant result is not necessarily a meaningful one.

## Procedure

### Step 1, restate the question quantitatively

Write down what is being computed, the inputs, and their units. Ambiguity resolved here saves the whole
calculation. Percent of what, over which period, measured how.

If two readings of the question give different answers, say so and compute both rather than picking one
silently.

### Step 2, list inputs with provenance

Each input gets a value, a unit, and a source. Mark each as given, retrieved with a link, or assumed.
Assumed values get a range, not a point, because the range is what makes the sensitivity analysis
possible later.

### Step 3, compute with a script

```
python3 - <<'PY'
# state units in comments and keep them in variable names
revenue_per_unit_usd = 34.50
units_per_month = 1200
cogs_per_unit_usd = 21.10
monthly_gross_usd = (revenue_per_unit_usd - cogs_per_unit_usd) * units_per_month
print("gross margin per unit: %.2f usd" % (revenue_per_unit_usd - cogs_per_unit_usd))
print("monthly gross: %.2f usd" % monthly_gross_usd)
print("margin pct: %.1f%%" % (100 * (revenue_per_unit_usd - cogs_per_unit_usd) / revenue_per_unit_usd))
PY
```

Use exact decimal arithmetic for money, meaning a decimal type rather than binary floating point.
Rounding a currency figure with floating point produces errors that compound through a model.

Keep full precision through intermediate steps and round only at the end, then say where rounding was
applied.

### Step 4, check it a second way

Order of magnitude. Does the answer sit where a rough estimate puts it? Off by a factor of ten usually
means a unit error or a misplaced decimal.

Different decomposition. Compute it by a different route and compare.

Boundary cases. Set an input to zero, to one, and to a large value. Does the result behave sensibly?
Nonsense at a boundary means the model is wrong even where it looks right.

Dimensional analysis. Do the units of the answer match what the question asked for? If the question
wants a rate and the answer has units of a quantity, something was dropped.

### Step 5, sensitivity

Vary each assumed input across its range and report which one moves the answer most. That single item
is what the user should go and verify, and naming it is often more useful than the answer itself.

If the conclusion flips inside the plausible range of any assumption, say the conclusion is not
determined by the available data. That is a result, not a failure.

### Step 6, report

```
ANSWER
[The figure, with units and honest precision.]

INPUTS
[Each with value, unit, and provenance: given, retrieved with link, or ASSUMPTION with range.]

METHOD
[The script, and the units cancelling.]

CROSS-CHECK
[The second method and what it gave.]

SENSITIVITY
[Which input dominates, and the range over which the conclusion holds.]

WHAT THIS DOES NOT SHOW
[The claim a reader might wrongly draw from this number.]
```

## Statistics specifics

Rules and traps in `references/checks.md`, covering percentages, averages, rates, significance,
sample size, survivorship, and the errors that appear most in business and engineering numbers.

## Proofs and derivations

Check each step independently rather than following the author's reasoning, which is how a plausible
error survives review. Name the step that fails and give the counterexample. For an induction, check
the base case and confirm the inductive step uses the hypothesis exactly once and validly. Check
quantifier order, division by a quantity that may be zero, and any step taking a root or a logarithm of
something that may be non-positive.

If a step cannot be verified, say which one rather than passing the whole proof.

## Self-audit

- A script was run, and its output is in the answer.
- Units appear at every step and cancel correctly.
- Every input has provenance, and assumptions have ranges.
- A second independent check was done and reported.
- Precision reflects the weakest input.
- Money used decimal arithmetic.
- The dominant assumption is named.
- The section on what the number does not show is present and specific.

A fully worked recompute of a small financial model, with the script, the cross-check, and the
sensitivity table, is in `references/worked-model.md`.

## Honest limits

This skill verifies the arithmetic, the units, and what a figure can support; it does not judge
whether the underlying idea or plan is any good. When the question is whether a business should be
built on these numbers, the blunt verdict with kill criteria belongs to `reality-check`. When an input
itself has to be established from sources, graded, and dated rather than taken as given, that retrieval
is the job of `deep-research`.

A cross-check that agrees is weak evidence, not proof: two methods can share the same wrong assumption
and both land on the same wrong answer, so a passed check means no error was found rather than none
exists. Every result is only as sound as its inputs, and an assumption labelled with a range still
carries whatever bias put it there. This skill does not give financial, tax, or actuarial advice, and
a decision that needs a licensed professional is named as such rather than answered.
