<!-- lint-exempt: vocab,vocab-density,chatter,significance-padding,copula-avoidance,participle-tail -->
# Worked rewrites

Every example below quotes machine phrasing in order to fix it, so this file opts out of the six rules
those quotes would trip. The lint report prints that list.

Each rewrite shows the original, the diagnosis as a list of tell and fix, the result, and what the
rewrite could not do without asking the author for facts. That last part matters: most of these
sentences are empty, and no amount of editing fills them.

## 1. Encyclopedic paragraph

Before:

> Gallery 825 serves as a vital cultural hub that has played a pivotal role in the evolving landscape of
> Los Angeles contemporary art, showcasing emerging talent and fostering dialogue between artists and the
> community, cementing its legacy as a cornerstone of the local scene.

Diagnosis:

- `serves as a` and `has played a pivotal role in` replace a copula. Fix: write `is`.
- `vital`, `pivotal`, `evolving landscape`, `showcasing`, `fostering`, `cornerstone` are tier one words.
- `cementing its legacy` is a participial tail making an unsourced claim about importance.
- Nothing in the sentence is checkable. It would fit any gallery in any city.

After:

> Gallery 825 is the exhibition space of the Los Angeles Art Association, at 825 North La Cienega
> Boulevard. It shows work by artists who are association members and holds roughly twelve exhibitions a
> year.

What the rewrite needed from the author: the address, the parent organisation, the exhibition count. The
original contained no facts, so the rewrite had to get them from somewhere. Where they were unavailable,
the honest output is two sentences shorter, not the same length with softer adjectives.

## 2. README opening

Before:

> This powerful and robust library provides a seamless, developer-friendly experience for handling date
> and time operations. Leveraging modern JavaScript features, it offers a comprehensive suite of
> utilities designed to streamline your workflow and enhance productivity.

Diagnosis:

- `powerful`, `robust`, `seamless`, `leveraging`, `comprehensive`, `enhance` are tier one or tier two.
- `developer-friendly experience` and `streamline your workflow` are claims with no test attached.
- Two sentences, forty three words, and the reader still does not know what it does or what it costs.
- No install line. A reader arriving at a README has a task.

After:

> Parses, formats and compares dates without pulling in a timezone database. 4 kB minified, no
> dependencies, works in Node 18 and every browser released since 2021.
>
> ```
> npm install tinydate
> ```
>
> It does not do calendar arithmetic across timezones. If you need that, use Temporal or Luxon.

What changed: every adjective became a measurement, and the limitation became a section instead of an
omission. The last line loses a sale and earns the reader's trust, which is the better trade for a
library.

## 3. Commit message

Before:

> Update authentication module
>
> This commit introduces several important improvements to enhance the robustness and security of the
> authentication flow, ensuring a more seamless user experience while maintaining backwards
> compatibility.
>
> Co-authored-by: AI Assistant

Diagnosis:

- The subject says nothing a reader can act on. Which module, and what changed?
- `important improvements`, `enhance`, `robustness`, `seamless` are padding around an unstated change.
- `ensuring a more seamless user experience` is a participial tail with no evidence.
- The body restates the diff instead of giving the reason.
- The attribution trailer names a tool and tells a reviewer nothing about the change.

After:

> lock the account for 15 minutes after 10 failed logins
>
> The previous limiter counted per IP, so a password spray from a botnet got unlimited attempts against
> one account. Counting per account closes that, at the cost of letting an attacker lock a known user
> out on purpose.
>
> Chose the lockout over a CAPTCHA because we have no CAPTCHA provider and adding one is a bigger
> decision than this fix.

What changed: the subject names the behaviour, the body gives the attack it stops and the new weakness
it introduces, and the third paragraph records the alternative rejected so nobody relitigates it.

## 4. Email

Before:

> Hi Sarah,
>
> I hope this email finds you well! I wanted to reach out and touch base regarding the project we
> discussed previously. I was wondering if you might have any updates you could share, as we are keen to
> align our timelines moving forward.
>
> Please don't hesitate to let me know if you have any questions.
>
> Best regards

Diagnosis:

- Three sentences before the ask, and the ask is vague when it finally arrives.
- `I hope this email finds you well`, `wanted to reach out`, `touch base`, `don't hesitate to let me
  know` are pleasantries carrying no information.
- `align our timelines` hides the actual question, which is a date.
- The reader has to infer what is wanted and by when.

After:

> Hi Sarah,
>
> Can you confirm whether the API contract lands before 14 October? We are holding the client build on
> it, and if it slips past that we will stub the endpoints and rework later.
>
> If the date is uncertain, a rough week is enough to plan around.
>
> Thanks

What changed: the ask is first, the reason the date matters is stated, and the fallback tells the reader
that an imprecise answer is still useful, which is what actually gets a reply.

## 5. Significance padding in a blog post

Before:

> In today's rapidly evolving digital landscape, the importance of observability cannot be overstated. As
> systems grow increasingly complex, teams must delve into a myriad of tools to gain valuable insights
> into their infrastructure, ultimately fostering a culture of reliability.

Diagnosis:

- `In today's`, `evolving landscape`, `delve`, `myriad`, `valuable insights`, `fostering`, `ultimately`.
- `cannot be overstated` is an importance claim standing in for a reason.
- `increasingly complex` is true of everything and therefore says nothing.
- The paragraph is a throat clear. Delete it and the piece starts better.

After:

> We were down for forty minutes before anyone noticed, because the only alert we had fired on CPU and
> the CPU was fine.

What changed: the abstraction became the incident that motivated the piece. This is the most common
single improvement available in a draft: cut the opening paragraph and start at the specific thing that
happened.

## 6. A clean passage that should be left alone

Before:

> The parser is recursive descent, which was a mistake. Expression nesting deeper than about thirty
> levels overflows the stack, and we found that when a generated config file nested ternaries forty deep.
> Rewriting it as a Pratt parser is on the list and has been for two years.

Diagnosis: none. Plain copulas, a specific failure, a number, an admission, and a dated piece of
self criticism. The rhythm is uneven and one sentence runs long.

After: unchanged.

This example exists because the most common failure when applying this skill is editing text that was
already fine. A passage with no tells and a real fact in every clause gets left alone. Reporting it as
clean, in one line, is the correct output.
