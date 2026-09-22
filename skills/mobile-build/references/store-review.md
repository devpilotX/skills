# Store review checklist

A rejection costs a review cycle, sometimes several days. The causes below account for most rejections
on both stores, and every one is preventable before you submit. Read the live guidelines at the source
before each submission, because the rules move between cycles. The App Review Guidelines and the Google
Play developer content policy are the authoritative text; this file only lists what to check.

## The recurring rejection causes

| Cause | What triggers it | The fix before submitting |
| --- | --- | --- |
| Wrong privacy declaration | Declared data collection does not match what the app and its SDKs actually send | Audit every network call and every third party SDK, then declare what leaves the device |
| Payment outside the store | Selling digital goods or subscriptions through an external payment flow | Use the platform in app purchase for digital goods; external pay is allowed only for physical goods and services |
| Login wall, no demo | The reviewer cannot get past sign in | Provide a working demo account and the exact steps in the review notes |
| Permission with no purpose | Requesting location, contacts or camera with no visible feature that uses it | Remove the permission or add the feature; explain the reason in the usage string |
| Incomplete metadata | Missing screenshots, wrong age rating, placeholder description | Fill every required listing field with real content |
| Crash on the reviewer device | Release build crashes on an OS version or device you did not test | Test the release build on the minimum supported OS and an older device |
| No account deletion | Accounts can be created but not deleted from inside the app | Add an in app account deletion path; both stores now require it |
| Broken links | Support URL or privacy policy URL returns an error | Check every URL in the listing resolves |
| Misleading listing | Screenshots or description promise features the app does not have | Match the listing to what the build does |

## Privacy declaration

Build the declaration from what the app actually collects, not from memory. Third party SDKs for
analytics, crash reporting, advertising and attribution frequently collect more than the developer
realises, and their collection is your declaration to make.

Steps to get it right:

List every SDK linked into the release build.

For each, read its documented data collection and its own privacy manifest where the platform requires
one.

Add the app's own collection: what the user types, what the device sends, what the backend logs.

Map each collected item to the store's category and to whether it is linked to the user and used for
tracking.

Declare that map. An under declaration found later is a removal, not a rejection.

## Before you press submit

Test the release build, not debug. They differ in optimisation, logging and sometimes behaviour, and the
reviewer sees release.

Run on the minimum supported OS version, not only the newest. A feature guarded by an availability check
that is missing will crash the reviewer's older device.

Walk the first run with nothing cached and no network, because reviewers often test on constrained
connections.

Confirm the demo account works from a fresh install and reaches the features under review.

Confirm every permission prompt names a real reason in its usage string, and that denying it leaves the
app usable.

Confirm the account deletion path exists and completes.

Confirm the privacy policy URL and support URL both resolve.

## After a rejection

Read the exact guideline number the reviewer cites. The rejection names a rule; the fix follows from the
rule, not from guesswork.

Reply in the resolution centre with what you changed, referencing the guideline. A clear reply shortens
the next cycle.

Do not resubmit the same build hoping for a different reviewer. The rule that failed will fail again.

Keep a record of which build was rejected for which reason, so a later regression does not repeat a fix
you already made.
