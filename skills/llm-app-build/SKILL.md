---
name: llm-app-build
description: Build a product on top of a language model so it can be changed without a silent regression, distinct from training a model in ml-build. Use when wiring an application to a model API, adding retrieval to ground answers, pinning prompt and model versions, setting cost and latency budgets, validating structured output, handling tool calls and their errors, defending against prompt injection from untrusted content, caching responses, or adding a fallback when the provider fails. Triggers on call the LLM API, add RAG to my app, ground the answers, pin the prompt version, model got upgraded and broke, structured output from the model, function calling, tool use errors, prompt injection, cache LLM responses, provider is down fallback, cost per request too high, measure answer quality, stop hallucinations in my app.
license: MIT
compatibility: Any language and any model provider. The optional evaluation runner needs Python 3.8 or newer and the standard library.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# LLM app build

A model-backed feature ships, works in the demo, and breaks two weeks later when the provider updates the model behind the same name and nobody notices until users complain. Or it answers from the model's memory instead of the documents it was given, and the wrong answer reads exactly as confident as a right one. This skill builds the feature so a change is detectable and a wrong answer is catchable, which the default of prompt-and-ship does not give you.

## Fit to the project

Read the application and its constraints before wiring a model in.

1. Find how the project already calls external services: its HTTP client, its retry and timeout policy, its secret handling, its logging. The model call is another external dependency and follows the same rules, so it does not get a bespoke path that skips the project's timeout and error handling.
2. Detect whether an evaluation runner or a test suite exists that a model evaluation can join, so the quality check runs where the other checks run rather than as a manual ritual.
3. Read the cost and latency the product can tolerate per request. A feature with no budget will find one in the monthly bill or in a user who left while it thought.
4. Check what content the feature will handle and whether any of it comes from users or third parties, because that decides how much of the prompt-injection defense in `references/injection-and-tools.md` applies.

## Non-negotiables

1. Write the evaluation set before the first prompt. An evaluation written after the prompt gets shaped to the answers the prompt already gives, so it passes a broken system. This is the same rule `ml-build` states for models; here it applies to the prompt and the retrieval.
2. Pin the model version and the prompt version, and record both with every logged request. When the provider changes the model behind an unversioned name, an unpinned call changes silently and you cannot tell a regression from noise. A pinned version turns a silent upgrade into a visible, testable change.
3. Set a cost budget and a latency budget per request, and measure against them under real load. Token cost scales with usage and with prompt size, so a prompt that grew during development can multiply the bill without any code change looking wrong.
4. Validate every structured output against a schema before acting on it, and define what happens when validation fails. A model returns text, and text that looks like JSON is not JSON until it parses. Acting on unvalidated output crashes on the first malformed response.
5. Treat all retrieved and user-supplied content as untrusted. Content that reaches the prompt can carry instructions, and a model does not natively separate its instructions from the data it was given. An unhandled injection turns your feature into the attacker's tool.

## Procedure

### Step 1, write the evaluation set first

Before any prompt, collect 20 to 50 real or realistic inputs with the answer or the property each one should have, including the hard cases and the ones that should be refused. Write a rubric that scores an output pass or fail against a stated criterion, not a vibe. This set is what tells you whether a prompt change helped or hurt. Method detail and scoring live in `references/eval-and-cost.md`.

### Step 2, ground the answer with retrieval, and measure retrieval separately

When the answer must come from specific documents, retrieve them and put them in the prompt rather than trusting the model's memory. Measure whether the correct passage is retrieved at all, separately from whether the final answer is good, because a pipeline that retrieves the wrong passage cannot be fixed by prompt wording. Chunk on document structure, keep the section title in the chunk, and combine keyword with vector search so exact identifiers are not lost. The chunking failures and their causes are in `references/eval-and-cost.md`.

### Step 3, pin versions and set budgets

Record the model name with its version, the prompt template with a version, and the parameters, alongside every request in the logs. Set the per-request cost and latency budget and add a check that fails when a change pushes past it. Now a provider update or a prompt edit shows up as a measured difference, not a mystery.

### Step 4, make output structured and validated

Ask for structured output where the result is consumed by code, and validate it against a schema before use. On a validation failure, retry once with the error fed back, then fall back to a safe default or an explicit error. Never pass unvalidated model text into a downstream call. Code that parses and validates follows the `code-craft` contract so the parsing, the decision, and the fallback are separate and readable.

### Step 5, handle tool calls and their errors

When the model calls tools, treat every tool result as input to be checked and every tool call as able to fail. Define the error path for a tool that times out, returns an error, or returns something the model did not expect, and make sure a failed tool call does not silently become a made-up answer. The tool-error paths and the injection defense are in `references/injection-and-tools.md`.

### Step 6, cache, and fall back when the provider fails

Cache responses whose inputs repeat, keyed on the exact prompt and model version so a version change invalidates the cache. Define what the feature does when the provider is slow, rate-limits, or is down: a shorter timeout with a retry, a smaller or different model, a cached or default answer, or a clear failure. A feature with no fallback inherits the provider's every outage.

### Step 7, measure quality with the evaluation, not a vibe

Run the evaluation set on every prompt or model change and compare the pass rate to the previous version. Read the individual failures rather than trusting the aggregate, because an average can hide a whole category that now fails. Report the pass rate with the sample size.

## Self-audit

- Was the evaluation set written before the first prompt and kept unchanged while iterating?
- Are the model version and prompt version pinned and logged with every request?
- Is there a per-request cost and latency budget with a check that fails when it is exceeded?
- Is every structured output validated against a schema, with a defined failure path?
- Is retrieval quality measured separately from answer quality?
- Is all retrieved and user-supplied content treated as untrusted, with an injection defense in place?
- Does every tool call have a defined error path that cannot turn into a fabricated answer?
- Is there a defined fallback for a slow, rate-limited, or down provider?

## Honest limits

This skill builds the application around a model; it does not train or fine-tune one, and it does not cover classic tabular or vision modelling, which is what `ml-build` owns along with the shared evaluation discipline. Writing the prompt text itself so a model follows it reliably belongs to `prompt-forge`. The threat handling here is application-level; broader `security-hardening` owns authentication, secret storage, and transport. Cost figures depend entirely on the provider and change without notice, so the budgets here are a method, not a price.

The off switch: say "stop" or "just execute" and this skill stands down, so the model gets called the simplest way without an evaluation, pinning, or fallback. It will not keep adding guardrails after you decline.
