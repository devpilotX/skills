---
name: skill-forge
description: Author a new skill for this repository so it scores ten out of ten and stops a model from a real default mistake, instead of restating good intentions. Use when adding a skill to the collection, when a draft scores nine and you need the last point, when the prose trips the style detector, when trigger phrases do not match how users actually ask, or when a skill reads as generic filler. Names the failure worth a skill, orders the parts so structure comes before prose, splits the main file from references by when the reader needs each, and runs the scorer, validator, and detector to closure. Triggers on write a new skill, add a skill to the repo, my skill scores nine, fix the style findings, skill wont pass the scorer, how do I structure a skill, write trigger phrases, my skill is too generic, author a SKILL.md, references arent linking, off switch for a skill, make this skill pass the rubric.
license: MIT
compatibility: This repository's skill specification. Any editor; the scorer, validator, and detector need Python 3.8 or newer.
metadata:
  version: 1.0.0
  suite: skills
---

# Skill forge

A new skill gets written prose-first, reads smoothly, scores nine, and stops the model from nothing it would not already do. It describes a topic well and prevents no mistake, so it adds words to the collection and changes no behavior. This skill authors a skill the other way round: start from the failure it prevents, build the structure, and write the prose last, so the file earns its place and passes the checks because it was built to.

## Fit to the project

Read the repository's own standard before writing, because it enforces itself mechanically.

1. Read `RUBRIC.md` for the ten criteria and the authoring order, and `STYLE.md` for the prose rules. The scorer and the detector apply these exactly, so a draft that ignores them fails at the last step regardless of how it reads.
2. Read two existing skills that already score ten, one that emits code and one that does not, and copy their shape rather than inventing a new one. Consistency across the collection is what lets a reader trust any file in it.
3. Check the list of existing skills so the new one does not duplicate a neighbour. Overlap splits the reader's attention and the next author's edits across two files that should have been one.
4. Confirm whether the skill produces code. If it does, its metadata sets `emits_code: true` and its body points at the `code-craft` contract, and the scorer checks for both.

## Non-negotiables

1. Name the failure before writing anything else. If you cannot say in two sentences what a competent person or a defaulting model gets wrong here, the skill has no subject and every later section will be filler. This is the test the rubric itself cannot mechanize, so it is on you.
2. Write the structure before the prose: the steps, the non-negotiables, the audit questions, then the sentences. Prose written first and fitted to the checks afterward reads as padding and scores as a stub on the parts that matter.
3. Split the main file from the references by when the reader needs each. What applies every time stays in the main file; lookup tables, worked examples, and domain detail move to references. A main file that carries everything stops getting read, which is the failure the split prevents.
4. Write trigger phrases from how people complain, not how an engineer indexes. Someone with the problem types "site is slow", not "latency percentile regression". Ten phrases in the wrong register means the skill never activates, so it never runs.
5. Fix findings rather than working around them. The style detector at its strictest must report nothing, and declaring a lint exemption to pass is banned outside the files that document the patterns. An exemption taken to hit the score hides the residue the check exists to remove.

## Procedure

### Step 1, name the failure

Write the two sentences that say what goes wrong by default and what this skill makes happen instead. Keep them; they become the opening of the file. If they will not come, stop and reconsider whether the skill has a subject, because no structure rescues a file with no failure to prevent.

### Step 2, write the procedure as bare steps

List the ordered steps with the output of each, no prose yet. At least four, written as `### Step 1,` through `### Step 4,` or more. Each step says what to do and what it produces, in an order that survives being followed literally. A list of topics is not a procedure and the scorer counts the steps.

### Step 3, write the non-negotiables and the audit

Write at least four numbered non-negotiables by asking what a helpful assistant would trade away under pressure, and name what breaks when each is ignored. Then write at least six self-audit items, each answerable yes or no by looking at the output. "The work is high quality" fails that test; "every figure is cited or labelled an assumption" passes it.

### Step 4, write fit-to-the-project and honest limits

Write `## Fit to the project` with at least three lines on what to read and detect in the host project before acting, and no host-specific paths or single-vendor mandates. Write `## Honest limits` with at least two lines naming what the skill does not do and which neighbouring skill owns that part. Add the off switch: the words "off switch" and a quoted stop phrase the user can say.

### Step 5, split content into references

Move the lookup tables, the worked example, and the domain detail into at least two files under `references/`. Mention each reference from the main file so it loads, and make sure every mentioned file exists, because the scorer checks the links in both directions.

### Step 6, write the description last

Once the skill's job is fixed, write the one-line description of 200 to 1024 characters. Include the words "Use when" and, after "Triggers on", at least ten comma-separated phrases in the register a user would actually type. Writing it last means it describes what the skill became, not what you hoped it would be. The register and common mistakes are in `references/triggers-and-audit.md`.

### Step 7, run the checks to closure

Run the scorer, the validator, and the detector. Fix every finding rather than exempting it. Loop until the scorer prints ten out of ten and the detector prints zero high, zero medium, zero low. The exact commands and how to read each report are in `references/scoring-workflow.md`.

## Self-audit

- Does the opening name a specific default failure, not define the topic?
- Is there an ordered procedure of at least four steps, each with an output?
- Are there at least four numbered non-negotiables, each naming what breaks if ignored?
- Are there at least six self-audit items, each answerable yes or no from the output?
- Does `## Fit to the project` tell the reader what to detect, with no host path or single-vendor mandate?
- Do at least two references exist, each mentioned from the main file and each present on disk?
- Is there an off switch with a quoted stop phrase?
- Does the scorer print ten out of ten and the detector print zero findings, with no lint exemption added to get there?

## Honest limits

This skill teaches how to build a skill to this repository's specification; it does not write the prose for you, and clean prose is the work of `human-prose`, whose detector this skill runs. It does not judge whether the subject is worth a skill, which is the judgement call the rubric says no check can make. Where a skill emits code, the quality of that code is owned by `code-craft`, not here.

The off switch: say "stop" or "just execute" and this skill stands down, so you author the file however you like without the structure-first process. It will not keep pushing the procedure after you decline.
