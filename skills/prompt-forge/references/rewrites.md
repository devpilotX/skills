# Rewrites by defect

One before and after for each of the six defects. Each pair shows the failing prompt, the output it
tends to produce, and the fix that removes the defect. Read the defect list in SKILL.md first; this
file is the worked demonstration of it.

## Defect one, no success criteria

Before:

```
Write a product description for my running shoe.
```

What arrives: a paragraph of adjectives that could describe any shoe, because nothing said how anyone
would know the description worked.

After:

```
Write a product description for a road running shoe aimed at first time marathon runners. A reader
should be able to tell in one sentence whether the shoe suits a heavier runner on hard pavement. Do
not claim any feature not in this list: 10 mm drop, 280 g, carbon plate, 6 mm outsole.
```

The criterion is checkable by someone who did not write it, and the feature list stops invention.

## Defect two, missing context that only the user has

Before:

```
Help me write a cold email to a potential client.
```

What arrives: a generic template with placeholder brackets, because the model has none of the context
that makes an email land.

After:

```
Write a cold email to the head of operations at a mid sized logistics firm. We already met once at a
trade show in March and they asked us to follow up after their Q2. We sell route planning software
that cut fuel spend 8 percent for a similar firm. Keep it under 120 words and end with one specific
ask for a 20 minute call.
```

The meeting, the timing, and the proof point are facts only the user had.

## Defect three, no output contract

Before:

```
Summarise this contract for me.
```

What arrives: a summary at whatever length and shape the model chose, often needing manual reworking.

After:

```
Summarise this contract as a table with three columns: clause, plain language meaning, and risk to us
rated low, medium, or high. Cover only termination, liability, and payment terms. Skip the boilerplate.
```

Format, scope, and what to leave out are all now specified.

## Defect four, multiple requests fused into one

Before:

```
Analyse our sales data, find the trends, build a forecast, and write an executive summary.
```

What arrives: a shallow pass at each of four tasks, none done well.

After, split into a sequence:

```
Step 1: from the attached sales data, list the three largest month over month changes and what drove
each. Wait for my confirmation before forecasting.
```

Splitting the tasks is usually the whole fix. Each step gets full attention and the user checks the
first before the next.

## Defect five, no failure instruction

Before:

```
What is the market size for electric cargo bikes in our region?
```

What arrives: a confident number with no source, because the default on uncertainty is to guess
fluently.

After:

```
Estimate the market size for electric cargo bikes in our region. If you do not have a reliable figure,
say so and list what data would settle it rather than guessing. Cite any number you do give.
```

The failure instruction turns a fabricated number into an honest gap.

## Defect six, leading or flattering framing

Before:

```
Explain why microservices are the right architecture for our app.
```

What arrives: advocacy, because the prompt asked for a conclusion rather than an analysis.

After:

```
Assess whether a microservices architecture fits our app. Give the strongest case for it, the
strongest case against, and the conditions under which each wins. We are a team of four with one
deployment target.
```

The neutral framing and the team size produce analysis instead of a sales pitch.

## Reading the pairs

Across all six, the fix adds a fact, a criterion, or a constraint the model could not infer, and it
names what to do when the model is stuck. None of the fixes is longer politeness or a stronger
adjective, because those change nothing.
