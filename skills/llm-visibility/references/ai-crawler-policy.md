# AI crawler policy and the traffic tradeoff

Deciding which AI crawlers to allow is a business decision with a real cost on each side. This file lays out the categories and the tradeoff so the choice is made with eyes open, not by copying a robots.txt from a blog post.

## Two different kinds of access

Training access is a crawler collecting content to train or update a model. Blocking it keeps the content out of future model weights, but has no direct effect on whether the site appears in a live answer today.

Retrieval access is a crawler fetching pages in real time to answer a specific user question, then citing the source. Blocking it removes the site from that assistant's live answers and from any referral clicks those citations bring.

These are separate decisions controlled by separate user agents. A common position is to allow retrieval, so the site can be cited and earn referrals, while blocking or allowing training according to how the owner feels about their content being used that way. Conflating the two is the most frequent mistake, because a blanket block of everything AI also blocks the crawler that would have cited you.

## The tradeoff to state before blocking

Allowing retrieval crawlers can bring citations and referral traffic, at the cost of the content being read and summarised by the assistant, which sometimes answers the user without a click.

Blocking retrieval crawlers protects content from being summarised, at the cost of disappearing from that assistant's answers entirely while competitors who allowed it get cited instead.

There is no default that is correct for every site. A publisher that lives on ad impressions weighs the click loss differently from a business that wants to be named as the authority in its field. Present both sides and let the owner choose.

## How to express the policy

The allow and disallow rules go in robots.txt keyed by user agent, the same mechanism as any other crawler. Some crawlers also honour response headers for finer control. Whatever the mechanism, keep the rules readable and documented so the next person knows why each line is there.

Robots rules are honoured voluntarily. A well behaved crawler obeys them; the rule does not enforce itself against one that ignores it. State this so the owner does not treat a robots disallow as a hard security control.

## Keeping the list current

The set of AI crawlers and their user agent strings changes as assistants launch and rename their bots. A policy written once goes stale. Re-check the user agents against current published lists periodically rather than trusting a snapshot, and confirm from server logs which crawlers are actually visiting.

## Measuring the effect of the choice

After setting a policy, watch two things. In server logs, confirm the intended crawlers are or are not visiting as expected. In the citation baseline from the main skill, watch whether the site's presence in answers changes after an allow or block. The policy is only doing what you think if the logs and the citations agree with the intent.
