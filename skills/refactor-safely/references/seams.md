# Seams

A seam is a place where you can change behaviour without editing the code at that place. Untestable code is
usually code with no seam: a dependency is constructed or reached in the middle of the logic, so a test
cannot substitute it. This is a catalogue of the smallest safe ways to add one.

Creating a seam is itself a refactor. It preserves behaviour, so it lands as its own commit with the suite
green before you use the seam to write a test.

## Parameter with a default

The smallest seam. Add a parameter whose default equals the value currently hardcoded, so no existing
caller changes and no behaviour moves.

```
# before
def report():
    now = SystemClock.now()
    ...

# after
def report(clock=SystemClock):
    now = clock.now()
    ...
```

Every existing call still passes nothing and gets the system clock. A test passes a frozen clock. Behaviour
for real callers is identical, which is what makes this safe.

## Extract and override

When a method reaches an untestable dependency inline, pull that part into its own method on the same
object, then override it in a test only subclass.

```
# before
class Importer:
    def run(self):
        rows = Database.query("select ...")
        return transform(rows)

# after
class Importer:
    def run(self):
        rows = self.fetch_rows()
        return transform(rows)
    def fetch_rows(self):
        return Database.query("select ...")
```

The production path is unchanged: `run` still calls `fetch_rows`, which still queries the database. A test
subclass overrides `fetch_rows` to return fixed rows and exercises `transform` without a database.

## Wrap a global or a direct constructor

When code reaches a global or constructs a concrete dependency in the middle of logic, put a function in
front of it that a test can replace.

```
# before
def handle(request):
    client = PaymentClient(API_KEY)
    return client.charge(request.amount)

# after
def make_payment_client():
    return PaymentClient(API_KEY)

def handle(request, client_factory=make_payment_client):
    client = client_factory()
    return client.charge(request.amount)
```

The default factory builds the same client with the same key, so real behaviour is untouched. A test passes
a factory that returns a fake client and asserts on the charge.

## Introduce an interface at the boundary you do not own

When the dependency is a third party service, define the narrow interface your code actually uses, adapt
the real client to it once, and depend on the interface.

```
# after
class Notifier:
    def notify(self, user_id, message): ...

class EmailNotifier(Notifier):
    def notify(self, user_id, message):
        self.mailer.send(lookup_email(user_id), message)
```

Production wires the real `EmailNotifier`. A test wires a recording double that captures the calls. The
behaviour of the real path is the same as before the interface existed.

## The rule that keeps a seam safe

A seam must not change what real callers do. If adding the seam changes a single production behaviour, it
is not a seam yet, it is a behaviour change wearing a refactor's clothes, and it belongs in a separate
commit with its own test. Run the suite after adding the seam and before writing the first test through it,
so you know the seam alone preserved behaviour.

## Choosing which seam

Prefer the parameter default when the dependency is passed as a value, because it is the least invasive.
Reach for extract and override when the dependency is buried in a method you cannot change the signature
of. Wrap a global when the dependency is reached rather than passed. Introduce an interface when the
dependency is external and you want the test double to stay honest against the real contract.
