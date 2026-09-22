# Cost causes in order of likelihood

When one line dominates a bill, the driver is usually one of a small set of causes. Check them roughly in this order, because the earlier ones turn out to be the answer more often. All figures here are rules of thumb, not measurements of your account.

## Idle and forgotten resources

The most common cause of surprise spend is something left running that nobody uses: a test environment nobody shut down, a database provisioned for a launch that slipped, an oversized instance from a load test, a load balancer with no traffic. These cost the same whether used or not.

Find them by looking for resources with near zero utilisation over a week: a database with almost no queries, a server with flat low CPU, a disk that is attached to nothing. Anything with no traffic and no owner is a candidate to turn off. Turn it off in a way you can reverse, and wait to see who complains before deleting.

## Over provisioned capacity

The second most common cause is capacity sized for a peak that rarely arrives, or copied from a template and never revisited. An instance at ten percent CPU all month is paying for ninety percent it never uses.

Right size to the observed load plus a headroom margin, not to the largest number anyone once imagined. Autoscaling helps here, but only if the floor is set sensibly; a minimum of ten instances that only ever needs two is over provisioning with extra steps.

## Data transfer and egress

Egress charges surprise people because they are invisible until the bill arrives. Data leaving a cloud, crossing regions, or crossing availability zones often costs more per gigabyte than storing it. A chatty service that crosses a zone boundary on every call, or a backup shipped out of the cloud daily, can dominate a bill quietly.

Look for cross zone and cross region traffic and for anything serving large files without a cache or content delivery layer in front.

## Storage that never dies

Storage accumulates because nothing deletes it. Old snapshots, log archives kept forever, orphaned volumes from deleted machines, and object stores with no lifecycle rule all grow without bound. Each item is small; the total is not.

Apply a lifecycle policy that moves cold data to cheaper tiers and deletes what has no retention requirement. Confirm the retention requirement before deleting anything.

## Logging and metrics volume

Observability is worth paying for, and it is also easy to overpay for. Logging every request at full verbosity, keeping traces for everything, and retaining all of it for a year produces a bill that rivals the compute it observes.

Sample high volume traces, drop debug logging in production, and set retention by what an investigation actually needs. Keeping errors and slow requests while sampling the rest cuts volume without losing the signal.

## Inefficient calls that multiply a unit charge

When the charge is per request, per token, per query, or per row scanned, an inefficient pattern multiplies it. A query with no index scanning the whole table, a loop that calls a paid API once per item instead of in a batch, or a cache that never hits all turn a small unit price into a large bill.

This one crosses into `performance-tuning`, because the fix is a better access pattern rather than a smaller resource. The cost view tells you where to look; the fix is a code change.
