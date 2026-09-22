---
name: prompt-forge
description: Turn a vague request into a specification that produces a usable result on the first attempt. Use when the user asks to improve, rewrite, optimise, or rate a prompt, asks how to prompt something better, says a model keeps giving them the wrong or generic output, asks for a system prompt, a custom instruction set, or a reusable template, or hands over a prompt and asks what is wrong with it. Also use when a request is too underspecified to act on, since the fix is a better specification rather than a guess. Diagnoses which of six specific defects the prompt has, rewrites it with the missing context and success criteria, and states what the rewrite cannot fix. Triggers on improve my prompt, rate my prompt, better prompt, prompt engineering, system prompt, why does the AI keep giving me, make this prompt 10/10, write a prompt for, fix my prompt, the model ignores my instructions, my prompt gives generic answers, custom instructions, help me phrase this, what is wrong with this prompt, reusable prompt template.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
---

# Prompt forge

A prompt is a specification. Most bad output comes from a specification that did not say what good
looks like, and no amount of instruction phrasing repairs a missing requirement.

## The honest framing first

Rating a prompt out of ten is theatre. There is no scale, and any number is invented. What can be
done is checking a prompt against the six defects below and reporting which ones it has. That is
falsifiable, and it tells the user what to change.

So this skill reports defects and a rewrite. If a score is demanded anyway, give the count of defects
remaining out of six and say plainly that this is the only honest version of a score.

## Fit to the project

The project is the existing prompt, the model it runs against, and the failure the user already saw.
Read all three before rewriting anything:

1. Read the prompt as written, not as intended. Quote the exact lines that carry each defect back to
   the user, because a rewrite they cannot map to their original teaches them nothing.
2. Read which model and interface it targets. A system prompt for an agent with tools, a one shot
   chat message, and a template pasted into an app each constrain length, format, and what a failure
   instruction can even say. Rewrite for the target, not for a generic model.
3. Read the bad output the user got. The failure they can show you is the fastest route to the defect,
   faster than inspecting the prompt cold, because it names the gap between what they asked and what
   arrived.
4. Read what is fixed and cannot change. A required output format, a downstream parser, a brand voice,
   a length cap. Those become constraints in the rewrite rather than suggestions.
When nothing has been established, when the user hands over a prompt with no model and no example of
the failure, ask for the output they got and what they wanted before touching the wording.

## When to stay off

Skip the rewrite when the user asks a factual question about prompting rather than handing over a
prompt to fix, or when the prompt already works and they only want reassurance. Rebuilding a prompt
that is doing its job wastes their time and risks breaking a format a downstream tool depends on.

Saying "stop", "leave it as is", or "just execute" is the off switch. Answer the narrow question and
stop diagnosing. It stays off for the rest of the session unless the user asks for a rewrite again.

## Non-negotiables

1. Never invent a score out of ten. There is no scale and any number is fiction. Report the count of defects out of six or the user learns a fake metric and trusts it.
2. Never rewrite while guessing the goal. A prompt rebuilt for the wrong use is worse than the original, because it looks finished and hides that the target was never confirmed.
3. Every rewrite carries at least one fact only the user could supply. Without it the output regresses to the generic case, which is the exact complaint that brought them here.
4. List every assumption the rewrite makes in its own section. An assumption buried inside the prompt cannot be corrected, so the user ships a spec built on a guess they never saw.
5. Name the defect before fixing it. Fixing silently means the user cannot spot the same defect next time and comes back for every prompt.

## The six defects

Diagnose which apply before rewriting. Name them, because the user should learn to spot them without
help.

1. No success criteria. The prompt says what to make and not how anyone would know it worked. This is the most common defect and the most expensive.
2. Missing context that only the user has. Audience, constraints, existing decisions, what was already tried, what the surrounding system looks like. Without it the answer regresses to the generic case, which is the complaint that usually brought them here.
3. No output contract. Format, length, structure, and what to leave out are unspecified, so the reply arrives in a shape that needs manual reworking.
4. Multiple requests fused into one. Three tasks in one sentence produce a shallow pass at each. Splitting is usually the whole fix.
5. No failure instruction. The prompt does not say what to do when the model does not know, cannot comply, or finds the request contradictory. The default is to guess fluently, which is the worst option.
6. Leading or flattering framing. A prompt that signals the desired answer gets it. "Explain why this architecture is the right choice" is a request for advocacy, not analysis.

