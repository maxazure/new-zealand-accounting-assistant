# Month-End Workpapers

Use this reference when preparing month-end close support, accountant review packs, draft journal entries, variance notes, or reconciliation exception reporting.

## What We Borrow From Finance Workflows

The useful pattern is not US-specific GAAP or SOX content. The useful pattern is disciplined financial workflow:

- close checklist before reports are treated as ready
- reconciling items categorized, aged, owned, and followed up
- draft journal entries balanced and supported before review
- material variances explained with numbers and evidence
- workpapers packaged so a reviewer can trace every output back to source files

Apply these patterns conservatively for New Zealand small-business bookkeeping.

## Month-End Close Checklist

For each active entity and period, maintain `ledger/periods/YYYY-MM/review-checklist.json`.

Minimum tasks:

1. Confirm the active client/entity.
2. Index all source files received for the period.
3. Import bank statement lines and remove duplicates.
4. Match bank lines to receipts and income records.
5. List unresolved `reconciling-items.json`.
6. Prepare draft `journal-entries.json` only where an adjustment is needed.
7. Recalculate monthly summary and GST/non-GST treatment.
8. Compare current month to prior month and prior year month when data exists.
9. Generate accountant review pack.
10. Mark professional review as required before filing or reliance.

Recommended statuses: `not_started`, `in_progress`, `blocked`, `complete`, `review_required`, `reviewed`.

## Reconciling Item Categories

Use `ledger/periods/YYYY-MM/reconciling-items.json`.

Allowed categories:

- `timing_difference`: normal timing issue expected to clear, such as a deposit appearing after period end.
- `adjustment_required`: likely needs a correction, private-use adjustment, missing bank fee, duplicate, or coding change.
- `needs_investigation`: no reliable explanation yet; ask the owner, bookkeeper, or accountant.

Age buckets:

- `0-30`: current
- `31-60`: aging, ask for follow-up
- `61-90`: overdue, escalate to owner/accountant
- `90+`: stale, do not hide in summaries

Do not clear an item only because it is old. Keep it visible until evidence, adjustment, or explicit reviewer decision resolves it.

## Draft Journal Entries

Use `ledger/periods/YYYY-MM/journal-entries.json` for draft entries. These are review artifacts, not proof that anything has been posted in Xero, a general ledger, or IRD.

Required fields:

- entry type and period
- clear description
- source record or bank transaction IDs
- debit and credit lines
- Xero account code and tax type when relevant
- calculation basis
- preparer and created date
- status and reviewer requirement

Quality gates:

- Debits must equal credits.
- Account codes must come from an explicit mapping file or user/accountant confirmation.
- GST treatment must follow the entity's GST registration status.
- Accruals or estimates must show the basis and whether reversal is expected.
- Do not create a journal entry when a simple Xero bank coding row is enough.

## Variance Analysis

Use variance analysis to make review packs more useful, not to create false precision.

Default investigation triggers when no entity-specific threshold exists:

- income or expense category changed by more than NZD 500 and 20% versus prior month
- any new category over NZD 500
- any single unmatched or uncoded bank line over NZD 200
- any GST-impacting issue for a GST-registered entity
- any repeated unresolved item across two or more periods

Variance notes should state:

- amount and percentage movement
- whether it is favorable/unfavorable or simply higher/lower
- likely driver based on evidence
- whether follow-up is needed
- whether the issue affects GST, income tax, Xero import, or accountant review

Avoid vague explanations such as "higher than expected" unless the specific driver is unknown and the item is explicitly marked for follow-up.

## Accountant Review Pack

Store review outputs under `outputs/accountant/review-packs/`.

Minimum pack contents:

- period summary
- source file index
- receipt and income ledgers
- imported bank transaction list
- match summary
- unresolved reconciling item list with age/status/owner
- draft journal entries or adjustment list
- material variance notes
- Xero export preview if relevant
- GST/IRD workpapers if relevant
- disclaimer and review-required statement

The pack should make it easy for a reviewer to answer: What changed, what is unresolved, what evidence supports the numbers, and what still needs a human decision?
