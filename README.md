# skills

Fifty eight agent skills built around one rule: say the true thing, in the user's own situation,
without the accent of machine writing.

They exist because of two failures that show up in almost every assistant. The first is flattery,
which produces agreement instead of assessment. The second is convergence, which hands every user the
same high probability answer. Fixing only the first gives you a confident, rude, generic answer, which
is not an improvement.

Every skill in here scores ten out of ten against the rubric in [RUBRIC.md](RUBRIC.md), and the score
is computed by [tools/score_skills.py](tools/score_skills.py) rather than asserted. Each one names the
failure it prevents, adapts to whatever project it lands in, carries an ordered procedure, a self
audit, an off switch, and a statement of what it cannot do.

Works in [Kiro](https://kiro.dev/docs/skills.md) and in any tool that reads the open
[Agent Skills specification](https://agentskills.io/specification), including Claude Code.

## The skills

Fifty eight of them, in nine groups.

### Running the work

| Skill | What it does |
|---|---|
| [build-pilot](skills/build-pilot/) | The whole build as seven staged phases: think, research, argue with itself, decide, plan, implement, verify. Gates where your input is needed. Writes no code before the deciding facts are verified. |
| [arch-decide](skills/arch-decide/) | Classifies a decision by what reversal costs, spends effort in proportion, and writes the decision record. Refuses complexity your team size cannot operate. |
| [release-manage](skills/release-manage/) | Separates deploying code from releasing behaviour, so a bad change is a toggle rather than an incident. |
| [migration-plan](skills/migration-plan/) | Incremental migration with both systems running and every step reversible. No cutover weekend. |
| [devex-tooling](skills/devex-tooling/) | One command from clean checkout to running, with pinned versions and a feedback loop short enough that nobody skips it. |

### Building software

| Skill | What it does |
|---|---|
| [code-craft](skills/code-craft/) | Files split by responsibility, functions short enough to hold in your head, comments that say why. Ships a structure linter covering twenty plus languages. |
| [frontend-build](skills/frontend-build/) | The five states most interfaces omit, state in the narrowest scope that works, accessibility during the build, bundle size budgeted in kilobytes. |
| [backend-build](skills/backend-build/) | Object level authorisation, a stated concurrency assumption per write path, timeouts everywhere, idempotency before the retry arrives. |
| [data-layer](skills/data-layer/) | Schemas, indexes read from the query plan, and migrations treated as production operations with a lock estimate. |
| [auth-implement](skills/auth-implement/) | Sessions or tokens chosen by what the client actually is, object level checks on reads as well as writes, and recovery treated as the most attacked path. |
| [queue-design](skills/queue-design/) | Idempotency keys before the retry arrives, visibility timeouts longer than the worst real runtime, and a dead letter path that leads back. |
| [mobile-build](skills/mobile-build/) | Offline behaviour decided before the screens, process death survived, store rejection causes covered. |
| [ml-build](skills/ml-build/) | Evaluation set and trivial baseline before the model. Treats a good score as leakage until proven otherwise. |
| [llm-app-build](skills/llm-app-build/) | An evaluation set written before the first prompt, pinned model versions so a silent upgrade is visible, and untrusted content kept out of instructions. |
| [i18n-localize](skills/i18n-localize/) | Strings out of the code, plurals that survive a template, and pseudo-localisation to find the hardcoded ones before a translator does. |
| [infra-deploy](skills/infra-deploy/) | Simplest hosting the requirements allow, rollback actually performed once, cost estimated from retrieved prices. |
| [observability-setup](skills/observability-setup/) | Works back from the questions you need answered at 3am. Every alert has an owner and an action. |
| [security-hardening](skills/security-hardening/) | Threat model first, findings ranked by reachability, advisories retrieved rather than recalled. |

### Keeping it working

| Skill | What it does |
|---|---|
| [ship-audit](skills/ship-audit/) | Eleven gate production readiness audit. Every finding names a file, a line, the trigger, and what is lost. |
| [code-review](skills/code-review/) | Defects that cost something. Ignores anything a linter owns. Reports a clean change as clean. |
| [test-strategy](skills/test-strategy/) | Effort allocated by what a failure costs. Says plainly that coverage percentage measures execution, not correctness. |
| [debug-method](skills/debug-method/) | Reproduce, then one hypothesis at a time with a prediction that can be wrong. A symptom that stopped is not a fix. |
| [performance-tuning](skills/performance-tuning/) | Profile first, fix the dominant cost, report before and after from the same method. |
| [refactor-safely](skills/refactor-safely/) | Never mixes a refactor with a behaviour change. Safety net first, small reversible steps, suite green between each. |
| [codebase-onboard](skills/codebase-onboard/) | Gets it running before reading it, traces one request end to end, and uses history to find the files nobody dares touch. |
| [incident-response](skills/incident-response/) | Stabilise before diagnosing. Severity from user impact, a communication cadence, then a review where every action has an owner and a date. |
| [dependency-guard](skills/dependency-guard/) | Pinned versions and committed lockfiles, advisories ranked by reachability, name confusion checked before anything is added. |
| [git-discipline](skills/git-discipline/) | One commit per reversible idea, messages that say why, and recovery from the mistakes that feel unrecoverable. |
| [cost-control](skills/cost-control/) | Attributes spend before cutting anything, fixes the dominant line, and reports unit cost per request instead of a total. |

### Design and interface

| Skill | What it does |
|---|---|
| [ui-design](skills/ui-design/) | A spacing scale, a type scale with real sizes, colour picked for contrast ratio first. Concrete values instead of adjectives. |
| [design-system](skills/design-system/) | Token layers from raw value to semantic role, a rule for what earns a component, and a plain statement of when a design system is premature. |
| [accessibility-audit](skills/accessibility-audit/) | The keyboard path walked, focus visible, names and roles checked against named success criteria. Says what automation cannot catch. |

### Search and distribution

| Skill | What it does |
|---|---|
| [seo-optimize](skills/seo-optimize/) | Crawlability, indexation and on-page work diagnosed from real data before anything gets rewritten. Promises no ranking. |
| [llm-visibility](skills/llm-visibility/) | Content shaped so a passage can be lifted and attributed, entity clarity, and a decision on which AI crawlers to allow. |
| [index-fast](skills/index-fast/) | Sitemaps, robots rules and the canonical mistakes that silently block indexing. Separates discovered from crawled and not indexed. |
| [content-craft](skills/content-craft/) | One reader, one job, a promise kept. Replaces generic claims with detail the writer could only get by looking. |
| [landing-convert](skills/landing-convert/) | One page, one action, objections answered in the order a buyer meets them. Refuses fake scarcity. |
| [launch-plan](skills/launch-plan/) | Positioning against doing nothing, the audience you can actually reach, and a plan for the far more likely quiet landing. |

### Judgement and communication

| Skill | What it does |
|---|---|
| [reality-check](skills/reality-check/) | Names the answer every other user got, bans it, then judges your idea against your own non-transferable advantages. BUILD, PIVOT or KILL with dated kill criteria. |
| [human-prose](skills/human-prose/) | Removes the stylistic residue of machine writing, then verifies with a working 23 rule detector rather than a judgement call. |
| [prompt-forge](skills/prompt-forge/) | Diagnoses which of six defects a prompt has and rewrites it. Refuses to invent a score out of ten. |
| [deep-research](skills/deep-research/) | Graded sources, reported contradictions, and an explicit list of what could not be established. |
| [numbers-check](skills/numbers-check/) | Recomputes with a script, carries units, cross-checks a second way, names the assumption that decides the result. |
| [data-analysis](skills/data-analysis/) | The question and the decision it feeds written before the file opens. Missing values treated as information, uncertainty reported as a range. |
| [doc-forge](skills/doc-forge/) | Documents chosen by what the reader does next, plus a zero dependency Markdown to print ready HTML and PDF converter. |

### Business and money

| Skill | What it does |
|---|---|
| [business-model](skills/business-model/) | Contribution margin, the working capital cycle, break-even, payback. Models cash rather than only profit. |
| [pricing-model](skills/pricing-model/) | Price anchored on value delivered and the buyer's alternative, the metric it scales with, and what a discount teaches a buyer. |
| [growth-experiment](skills/growth-experiment/) | Sample size and stopping rule fixed before the test runs. Reads a null result as a real answer. |
| [user-research](skills/user-research/) | Recruits people who have the problem, asks for the last concrete instance, and listens for workarounds over opinions. |
| [email-deliver](skills/email-deliver/) | Authentication records that actually match, transactional and marketing kept apart, and a way to find where a message stops. |
| [payments-integrate](skills/payments-integrate/) | Idempotent charges, verified webhooks, money in integer minor units, and reconciliation against the provider's payouts. |
| [compliance-map](skills/compliance-map/) | Data inventory before regulation, retention that actually runs, and evidence a reviewer can follow. Names where a lawyer takes over. |
| [finance-books](skills/finance-books/) | Bookkeeping, reconciliation and statement checking. Stops at the line where a licensed accountant is required. |

### Career

| Skill | What it does |
|---|---|
| [career-strategy](skills/career-strategy/) | Career decisions priced in years and money, anchored in your financial position and rare skill combinations. |
| [job-hunt](skills/job-hunt/) | Diagnoses which stage of the funnel is broken before rewriting anything. |

### Agent tooling

| Skill | What it does |
|---|---|
| [memory-keeper](skills/memory-keeper/) | Plain text project memory so a session you closed last week resumes without you retelling it. Ships a working memory command line tool. |
| [agent-orchestrate](skills/agent-orchestrate/) | When delegation pays, what the parent has to verify rather than trust, and loop limits so a review cycle terminates. |
| [skill-forge](skills/skill-forge/) | Writes a new skill to the rubric in this repository. Structure before prose, triggers taken from how people actually complain. |

### How they chain

`build-pilot` is the entry point for anything substantial. It calls the others in order: `deep-research`
to verify the facts, `reality-check` to test the premise, `arch-decide` to record the choice, the build
skills to implement, `code-craft` to keep the result readable, `test-strategy` and `code-review` while
working, then `ship-audit` before release. Each one also works alone.

Two more run across a whole session rather than at a point in it. `code-craft` applies to every file
any skill writes. `memory-keeper` records what was decided so the next session starts from the
decision rather than from the beginning.

## Install

Pick the scope you want.

Project scope, shared through a repository:

```
git clone https://github.com/devpilotX/skills.git devpilotx
mkdir -p your-project/.kiro/skills
cp -r devpilotx/skills/* your-project/.kiro/skills/
```

Personal scope in the Kiro IDE or CLI:

```
mkdir -p ~/.kiro/skills
cp -r devpilotx/skills/* ~/.kiro/skills/
```

Kiro Web and Mobile do not read `~/.kiro/skills`. Use Settings, then Skills, and upload a skill as a
zip. There are three ways to get one:

```
bash tools/build_dist.sh          # writes dist/<skill>.zip and dist/skills-all.zip
```

Per skill zips are attached to each [release](https://github.com/devpilotX/skills/releases) by the
release workflow, alongside `SHA256SUMS.txt` for verification. The whole repository at a tag is also
downloadable directly:

```
https://github.com/devpilotX/skills/archive/refs/tags/v1.0.0.zip
```

For Claude Code, copy a skill folder into `.claude/skills/`. The format is the same.

## Use

Each skill activates from its description when your request matches, or explicitly as a slash command
named after the folder:

```
/build-pilot build a booking system for a two person dental practice
/reality-check I want to start a timber company with 30,000
/seo-optimize traffic dropped after the redesign and I do not know why
/memory-keeper pick up where we left off on the billing rewrite
/ui-design this dashboard looks amateur and I cannot say why
/debug-method it works locally but 500s in production
```

Every skill has an off switch. Saying "stop", "I've decided", or "just execute" ends it for the
session. Skills that nag get uninstalled.

## Four working scripts

Most skill collections are documentation. Four of these ship code, none of which needs a third party
package.

`skills/human-prose/scripts/ai_tells.py` detects 23 classes of machine writing marker across three
severities, from leaked citation markup and tracking parameters through to overrepresented vocabulary
measured as a density. It skips fenced code and frontmatter, and supports per file per rule exemptions
that are printed in every report so no exemption stays hidden.

```
python3 skills/human-prose/scripts/ai_tells.py --strict docs/*.md
```

`skills/code-craft/scripts/structure_scan.py` measures code lines, function length, nesting depth and
parameter count against per language budgets, across more than twenty file extensions. It reads
indentation and braces instead of parsing, counts a docstring as documentation rather than code, and
skips generated files.

```
python3 skills/code-craft/scripts/structure_scan.py src/ --max-function 40
```

`skills/memory-keeper/scripts/memory.py` keeps a plain text memory directory: project facts,
decisions with dates and reasoning, current state, open questions, and a dated log. It prints a
session opening briefing and reports any file that has grown past its budget.

```
python3 skills/memory-keeper/scripts/memory.py brief
```

`skills/doc-forge/scripts/md2doc.py` converts Markdown to self contained HTML with embedded A4 print
rules, then to PDF using whichever of weasyprint, wkhtmltopdf, Chromium or pandoc is installed. With
none installed it says so and exits 3, and the HTML still prints correctly from a browser.

```
python3 skills/doc-forge/scripts/md2doc.py report.md --toc --pdf
```

## Verification

Nothing here is asserted without a check behind it.

```
python3 tools/score_skills.py        # the ten point rubric, per skill
python3 tools/validate_skills.py     # spec, references, scripts, style, hygiene, README
python3 tests/test_ai_tells.py       # 28 checks on the style detector
python3 tests/test_md2doc.py         # 31 checks on the document converter
python3 tests/test_score_skills.py   # 15 checks on the rubric scorer
python3 tests/test_structure_scan.py # 13 checks on the structure linter
python3 tests/test_memory.py         # 12 checks on the memory tool
```

The scorer reports every skill at ten out of ten and names the criterion and reason for any point
lost. The validator runs 1087 checks: it enforces the skill specification, confirms every referenced
file exists and every existing file is referenced, compiles every script, and runs the style detector
across all 184 Markdown files in the repository. The five test files run 99 checks between them. CI
runs all of it on every push and pull request.

The repository holds itself to its own rules, which is the part worth checking if you doubt any of the
above. Every Markdown file passes the style detector at its strictest level, and the two files that
have to enumerate the banned patterns declare per rule exemptions that the report prints. Every Python
file passes `structure_scan.py` at the budgets in `code-craft`, which took refactoring two of the
older functions rather than raising the limits.

## What this does not claim

Stated plainly, because overselling would break the first rule.

No skill makes a model original. What these do is subtract the predictable answer and force the
reasoning through facts only you have. The differentiation comes from your inputs.

Removing the markers of machine writing does not make text human authored. It changes how it reads,
not where it came from. Detection is unreliable in both directions, human judgement performs near
chance, and classifier tools have error rates that matter, which is why Wikipedia tells its own editors
not to depend on them. Where authorship must be disclosed, disclose it.

Ten out of ten means ten mechanical criteria passed. A file can pass all ten and still be generic, so
the rubric ends with a judgement no script can make: read the skill and ask what it stops the model
from doing. That question is in [RUBRIC.md](RUBRIC.md) alongside the criteria.

There is no measurable score out of ten for a prompt, a document, or an idea. Any such number is
invented, so `prompt-forge` reports a defect count instead.

Verdicts are opinions with reasoning attached. Push back with evidence and they should change. Push
back with displeasure and they should not.

`finance-books` is not tax, audit, or regulatory advice, `compliance-map` is not legal advice, and
`career-strategy` is not legal, immigration, or financial advice. Each names the question to put to a
professional instead of guessing.

## Why convergence is the real problem

Measured, not assumed.

Model responses cluster far more tightly with each other than independent human responses do
([arXiv 2501.19361](https://arxiv.org/html/2501.19361v1)).

In a 36 participant study, people using one assistant produced less semantically distinct ideas than
people using a different tool ([arXiv 2402.01536](https://arxiv.org/abs/2402.01536)).

Output diversity has fallen across three years of model releases
([arXiv 2608.19437](https://arxiv.org/html/2608.19437)), and the mechanisms behind low idea diversity
are documented ([arXiv 2602.20408](https://arxiv.org/html/2602.20408)).

Two mitigations are adapted here at the prompt level, with no embeddings and no extra API calls.
Semantic repulsion estimates the default response distribution and moves away from its repeated
concepts ([arXiv 2606.09587](https://arxiv.org/html/2606.09587v1)). Verbalized sampling asks for an
explicit spread of candidates instead of one best answer
([arXiv 2510.01171](https://arxiv.org/html/2510.01171v3)).

The writing rules come from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
CC BY-SA 4.0, paraphrased and reorganised, together with frequency studies on excess vocabulary
([Science Advances 2025](https://doi.org/10.1126/sciadv.adt3813)), style comparison
([PNAS 2025](https://doi.org/10.1073/pnas.2422455122)), and detection accuracy among frequent users
([ACL 2025](https://arxiv.org/abs/2501.15654)).

## Prior art

Good work exists on the parts this combines, and credit belongs with it.

[machinesoul11/anti-sycophant-ai-agent-skills](https://github.com/machinesoul11/anti-sycophant-ai-agent-skills)
for premise testing and for the explicit off switch pattern, which is borrowed here.
[Dimerin1/honest-audit](https://github.com/Dimerin1/honest-audit) named the manufactured filler
criticism failure. [acost1a/murderboard](https://github.com/acost1a/murderboard),
[zszendro/vc-teardown](https://github.com/zszendro/vc-teardown) and
[SanketSapkal/founder-skills](https://github.com/SanketSapkal/founder-skills) shaped the adversarial
teardown and the explicit verdict. [sirbuggington/no-bs](https://github.com/sirbuggington/no-bs) and
[hoodini/ai-agents-skills](https://github.com/hoodini/ai-agents-skills) cover anti-sycophancy tone.
[maxgoff/unslop](https://github.com/maxgoff/unslop) covers banned phrase discipline.

What none of them do is attack convergence directly. They fix tone, or they fix rigour. None names the
consensus answer and bans it, and none requires differentiation to be derived from the user's own non
transferable assets. That gap is the reason this repository exists.

## Contributing

Read [RUBRIC.md](RUBRIC.md) for what a skill has to contain, then [STYLE.md](STYLE.md) for the house
style, which is enforced in CI, then [CONTRIBUTING.md](CONTRIBUTING.md) for the mechanics. The
`skill-forge` skill walks through authoring one.

## Licence

MIT. See [LICENSE](LICENSE).
