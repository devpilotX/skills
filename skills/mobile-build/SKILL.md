---
name: mobile-build
description: Build mobile applications that survive a bad network, a backgrounded process and a store review. Use when the user asks to build an iOS or Android app, asks about Swift, SwiftUI, Kotlin, Jetpack Compose, React Native, Flutter or Expo, asks about offline support, push notifications, app store submission, permissions, deep links, or asks why their app is rejected, slow, or draining battery. Treats the network as unreliable by default, plans the offline and conflict behaviour before the screens, budgets battery and data, and covers the store review rules that cause most rejections. Names the minimum supported version and the device class being targeted before any code. Triggers on build an iOS app, build an Android app, React Native, Flutter, SwiftUI, Jetpack Compose, offline support, push notifications, app store rejection, deep linking, mobile performance, battery drain.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Mobile build

Mobile differs from web in four ways that change the design: the network fails constantly, the operating
system can kill your process, distribution goes through a reviewer, and the battery is a shared resource
the user notices.

## Fit to the project

Before proposing anything, find out what the app already is. An existing app has a platform and a
minimum version you do not get to move without a reason.

Read the platform manifests: an iOS project's Info.plist and deployment target, an Android module's
build.gradle for minSdk, targetSdk and compileSdk, or the Expo and React Native config and the Flutter
pubspec. Those files name the platforms, the minimum operating system, and the permissions already
declared. Read them before you assume a target.

Check how the app stores data locally and whether any sync already exists, because the offline model
is the hardest thing to change later. Look for the store metadata that ships releases: the App Store
Connect configuration, the Play Console listing, the privacy declarations, the signing setup and the
build flavours. Note the accessibility posture too, meaning dynamic type support and screen reader
labels on the current screens.

When nothing is set, meaning a fresh app with no target chosen, stop at step 1 and decide the platform
strategy and the minimum version first, then treat every platform API as unverified until checked
against that minimum. Any Swift, Kotlin, Dart or TypeScript this skill writes follows the `code-craft`
contract for file layout, function length and comments.

## Non-negotiables

1. Decide the offline behaviour before building screens. Read only cache, queued writes, or full sync with conflict resolution are three different applications. Retrofitting the third is close to a rewrite.
2. Assume the process is killed at any moment. Anything not persisted is gone. State restoration is a requirement, not a refinement.
3. Never ship a secret in the binary. A mobile app is a client in someone else's hands and can be unpacked. API keys, private keys and signing secrets belong on a server.
4. State the minimum supported operating system version and the oldest target device, and check the feature availability of every API against it. Recall about platform version support is often wrong, so retrieve it.
5. Request a permission at the moment it is needed, with an explanation, never all at once on launch. Denial is a normal path that has to work.
6. Verify on a real device on a slow connection. A simulator on a fast desktop hides almost every problem that matters.
7. Read the current store review guidelines before submission rather than recalling them, since they change and rejection costs a review cycle.

## Procedure

### Step 1, decide the platform strategy honestly

Native, meaning Swift or Kotlin, gives the best performance, immediate access to new platform features,
and the best debugging. It costs two codebases when both platforms are needed.

React Native and Flutter share most logic across platforms and are a good fit for interface heavy
applications. They cost a bridge or an engine, a harder path for platform specific features, larger
binaries, and dependence on the ecosystem keeping up with platform releases.

A web application installed to the home screen is far cheaper and is limited in background work, push
support on some platforms, and hardware access.

Pick on the constraint that actually binds: team skill, the platform features required, and whether one
or two platforms must ship. Say which constraint decided it.

### Step 2, plan data and sync first

List what the user can do with no connection. That list determines the storage design.

For queued writes, decide the conflict rule now. Last write wins is simple and loses data silently.
Server authority is predictable and can discard user work. Merge is correct and the most work. Say which
one, and say what the user sees when their change is rejected.

Give every queued operation an idempotency key, because retries after a reconnect are certain.

Store queued work durably, not in memory, since the process will be killed before the network returns.

Show sync state in the interface. A user who cannot tell whether their change was saved will retry it.

The decision matrix for cache, queue and full sync, with what the user sees under each, is in
`references/offline-sync.md`.

### Step 3, build for interruption

Save draft input as it is typed, not on submit.

Restore scroll position, navigation stack and partially entered forms after a cold start.

Handle a resume after minutes, hours or days. Tokens will have expired and cached data will be stale.

Handle rotation, split screen, and a phone call arriving mid action.

Handle the app being opened from a notification or a deep link into an arbitrary screen, with no
navigation history behind it.

### Step 4, respect the shared resources

Network. Batch requests, deduplicate them, and cache with a stated freshness. Every wake of the radio
costs battery. Give every request a timeout and a retry with backoff.

Battery. Background work belongs in the platform's scheduler so the system can batch it, not in a timer.
Location at the lowest accuracy that works, and never continuously without a visible reason.

Data. Assume a metered connection. Size images for the device, and avoid downloading what is not shown.

Storage. Cap the cache and evict. An application that grows without limit gets deleted.

Memory. Large images are the usual cause of a termination. Downsample before display.

### Step 5, the paths that get skipped

Permission denied, and permission granted then revoked later in settings.

Notification permission refused, with the feature still usable.

Storage full.

No network at launch, meaning the very first run with nothing cached.

Token expired while backgrounded.

Operating system version older than the newest API used.

Accessibility: platform screen reader, larger text sizes, and reduced motion. Dynamic type breaks fixed
height layouts, which is the most common mobile accessibility defect.

### Step 6, submission

Check the current guidelines at the source: the
[App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) and
[Google Play policies](https://play.google.com/about/developer-content-policy/). The recurring rejection
causes are a missing or incorrect privacy declaration, payment for digital goods outside the platform
system, incomplete metadata, a login wall with no demo account, requesting permissions with no visible
purpose, and crashes on the reviewer's device.

Prepare the privacy declaration from what the application actually collects, including what third party
software development kits collect, which is frequently more than the developer knows.

Provide a working test account and steps for anything behind a login.

Include the account deletion path if accounts can be created, which is now required on both stores.

Test the release build, not the debug build. They differ in optimisation, logging and sometimes
behaviour.

The checklist of recurring rejection causes, mapped to the fix and the guideline area, is in
`references/store-review.md`.

## Self-audit

- Offline behaviour and conflict rule decided and written down.
- Queued work durable and idempotent.
- State restored after a process kill.
- No secret in the binary.
- Minimum version stated, and every API checked against it.
- Permissions requested in context, with the denial path working.
- Tested on a real device on a throttled connection.
- Dynamic type and screen reader checked.
- Current store guidelines read, not recalled.
- Release build tested, with a demo account prepared.

## When to stay off

A small change to a shipping app, a copy fix, a colour tweak, a single bug on one screen, does not need
the offline model relitigated or the store rules reread. If the user says "stop", "just execute", or
"skip the mobile checklist", that is the off switch: make the change they asked for and leave the rest.
It stays off for the rest of the session unless they ask for the full treatment again. A skill that
reopens settled architecture on every edit gets turned off.

## Honest limits

This skill decides the offline model, the interruption handling, the resource budget and the store
path. It does not design the screens or the interaction, which belong to `ui-design`, and it does not
own the accessibility depth past dynamic type and screen reader labels, which is `accessibility-audit`.
The server the app talks to, its API shape and its auth are `backend-build` and `auth-implement`, not
this skill.

The store guideline summaries here are pointers, not the current text. Both stores change their rules
between review cycles, so the rejection checklist in `references/store-review.md` says where to read
the live version rather than standing in for it. Cost of a push service or a backend at scale is a
`cost-control` question.