## Procedure

### Step 1, find the real goal

Ask what the output gets used for. The answer usually changes the prompt more than any phrasing
change. A summary for a decision meeting and a summary for a search index share no requirements.

If the goal is unclear, ask at most three questions. Never rewrite a prompt while guessing what it is
for.

### Step 2, extract what only the user knows

This is the step that produces a non-generic result, and it is the step usually skipped. Pull out the
constraints, the audience, the prior attempts, the things that are fixed and cannot change, and the
things that are explicitly out of scope.

Anything the model could not infer belongs in the prompt. Anything the model can infer is padding and
comes out.

### Step 3, write the success criteria

Write them before the instruction, because they determine it. Good criteria are checkable by someone
who did not write them.

Weak: "write a good landing page". Checkable: "a visitor who sells car parts should be able to tell in
one sentence whether this product handles their VAT case, and the page must not claim any feature not
in the attached list".

### Step 4, rewrite in the six part shape

Role and audience, only if it changes the answer. Skip decorative personas, since claiming expertise
does not create it.

Task, one goal per prompt.

Context, the facts only the user has.

Constraints, including what to leave out, which is more useful than it looks.

Output contract, the exact shape wanted, with an example if the shape is unusual.

Failure instruction, what to do on uncertainty. The sentence that earns its place in almost every
prompt: state uncertainty rather than filling the gap, and name what additional information would
resolve it.

Patterns for specific job types, including extraction, code generation, review, and long research
tasks, are in `references/patterns.md`.

### Step 5, remove what does not work

Politeness, threats, offers of payment, and instructions to think hard do not reliably change quality,
and they consume attention. Cut them.

Instructions that restate the model's defaults are noise. "Be accurate" changes nothing.

Negations are weaker than positive instructions. Rather than saying not to be verbose, give a length.

Long preambles about importance bury the actual request. Put the request first.

### Step 6, state the limits of the rewrite

A better prompt cannot supply facts the model does not have, cannot make a stylistic preference
objective, and cannot prevent confident errors on questions outside the model's knowledge. Say which
of those apply, and say what tooling would fix it, usually retrieval, a test, or a human check.

## Output shape

```
DEFECTS FOUND
[Which of the six, each in one line, quoting the part of the prompt at fault]

REWRITE
[The new prompt, ready to copy]

WHAT I HAD TO ASSUME
[Every assumption made in the rewrite, so the user can correct it]

WHAT THIS STILL WILL NOT FIX
[Limits that a prompt cannot address]
```

## Self-audit

- Each of the six defects was considered, not just the obvious one.
- The rewrite contains at least one fact that only this user could have supplied. If not, the context step was skipped and the result will be generic.
- Success criteria are checkable by a third party.
- Exactly one task per prompt, or the split is explicit.
- A failure instruction is present.
- Every assumption is listed rather than buried in the rewrite.
- No invented score. Defect count only.

A before and after rewrite for each of the six defects, with the failing output and the fix, is in
`references/rewrites.md`.

## Honest limits

A better specification cannot supply a fact the model does not hold, cannot make a wrong model right,
and cannot verify its output. When the prompt asks a research question, the retrieval and source
grading that would make the answer trustworthy belong to `deep-research`. When it asks for a
calculation, the recompute that catches a confident arithmetic error belongs to `numbers-check`, and
when the output is code, the readability contract belongs to `code-craft`.

This skill will not rate a prompt out of ten, because there is no scale and the number would be
invented; it reports the count of defects out of six instead. It cannot promise the rewrite works,
since only running it against the target model shows that, so treat the rewrite as a hypothesis to
test rather than a finished result.
