# Worked reports

Three runs of the procedure, each on a different kind of question, so the shape is concrete before you
apply it. The links here are placeholders written as example.org on purpose, because the point is the
structure of the claim table and the report, not the specific evidence. In a real run every link
resolves to a real page you opened.

## Run one, a claim check

Question as asked: is it true that a raw egg contains more protein than a large banana?

Decomposition in step 1:
- How much protein is in one large chicken egg?
- How much protein is in one large banana?
- Are the two figures measured the same way, per item or per hundred grams?

Search notes. The deciding sub-question turned out to be the third, because a per hundred gram
comparison and a per item comparison give opposite framings. Both foods have public nutrient data from
a government database, which is independent and primary.

Claim table:

```
Claim                                  Source                Date        Grade                    Confidence
One large egg has about 6 g protein    fooddata.example.gov  2025-02-10  independent/slow/primary  Established
One large banana has about 1.3 g       fooddata.example.gov  2025-02-10  independent/slow/primary  Established
Per 100 g egg has ~13 g, banana ~1.1 g fooddata.example.gov  2025-02-10  independent/slow/primary  Established
```

Report:

```
ANSWER
Yes, on any normal serving. A large egg has about 6 g of protein against about 1.3 g in a large
banana. Confidence Established.

WHAT IS ESTABLISHED
Egg and banana protein figures, both from the same government nutrient database, dated 2025-02-10.

WHAT IS CONTESTED
Nothing found.

WHAT I COULD NOT ESTABLISH
Nothing material. The claim is settled by public nutrient data.

WHAT WOULD CHANGE THE ANSWER
Only a different definition of serving, which the question did not raise.
```

## Run two, a vendor comparison

Question as asked: which of two managed database services is cheaper for a small always on workload?

Decomposition:
- What does each vendor charge for the smallest always on instance?
- What is billed on top, meaning storage, egress, and backups?
- What has changed in the last quarter, since pricing is volatile?

Search notes. Each vendor is a primary source for its own prices and an interested source for the
comparison, so the price rows are gradeable but the recommendation cannot come from either vendor's
own comparison page. One independent teardown was found and dated.

Claim table:

```
Claim                                     Source                   Date        Grade                       Confidence
Vendor A base instance is X per month     a-vendor.example/pricing 2026-01-05  interested/volatile/primary Likely
Vendor B base instance is Y per month     b-vendor.example/pricing 2026-01-05  interested/volatile/primary Likely
Egress dominates the bill above 200 GB    indep-teardown.example   2025-11-20  independent/volatile/secondary Contested
```

Report:

```
ANSWER
On the base instance alone vendor A is cheaper, but egress can reverse that above a few hundred
gigabytes a month. Confidence Likely on the base, Contested on the crossover.

WHAT IS CONTESTED
The egress crossover point. The independent teardown puts it near 200 GB; vendor A's own page implies
higher. Evidence leans toward the teardown because it is independent.

WHAT I COULD NOT ESTABLISH
The user's actual monthly egress, which decides the answer. Named as the open question.

WHAT WOULD CHANGE THE ANSWER
A measured egress figure from the user's current traffic.
```

## Run three, a question public sources cannot settle

Question as asked: how many private companies in one city use a specific niche framework in production?

Decomposition showed no public register tracks this. Job postings and a language survey were the only
proxies, both weak.

Report:

```
ANSWER
This cannot be settled with public information. The best available reading is a lower bound from job
postings, which named a handful of firms, with no way to count the rest. Confidence Unknown.

WHAT I COULD NOT ESTABLISH
The population itself. No public register exists, and the proxies undercount private and internal use.

WHAT WOULD CHANGE THE ANSWER
A direct survey of the local user group, or access to the framework vendor's private customer list.
```

The lesson across all three: the honest report often ends on what could not be found, and that ending
is the result rather than a failure to reach one.
