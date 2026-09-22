# Evaluation, retrieval, and cost

How to build the evaluation set, what each retrieval and chunking choice costs when it goes wrong, and how to keep cost and latency inside a budget. The numbers here are rules of thumb; measure your own once you have traffic.

## The evaluation set, written first

An evaluation written after the prompt is shaped to the answers the prompt already gives, so it certifies a broken system as working. Write it first.

Collect 20 to 50 inputs that reflect real use, including the hard cases, the ambiguous ones, and the ones that should be refused or answered with "I do not know". For each, record the expected answer or the property the answer must have. Write a rubric that scores an output as pass or fail against a stated criterion. A criterion like "the answer cites a source passage that supports it" is checkable; "the answer is good" is not.

Keep the set unchanged while you iterate on the prompt. Change the set only when the task changes, and note when you did, because a moving target cannot show progress.

## Scoring without a vibe

Score against the rubric, not an impression. Where a human scores, give two people the same rubric and check they agree before trusting the scores. Where a model scores another model's output, validate the scorer against a human-scored sample first, because an unchecked model grader drifts in the same direction as the model it grades.

Report the pass rate with the sample size. A pass rate with no denominator is not a result. Read the individual failures every time, because an aggregate that looks stable can hide one category that started failing after a prompt edit.

## Retrieval choices and the failure each causes

Retrieval quality sets the ceiling on answer quality. When the right passage is not retrieved, no prompt wording recovers it, so measure retrieval on its own: does the correct passage appear in the top results.

Chunking too large dilutes the match, so the right passage ranks below a longer loosely related one and never reaches the prompt. Chunking too small cuts a fact in half, so neither half carries enough context to be retrieved or to answer. Chunk on document structure, a section or a paragraph, and keep the section and document title inside the chunk text so a chunk read alone is still interpretable.

Pure vector search misses exact identifiers, product codes, error strings, and rare terms, because embeddings blur the exact token that mattered. Combine keyword and vector search so the exact match is not lost.

No retrieval hit must be handled explicitly. When nothing relevant is found, the feature says it does not know rather than answering from the model's memory, and that behavior is in the evaluation set.

When documents change, plan reindexing before it is needed, because a stale index answers from content that no longer exists.

## Cost and latency budgets

Set both per request before building, from what the product can tolerate, not from what the model happens to cost today.

Cost scales with total tokens, which is prompt plus retrieved context plus output. A prompt or a retrieval window that grew during development multiplies cost without any single change looking wrong, so check token counts, not just wall-clock behavior. Measure cost at the traffic of the heaviest users, because a fixed per-request cost becomes a large bill at volume.

Latency is dominated by the model call and by output length, since most providers stream tokens one at a time. Long outputs are slow outputs. Cap output length, and where a user waits, stream the response so the wait is visible progress rather than a frozen screen.

Add a check that fails the build or alerts when a change pushes cost or latency past budget, so a regression is caught at the change, not on the invoice.

## The optional runner

Where Python is available, a small standard-library runner can read a JSON file of cases and a callable that produces an output, score each against its rubric, and print the pass rate with the sample size and the list of failures. Keep it under the `code-craft` contract: read the cases, call the system under test, score, and report as separate functions, so the scoring logic is testable without a live model call.
