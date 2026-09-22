---
name: build-pilot
description: Run a whole build as a staged process that thinks, researches, argues with itself, decides, then implements and verifies. Use when the user asks to build, create, make or develop an application, a website, a SaaS product, a service, a tool, a script or a feature, asks how to approach a project, asks for an architecture or a plan or a roadmap, or hands over a vague idea and expects working software at the end. Also use when a request is large enough that jumping straight to code would be guessing. Refuses to write code before the deciding facts are verified and the choice is recorded, presents real options with the argument against each, stops at named gates for the user to weigh in, then implements in vertical slices and reports honestly on what runs and what does not. Triggers on build me, create an app, make a website, develop a, I want to build, how should I approach, plan this project, architect this, from scratch, end to end.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Build pilot

Seven stages with gates between them. The stages exist because the expensive mistakes in software get
made before any code is written, and they get made by skipping straight to implementation.

Stage order is not a suggestion. Each stage consumes the output of the one before it.

## Fit to the project

Before stage 1, find out whether a project already exists and what shape it is in. A greenfield idea and
a change to a running system need different amounts of each stage.

Read the dependency manifest and lockfile to learn the language, the framework and the pinned versions
that any new work has to sit beside. Read the CI configuration and the test command so you know what
"it runs" will mean at stage 6 and 7. Read the top level README and any decision records under a docs
or adr folder, because a choice recorded there is a fact you do not get to relitigate in stage 3.

Look for the entry points, the data stores and the auth boundary the way `ship-audit` maps a codebase,
so stage 2 research is grounded in what is there rather than what you imagine. Note the commit history
depth and whether the tree is clean, since a dirty tree changes how stage 6 commits per slice.

When the project has settled nothing, meaning there is no repository yet, say so and treat every design
fact as unverified until stage 2 establishes it. Code this skill emits at stage 6 follows the
`code-craft` contract for file layout, function size and comments.

## Non-negotiables

1. No implementation code before stage 4 records a decision. A decision made while typing is a decision nobody reviewed.
2. No fact used in a decision unless it was verified this session or labelled `ASSUMPTION:` with its risk. Library versions, API shapes, limits, prices and platform rules all change, and recall is not verification.
3. Present the argument against the recommendation. A stage 3 that only supports one option is advocacy, not analysis.
4. Never claim code works without running it. Say which command was run and what it printed. "Should work" is not a result.
5. Report unfinished work as unfinished. A stub, a mock, a hardcoded value and a skipped test all get named in the status report.
6. Stop at the gates. A gate exists because the user holds information the process needs, and guessing past it wastes the whole build.
7. Scope creep gets named, not absorbed. When a new requirement appears, say what it costs and what it displaces.

## Procedure

### Phase 1, think

Restate the request in your own words, including what you think the user actually wants as distinct from
what they asked for. Getting this wrong is the most expensive failure available, and it is cheap to check.

Then produce four lists. What is certain because the user stated it. What is assumed and would change the
design if wrong. What is unknown and must be researched. What is explicitly out of scope.

Name the single hardest part of the problem. Every project has one, and a plan that does not mention it is
a plan built around the easy parts.

Ask at most five questions, chosen because the answer changes the design. Typical high value ones: who
uses this and how many of them, does it handle money or personal data, what has to integrate with it,
what is the deadline and what is fixed about it, and what has already been decided that cannot be
revisited.

Gate 1. Confirm the restatement before continuing. Details in `references/phase-gates.md`.

### Phase 2, research

Verify everything the decision rests on. Use the `deep-research` method: grade sources, prefer primary
ones, and date everything.

Check current versions and whether they are compatible with each other, not just current individually.
Check the actual API shape rather than the remembered one. Check platform limits, quotas, pricing tiers
and rate limits with a link. Check licences on anything being depended on. Check whether the problem is
already solved by something maintained, since the correct answer is sometimes to adopt rather than build.

Read the existing codebase if there is one, before proposing anything for it. Use `ship-audit` mapping to
find the entry points, the data stores, the auth boundary and the test suite. A design that ignores the
conventions already in the repository will be rejected in review.

Output a fact sheet where every line has a source and a date, plus a list of what could not be
established and how that limits the design.

### Phase 3, discuss

Generate at least three genuinely different approaches. Different in mechanism, not in naming. Borrow the
consensus firewall from `reality-check`: write down the obvious default approach, then make sure at least
one option is not it.

For each option give what it optimises for, what it costs in time and money and operational burden, what
it makes hard later, the failure mode it brings, and who on the team has to learn something new.

