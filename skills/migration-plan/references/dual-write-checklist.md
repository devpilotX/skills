# Dual write and shadow read checklist

The main file gives the dual write pattern in one paragraph: write to both, keep reading from the old
one, read the new one in parallel and compare, move reads at a sustained zero mismatch, then stop
writing to the old one after a safety period. This breaks that into ordered stages, with the exit that
stays open at each one and the trap that ends the stage early.

## Stage 1, write to both, read the old one

Start writing every change to both the old and the new store. Keep serving all reads from the old store.
Nothing a user sees depends on the new store yet.

Exit open: stop writing to the new store and delete it. Nothing depends on it.

Trap: a write that succeeds on the old store and fails on the new one. Decide up front whether the write
overall fails or the divergence is logged and reconciled. Logging and reconciling keeps the old store
authoritative, which is what you want at this stage.

## Stage 2, backfill the history

The dual write only captures new changes. Backfill the existing records into the new store, in batches,
resumable, verified per batch by count and checksum as the main file's backfill step requires.

Exit open: the new store is still read by nobody, so a bad backfill is thrown away and rerun.

Trap: running the backfill at full speed against production load and saturating the source. Pace it and
watch the source's own metrics.

## Stage 3, shadow read and compare

For each read served from the old store, also read from the new store, and compare the two results
without using the new one. Record every mismatch with enough context to find its cause. Report the
mismatch rate.

Exit open: turn off the shadow read. It never affected a response.

Trap: treating a non zero mismatch rate as acceptable and moving on. Every mismatch is a parity bug,
usually one of the undocumented behaviours from the inventory. Fix the cause, do not tune the
threshold. The bar is a sustained zero, not a low number.

## Stage 4, move reads to the new store

When the mismatch rate has held at zero for a sustained period, switch reads to the new store. Keep
writing to both. The old store is now a live backup that receives every write.

Exit open: switch reads back to the old store instantly. It is fully current because dual write never
stopped.

Trap: switching reads before the mismatch rate has been zero long enough to cover the slow and rare
code paths. A path exercised once a day needs more than a day of clean comparison.

## Stage 5, stop writing to the old store

After a safety period reading from the new store with no problem, stop writing to the old store. This is
the point the main file names: usually the moment writes stop going to the old system is the point of no
return. Prepare for it specifically.

Exit open: this is where the easy exit closes. Returning now means the old store is stale by however
long writes have stopped. Keep it readable but know that a return requires a reverse backfill.

Trap: crossing this point without a written decision. It should be a deliberate, announced step, not a
side effect of a config cleanup.

## Stage 6, decommission

After the old store has been idle long enough to be sure nothing needs it, remove it. Then remove the
dual write code, the comparison code, the backfill runner, and the routing shim. The main file is
firm that a migration leaving its scaffolding behind has added complexity rather than removed it.

Exit open: none. The migration is complete. Record what it actually cost against the estimate.

## The rule that runs through every stage

The old store stays authoritative until stage 4, and stays a live backup until stage 5. That ordering is
what keeps every step before the point of no return reversible. Do not let a convenience, such as
turning off dual write early to save cost, collapse two stages into one and remove the exit before you
meant to.
