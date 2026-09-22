# Offline models and conflict rules

The offline model decides most of the app's data code, so pick it before the screens. The three models
below are not points on a slider. Each one is a different application, and moving from one to the next
after launch is close to a rewrite.

## The three models

Read only cache. The app reads from a server, keeps the last response, and shows it when there is no
connection. Writes either fail offline or are disabled. This is the cheapest model and the right one for
an app that mostly displays server owned data: a transit schedule, a news reader, a catalogue.

Queued writes. The app records the user's changes locally, applies them to the visible state at once,
and sends them when the connection returns. The user keeps working offline and sees their edits
immediately. This is the common case for note taking, task lists, and forms. The cost is that every
queued operation needs an idempotency key and a durable store, and you must decide what happens when the
server rejects a queued change.

Full sync with conflict resolution. Both the device and the server can change the same record while
disconnected, and the app reconciles the two versions. This is correct for collaborative editing and for
data edited on several devices by the same user. It is the most work by a wide margin, because you carry
version vectors or timestamps per record and a merge that a user can understand.

## Choosing between them

| Question | Read only cache | Queued writes | Full sync |
| --- | --- | --- | --- |
| Can the user create or edit offline | No | Yes | Yes |
| Can two clients edit the same record offline | No | Rarely | Yes |
| Local storage needed | Last response | Durable write queue | Full record store plus versions |
| Idempotency keys required | No | Yes | Yes |
| Conflict handling | None | Reject or retry | Merge |
| Rough effort | Low | Medium | High |

Pick the lowest row that the product actually needs. Building full sync for an app where only one device
ever edits a record is paying for a merge that never runs.

## Conflict rules for queued writes and sync

Last write wins. The most recent change by wall clock replaces the other. Simple to build and it loses
data silently, because the user whose change was discarded is never told. Acceptable for a status field
where only the latest value matters. Wrong for anything the user typed at length.

Server authority. The server's version wins on conflict and the client's change is dropped or bounced
back for the user to redo. Predictable and easy to reason about. The cost is discarded user work, so the
interface has to show that a change did not stick rather than pretending it did.

Field level merge. Two edits to different fields of the same record both survive; only edits to the same
field conflict. More work and far fewer visible conflicts. Good for a profile or a settings record with
many independent fields.

Value merge. For sets and counters, a data type that merges by construction removes the conflict. Adding
two different tags offline can union cleanly without a rule.

Whatever the rule, decide what the user sees when their change is rejected, and build that path. A silent
loss is the failure users remember.

## Queue mechanics that always apply

Give every queued operation an idempotency key generated on the device, so a retry after a flaky
connection does not create a duplicate.

Store the queue durably, in the local database, not in memory. The process will be killed before the
network returns, and an in memory queue is gone.

Order the queue and respect dependencies. A create followed by an update to the same record must send in
that order, or the update hits a record the server has not seen.

Cap retries and surface a permanent failure. A queued write that has failed twenty times needs the user
told, not an infinite background loop draining the battery.

Show sync state per item where it matters: pending, syncing, synced, failed. A single global spinner
hides which change is stuck.

## Worked example, a task app

The product lets one user manage tasks across a phone and a tablet, edit offline, and see edits appear at
once. Two devices editing the same task offline is possible but rare.

Model: queued writes, not full sync, because same record concurrent editing is rare enough that a simple
rule is acceptable. Conflict rule: server authority on the whole task record, with the interface showing
"this task changed on another device" and offering the user both versions to pick from. Storage: a local
tasks table plus an operations queue table, each operation carrying an idempotency key and a created
timestamp. On reconnect, the queue drains in order, and any rejected operation raises the reconcile
prompt rather than vanishing.
