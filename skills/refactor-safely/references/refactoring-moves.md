# Refactoring moves

A catalogue of behaviour preserving moves, each with a before and after and the reason it is safe. One move
is one commit, and the suite runs green between each. The examples are generic; the shape carries to any
language.

## Rename for accuracy

The cheapest improvement and the one that prevents the most future defects, because a name that states the
wrong thing misleads every reader after you.

```
# before
d = get(u)      # what is d, what is u

# after
active_subscription = get_subscription(user)
```

Safe because the tool renames every reference at once. Run the type checker to confirm nothing was missed.

## Extract a function

Pull a block with a single purpose into a named function, keeping the parameter list short.

```
# before
total = 0
for line in order.lines:
    total += line.qty * line.unit_price
total = apply_tax(total, order.region)

# after
subtotal = sum_line_items(order.lines)
total = apply_tax(subtotal, order.region)
```

Safe because the extracted code runs identically; only its location changed. The name replaces a comment
that would have started "now we".

## Inline a function

The reverse, for a function that adds a name and no clarity.

```
# before
def is_zero(n): return n == 0
if is_zero(count): ...

# after
if count == 0: ...
```

Safe when the function has one caller and the inlined form reads at least as clearly.

## Replace a magic value with a named constant

Define the value once so it cannot drift between uses.

```
# before
if retries > 3: ...
sleep(3)

# after
MAX_RETRIES = 3
if retries > MAX_RETRIES: ...
```

Name each value for what it means, since two unrelated threes should not share a constant.

## Introduce a parameter object

When the same arguments travel together everywhere, group them.

```
# before
def price(weight, zone, promo): ...
price(w, z, p)

# after
def price(shipment): ...
price(Shipment(weight=w, zone=z, promo=p))
```

Safe because the values are the same; only their packaging changed. Do this when the group has meaning, not
to shorten a signature that is fine.

## Guard clause instead of nesting

Handle the failure cases at the top and return early, which flattens the code without changing it.

```
# before
def charge(card):
    if card.valid:
        if card.funds:
            return do_charge(card)
        else:
            return declined("no_funds")
    else:
        return declined("invalid")

# after
def charge(card):
    if not card.valid: return declined("invalid")
    if not card.funds: return declined("no_funds")
    return do_charge(card)
```

Safe because every path returns the same value it did before. Confirm by reading each original branch.

## Separate the decision from the action

Split the code that decides from the code that acts, so the decision becomes testable without performing
the action.

```
# before
def maybe_send(user):
    if user.opted_in and not user.bounced:
        mailer.send(user.email, welcome())

# after
def should_send(user):
    return user.opted_in and not user.bounced

def maybe_send(user):
    if should_send(user):
        mailer.send(user.email, welcome())
```

Now `should_send` can be tested with values alone, and the send stays a thin action. Behaviour is
unchanged: the same users receive the same mail.