Then argue. State the strongest case for each option, then the strongest case against the one you prefer.
If you cannot argue against your own recommendation, you have not understood it yet.

Name the reversibility of each choice. A decision that can be undone in a day deserves far less debate
than one that locks in a data model or a vendor.

Gate 2. Put the options to the user with a recommendation. Do not proceed on a one way decision without
an answer.

### Phase 4, decide

Commit to one approach and write it down as an architecture decision record, using the shape in
`arch-decide`. Context, decision, options considered, consequences, and what would reverse it.

Apply the ground reality pass before accepting the decision. Run the relevant parts of `reality-check`
against it: what must be true for this to work, is it true, what does it cost to run at the expected
scale, and would this still be the answer for a team with different constraints. If the decision only
survives under optimistic assumptions, say so and name the assumption.

Where money is involved, use `business-model` for the cost side rather than estimating. Where numbers are
involved, use `numbers-check`.

### Phase 5, plan

Break the work into vertical slices. A slice goes from interface to storage and produces something
demonstrable. Horizontal layers, meaning all the models then all the services then all the screens,
hide integration problems until the end, which is when they are most expensive.

Order slices by risk, hardest and least certain first. The purpose of slice one is to find out whether the
design is wrong while changing it is still cheap.

Each slice gets acceptance criteria that someone else could check, a rough size, and its dependencies.
Name what is deliberately deferred so it does not look forgotten.

Gate 3. Confirm the slice order, since it determines what exists first if the work stops early.

### Phase 6, build

Implement one slice at a time. Finish a slice before starting the next, where finished means it runs, it
has a test on the risky part, and it is committed.

Follow the conventions already in the repository over any personal preference. Match the error handling,
logging, naming and test style already present.

Write the test first for anything involving money, auth, deletion or data integrity. Elsewhere, write it
straight after. Use `test-strategy` for what deserves a test.

Run the code after every slice. Run the test suite, the type checker and the linter. Paste real output.

Commit per slice with a message saying what changed and why. Never leave the tree broken between slices.

When something turns out harder than planned, stop and report rather than quietly reducing scope. The
schedule is the user's decision, not yours.

### Phase 7, verify and hand over

Run `ship-audit` against the result, with the bar set by what this project actually is.

Then report using the shape in `references/status-reporting.md`. What works with the command that proves
it. What is stubbed, mocked or hardcoded. What is untested. What was cut and why. What the next person
should do first. Known defects, including small ones.

Use `doc-forge` for the README or runbook, and `human-prose` on any prose before it ships.

## Stage skipping

Skipping is allowed only in these cases, and the skip gets stated.

A task small and reversible enough that the stages cost more than the work. Fixing a typo does not need
an architecture decision record.

A decision the user has already made and stated. Record it and move on rather than relitigating.

An existing plan or specification supplied by the user. Verify it in stage 2 and raise anything that
looks wrong, then continue from stage 5.

Never skip stage 2 verification on a fact that decides the design, and never skip the gates on a one way
door.

## When to stay off

A user who wants code now and has already made the design calls does not need seven stages. If they say
"stop", "just execute", or "skip the planning", that is the off switch: drop the gates, drop the option
generation, and implement what they asked from phase 6. It stays off for the rest of the session unless
they ask for the process back. Pushing stages onto someone who declined them gets the skill uninstalled.

## Self-audit

- Every fact that fed a decision was verified this session or carries an `ASSUMPTION:` label with its risk.
- Phase 3 presented at least three approaches that differ in mechanism, with the case against the recommended one written out.
- A decision record exists from phase 4 before any implementation code was written.
- Each build slice runs, has a test on its risky part, and was committed on its own.
- Every claim that something works names the command run and quotes what it printed.
- The status report lists what is stubbed, mocked, hardcoded, untested, or cut, with reasons.
- Any gate that was skipped is named, with the reason it was safe to skip.
- Scope added during the build was reported with its cost, not absorbed silently.

## Honest limits

This skill sequences a build and holds the gates. It does not write the code well on its own: file
layout, function length and comments are owned by `code-craft`, and what deserves a test is owned by
`test-strategy`. The research in phase 2 leans on `deep-research` for grading sources and `ship-audit`
for mapping an existing codebase; the cost side of a decision belongs to `business-model` and
`numbers-check`, not to an estimate made here.

Verification in phase 7 confirms that the commands run and print what the report says. It does not prove
the design was the right one, only that the built thing matches the recorded decision. Whether that
decision was sound is a judgement `reality-check` and `arch-decide` are built to challenge.
