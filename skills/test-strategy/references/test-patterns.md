# Test patterns

Worked patterns for tests that fail for the right reason and stay readable after the code moves. The
language here is generic; translate the shape into the framework the project already uses.

## Arrange, act, assert, in that order

Keep the three phases visually separate so a reader can find the assertion without parsing the setup.

```
def test_expired_card_is_rejected():
    # arrange
    card = Card(number="4111...", expiry="2020-01")
    gateway = FakeGateway()

    # act
    result = charge(card, amount_cents=500, gateway=gateway)

    # assert
    assert result.status == "declined"
    assert result.reason == "card_expired"
    assert gateway.calls == []
```

The last assertion matters as much as the first: an expired card must not reach the gateway at all.
Asserting only the status would pass even if the code called the gateway and then threw the result away.

## Name the test after the input and the outcome

A test name is read in the failure output long after the code is forgotten. State the condition and the
expected result. `test_empty_cart_totals_zero` beats `test_cart_2`. When the name needs the word "and", the
test is checking two behaviours and wants splitting.

## One behaviour per test

A test that asserts five unrelated things fails on the first and hides the other four. Split by behaviour,
not by method. Two tests that each fail for one reason localise a defect faster than one test that fails
for any of five.

## Build fixtures per test, not from a shared mutable base

A fixture that every test mutates accumulates state and couples tests to run order. Prefer a small factory
that returns a fresh object with sensible defaults and lets each test override the one field it cares
about.

```
def make_order(**overrides):
    defaults = dict(items=[item()], discount=None, currency="USD")
    return Order(**{**defaults, **overrides})

def test_discount_reduces_total():
    order = make_order(discount=Percent(10))
    assert order.total() == expected_after_discount
```

The test states only the field under test. A reader sees at once that the discount is the variable.

## Table driven cases for a family of inputs

When the same assertion holds across many inputs, drive it from a table so each case is one line and a new
case is one row.

```
cases = [
    ("empty", "", 0),
    ("single", "a", 1),
    ("trims", "  ab  ", 2),
    ("unicode", "cafe\u0301", 4),
]
for name, text, expected in cases:
    assert length(text) == expected, name
```

The name column turns a failing row into a readable message instead of an index.

## Wait for a condition, never sleep

A fixed sleep is either too short and flaky or too long and slow. Poll for the condition with a timeout.

```
def wait_until(predicate, timeout_seconds=5):
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition not met within timeout")
```

## Freeze the clock and seed randomness

Inject the clock and the random source so a test controls both. Print the seed on failure so the failing
case can be replayed exactly.

```
def test_token_expires_after_one_hour():
    now = FrozenClock("2024-01-01T00:00:00Z")
    token = issue_token(clock=now)
    now.advance(hours=1, seconds=1)
    assert token.is_expired(clock=now)
```

## The bug fix test comes first

Write the test that reproduces the reported bug, watch it fail, then fix the code and watch it pass. A
test written after the fix, that has never been red, proves only that the code does what it currently does.
