# Consensus firewall

Method for phases 1 to 3. It has to be mechanical, because "try to be original" does not work.
Originality here is produced by subtraction.

## Why subtraction

A model answering a common question walks toward the densest region of its training distribution.
That is the design, not a defect. Independent human respondents spread out. Independent model samples
cluster ([arXiv 2501.19361](https://arxiv.org/html/2501.19361v1)). The same clustering shows up in
ideation studies, where users of one assistant produced less semantically distinct ideas than users
of a different tool ([arXiv 2402.01536](https://arxiv.org/abs/2402.01536)).

You cannot instruct the centre away. You can locate it and step off it. Two published techniques
inform the method here. Semantic repulsion estimates the default response distribution, pulls out its
repeated concepts, and treats them as negatives to move away from
([arXiv 2606.09587](https://arxiv.org/html/2606.09587v1)). Verbalized sampling asks for an explicit
set of candidates with their likelihoods instead of one best answer, which recovers diversity lost to
mode collapse ([arXiv 2510.01171](https://arxiv.org/html/2510.01171v3)).

This file is the prompt level adaptation of both. No embeddings, no extra API calls. The estimate
gets written out in plain language and then banned.

Those research summaries were paraphrased for licensing compliance. Follow the links for the papers.

## Step 1, write the consensus answer

Ask: if a hundred thousand people sent this exact message today, what did they all get back?

Write three to six bullets. Be specific and fair, because a strawman defeats the purpose. Cover
whichever of these apply: the obvious framing of the problem, the obvious customer segment, the
obvious stack or platform or channel, the obvious first step, the obvious business model, and the
obvious encouragement.

## Step 2, recognise the tells

If a draft contains these, the centre was not escaped.

Start with an MVP, which replaces naming the one feature a buyer would pay for now.

Validate with a landing page, which replaces one conversation with a named qualified buyer.

Differentiate on user experience or customer service, which replaces a structural advantage a
competitor cannot copy.

Focus on a niche, which replaces naming the specific niche this user can reach and others cannot.

Use AI to automate it, which replaces asking whether the manual version is worth automating.

The market is growing at some percent a year, which replaces asking whether this buyer has budget
now.

Build an audience and monetise later, which replaces building something someone pays for.

Partner with established players, which replaces explaining why an established player answers the
email.

Start lean and iterate, which replaces the one fact that decides the whole thing.

It depends on execution, which replaces having an opinion.

Every one of those is true-ish and useless. Useless advice delivered bluntly is still useless.

## Step 3, ban and disclose

The bullets become a blacklist for the response. Print them for the user under a heading that makes
their function clear, such as "the answer everyone else got". Readmission needs either specific
evidence that the item applies to this user, labelled as the obvious move, or a reframing that shows
it is the trap.

## Step 4, generate wide before narrowing

At least five distinct angles. Force coverage of these five slots.

The inversion, where the premise is wrong and the opposite move is correct.

The boring one, unsexy and cash generating, which is why it is uncrowded.

The constraint-exploiting one, which only works because of a limitation this user has.

The adjacent one, the same capability aimed at a customer the user has not considered.

The unwelcome one, which is true and which the user will not like. The job, the partner, the timing,
the missing skill.

Tag each `COMMON`, `SEMI`, or `RARE` by how likely a typical assistant is to say it. Carry the rare
and semi-rare forward.

## Step 5, truth filter last

Order matters. Filter for commonness first and truth second, never the reverse, or the rare
candidates never get examined.

A rare idea that fails the phase 5 economics dies there. Being reflexively contrary is the consensus
inverted, which is equally derivative and usually worse. The target is the intersection of uncommon
and true, and it is a small set.

If nothing survives, say so. The honest output is that the obvious answer is correct here, with the
evidence, plus the part the crowd gets wrong anyway.
