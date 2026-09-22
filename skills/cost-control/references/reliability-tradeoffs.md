# Reliability tradeoffs in cost cuts

Many cost cuts are reliability decisions in disguise. The saving is immediate and visible; the cost arrives later as an outage, a slow recovery, or lost data. This file lists the cuts that carry a hidden reliability price so you can name the price and get it accepted before the cut ships.

## Removing redundancy

Dropping from two replicas to one halves the compute cost of that tier and removes the ability to survive a single failure. During normal operation nothing changes, which is exactly why it feels safe. The price is paid the day one instance dies and there is no second one to serve traffic.

Accept this only where the recovery time from a full restart is genuinely tolerable, and never for a stateful store where the replica is also the backup path.

## Shrinking headroom

Running instances close to their limit saves money on capacity that mostly sits idle. It also removes the buffer that absorbs a traffic spike or a slow dependency. A system at ninety percent utilisation has no room for the surge that a normal day occasionally brings, and it tips into failure under load that a roomier system would have shrugged off.

Keep enough headroom to absorb the largest normal spike plus the time it takes to scale up. Cutting below that trades a small monthly saving for an outage during your busiest hour.

## Lengthening recovery

Choosing a cheaper storage tier, a smaller backup frequency, or a cold standby instead of a warm one all save money and all make recovery slower. The question is how long the business can be down while the slower path restores service. A backup taken daily instead of hourly means up to a day of data can be lost, and a cold standby means minutes or hours of downtime while it starts.

State the recovery time and data loss the cut implies, and check it against what the business has agreed it can tolerate.

## Reducing backups

Fewer backups, shorter retention, or backups in the same failure domain as the primary all cut storage cost. They also raise the chance that when you need a backup, the one you need is gone or destroyed by the same event that took the primary. A backup in the same region as the data it protects does not survive a region loss.

Keep at least one backup in a separate failure domain, and test a restore, because an untested backup is a hope rather than a safeguard.

## Dropping observability

Cutting logging, metrics, or tracing to save money removes the ability to diagnose the next incident. The saving is real and the cost is that the next outage lasts longer because you are debugging blind. Sample and set retention deliberately rather than switching signals off.

## Aggressive autoscaling floors

Setting the autoscaling minimum very low saves money in quiet periods and adds latency when traffic returns, because there is nothing warm to serve the first requests while new capacity starts. For a spiky workload, a floor of zero means every spike begins with a cold start and a queue of waiting users.

Set the floor to cover the baseline load plus the startup time of new capacity, not to zero.

## How to present a cut

For every cut, write one line: what it saves, and what reliability it costs. A cut that reads "saves 40 percent, removes single failure survival for this tier" can be accepted or rejected honestly. A cut that reads only "saves 40 percent" hides the decision that matters.
