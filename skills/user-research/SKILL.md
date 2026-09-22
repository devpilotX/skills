---
name: user-research
description: Learn what users actually do rather than what they say they will do, in any product or market: decide whether research is the right spend, recruit people who have the problem, ask non-leading questions that request the last concrete instance instead of general habits, listen for behaviour and workarounds over stated preference, know how many conversations before the pattern repeats, and synthesise so the findings survive a sceptic. Use when planning user interviews, when a team is about to build on assumptions, when survey questions need writing, when interview notes need turning into decisions, or when research is being used to ratify a choice already made. Triggers on talk to users, run user interviews, write survey questions, how many users should we interview, what should we ask, validate this idea, are we building the right thing, synthesise interview notes, customer discovery, jobs to be done, is this feedback reliable, user needs.
license: MIT
compatibility: Any product, service, or market, business to business or consumer, at any stage.
metadata:
  version: 1.0.0
  suite: skills
---

# User research

A team about to build something asks users if they want it, users say yes to be agreeable, and the team
ships to silence. The failure is not talking to users, it is asking questions that produce comfortable
answers: leading questions, requests for predictions, and general habit questions that people answer
with an idealised version of themselves. This skill keeps research pointed at what people have actually
done, recruits the people who have the problem, and separates what was observed from what was inferred,
so the output survives a sceptic instead of flattering the plan.

## Fit to the project

Read the decision and the existing evidence before recruiting anyone.

1. Find the decision the research feeds. A roadmap doc, a spec, or a pitch. Research with no decision
   attached becomes a comfort exercise, so identify what will be done differently depending on the
   answer.
2. Check what evidence already exists: past interviews, support tickets, usage analytics, sales call
   notes, churn reasons. Often the answer is already in the building, and new interviews would repeat
   known findings at a cost.
3. Identify who actually has the problem, not who is easy to reach. The people available in your
   network or your existing user base are often the wrong sample, and a wrong sample gives a confident
   wrong answer.
4. Confirm the question is one research can answer. Whether people want a thing is answerable by
   watching behaviour. Whether a specific design will succeed is usually answerable only by shipping or
   testing, which belongs elsewhere.

## Non-negotiables

1. Attach the research to a decision before starting. Research with no decision behind it produces
   interesting notes nobody acts on, and it trains the team to treat research as theatre.
2. Recruit people who have the problem, not people who are available. A sample of convenience answers
   confidently and wrongly, because the people easiest to reach are rarely the people whose behaviour
   you need to understand.
3. Ask about the last concrete instance, not about general habits or future intentions. People
   describe an idealised self and predict badly, so "tell me about the last time you did X" beats "do
   you usually do X" and both beat "would you do X".
4. Never lead the witness. A question that contains the answer you hope for gets that answer back and
   teaches you nothing, because the respondent reads what you want and obliges.
5. Separate what you observed from what you inferred in every note. An inference recorded as an
   observation becomes a false fact the team builds on, and the two are impossible to untangle later.
6. Do not let research ratify a decision already made. If the plan will not change whatever the
   research finds, the research is a cost with no purpose, and running it anyway corrupts the next
   honest study.

## Procedure

### Step 1, decide whether to research at all

Write the decision the research feeds and what each possible finding would change. If no finding would
change the plan, stop: this is not research, it is reassurance, and it wastes the participants' time
and yours. Check whether existing evidence already answers the question before recruiting anyone new.

### Step 2, recruit for the problem

Define the person who has the problem in terms of behaviour, not demographics: someone who did X in the
last month, not someone aged 25 to 34. Screen for it with a question about recent behaviour, because a
screener that asks whether someone is interested lets everyone in. Aim to talk to people across the
range of the problem, including those who tried a solution and abandoned it, since the abandoners
carry the sharpest lessons.

### Step 3, write questions that do not lead or predict

Open with the last concrete instance: "walk me through the last time you ran into this". Follow the
story rather than a script, and ask why at each turn. Avoid three question shapes: the leading question
that names the answer, the hypothetical that asks for a prediction, and the general habit question that
invites an idealised self. When a participant states a preference, ask for the last time they acted on
it, because the gap between the two is the finding. The question shapes that lie and the ones that get
truth are in `references/question-design.md`.

### Step 4, listen for behaviour and workarounds

The signal is what people do, especially the workarounds they built to cope. A spreadsheet someone
maintains by hand, a tool used for something it was not made for, a step they skip: these reveal real
needs more reliably than any stated preference. Note the emotion too, since frustration points to a
problem worth solving. Record exact words where you can, because a paraphrase quietly inserts your
interpretation.

### Step 5, run enough conversations to see the pattern

Keep going until new conversations stop producing new patterns, the point of saturation. A rule of
thumb from usability research is that five to eight conversations per distinct user segment surface
most of the recurring patterns, and past a dozen in one segment you are usually confirming rather than
discovering. If patterns are still shifting after a dozen, your segments are mixed and need splitting.
Interview across segments separately rather than pooling them.

### Step 6, synthesise so it survives a sceptic

Group observations into patterns, and for each pattern cite the specific instances behind it with the
participants' own words. Mark every claim as observed or inferred. Then attack your own synthesis:
would a sceptic who wanted the opposite conclusion be able to find it in the same notes. A pattern that
rests on one enthusiastic participant is not a pattern. State how many participants showed each pattern
and how many did not. The full method for building patterns and the sceptic test is in
`references/synthesis.md`.

### Step 7, report findings tied to the decision

Report what you learned against the decision from Step 1: what the evidence supports, what it does not,
and what it changed. Separate the strong findings, seen across participants, from the weak signals worth
watching. Name what you still do not know. A finding that maps to no decision is a note, and it belongs
in an appendix rather than the summary.

## Self-audit

- The research is tied to a written decision, and each possible finding maps to a change in the plan.
- Participants were recruited for having the problem, screened on recent behaviour, not for being
  available.
- Questions ask about the last concrete instance, and none of them lead, predict, or ask about general
  habits.
- Notes record behaviour and workarounds, with participants' own words where possible.
- Every claim in the synthesis is marked as observed or inferred.
- The number of conversations reached saturation within each segment, and segments were kept separate.
- Each pattern names how many participants showed it and how many did not.
- No finding was used to ratify a decision that would not have changed regardless.

## Honest limits

This skill runs qualitative discovery to learn what users do and need. It does not measure how many
users behave a certain way: a qualitative sample cannot produce a reliable percentage, and quantifying
a behaviour needs analytics or a survey with a real sample, which touches `data-analysis`. It does not
test whether a specific design or change works, which is a controlled comparison owned by
`growth-experiment`. It does not decide what to build from the findings, which is a product judgement.
Interviews reveal problems well and predict adoption poorly, so a stated intention to buy or use is a
weak signal until behaviour confirms it.

The saturation and sample size figures here are rules of thumb from usability practice, not laws. A
narrow question saturates faster and a diverse population needs more conversations, so treat the numbers
as a starting point and stop when new interviews genuinely stop teaching you anything.

## Off switch

If the user says "stop", "just execute", or "just talk to a few people", stand down and drop the
full protocol. The skill stays quiet for the session unless the user asks for the method.
