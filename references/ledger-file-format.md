# Ledger File Format

Use this reference whenever implementing storage, imports, reconciliation, reports, or migrations.

## Design Principles

- Do not store all bookkeeping records in one large JSON file.
- Store monthly facts in monthly period folders.
- Store annual tax/register data in tax-year folders.
- Store reusable reference data globally for the entity.
- Treat generated summaries as rebuildable outputs, not the source of truth.
- Preserve original source files separately from normalized ledger records.
- Keep each legal/tax entity in a separate ledger folder. Use workspace registry files to group multiple entities for one owner, client, accountant, or bookkeeper.

## Workspace Registry Layout

The bookkeeping root can contain many clients and many entities:

```text
{books_root}/
├── registry/
│   ├── operators.json
│   ├── clients.json
│   ├── entities.json
│   └── assignments.json
├── clients/
│   └── {client-or-owner-slug}/
│       ├── client.json
│       └── entity-links.json
└── businesses/
    └── {entity-slug}/
        └── ...
```

Definitions:

- `operator`: the person or firm using the skill, such as an owner, director, accountant, or bookkeeper.
- `client`: the customer or owner group. For an owner with several companies, this can be the person or holding group. For an accounting firm, this is the client.
- `entity`: the legal/tax entity with its own ledger, such as a company, sole trader, partnership, trust, non-profit, or other entity.

Registry files are JSON objects keyed by slug. They are routing and discovery metadata only. Accounting facts live under the entity's own `businesses/{entity-slug}/` folder.

## Entity Directory Layout

```text
{business_dir}/
├── config.json
├── inbox/
│   ├── receipts/YYYY-MM/
│   ├── income/YYYY-MM/
│   ├── bank-statements/YYYY-MM/
│   └── notes/YYYY-MM/
├── ledger/
│   ├── periods/
│   │   └── YYYY-MM/
│   │       ├── receipts.json
│   │       ├── income.json
│   │       ├── bank-transactions.json
│   │       ├── matches.json
│   │       ├── reconciling-items.json
│   │       ├── adjustments.json
│   │       ├── journal-entries.json
│   │       ├── review-checklist.json
│   │       └── period-summary.json
│   ├── tax-years/
│   │   └── YYYY-YYYY/
│   │       ├── assets.json
│   │       ├── depreciation.json
│   │       ├── income-tax.json
│   │       ├── provisional-tax.json
│   │       └── annual-summary.json
│   ├── registers/
│   │   ├── contacts.json
│   │   ├── assets-master.json
│   │   └── bank-accounts.json
│   └── indexes/
│       └── document-index.json
├── mappings/
│   ├── categories.json
│   └── xero-account-map.json
├── working/
│   ├── reconciliations/
│   ├── month-end-close/
│   ├── workpapers/
│   └── journal-entries/
└── outputs/
    └── accountant/review-packs/
```

## Mapping Files

### mappings/xero-account-map.json

Per-entity Xero mapping file. Account codes and tax-rate names must come from that entity's exported Xero chart of accounts, an accounting-system connector, or explicit accountant/user confirmation.

```json
{
  "chart_of_accounts": {
    "source": "not_configured",
    "requires_entity_xero_export_or_accountant_confirmation": true
  },
  "defaults": {
    "expense_tax_type": "No GST",
    "income_tax_type": "No GST",
    "no_gst_tax_type": "No GST"
  },
  "income": {},
  "categories": {}
}
```

See `references/xero-chart-of-accounts.md` before changing this schema or proposing default category mappings.

## Config Fields

`config.json` records entity-level tax status and defaults:

```json
{
  "schema_version": 2,
  "business_slug": "my-construction-ltd",
  "business_name": "My Construction Ltd",
  "client_slug": "jay-owner-group",
  "operator_slug": "jay-zhang",
  "operator_role": "owner",
  "entity": {
    "entity_slug": "my-construction-ltd",
    "legal_name": "My Construction Ltd",
    "trading_name": "My Construction Ltd",
    "entity_type": "company",
    "entity_role": "owned_entity",
    "client_slug": "jay-owner-group",
    "operator_slug": "jay-zhang",
    "nzbn": "",
    "ird_number": ""
  },
  "balance_date": "31-march",
  "tax_year_start_month": 4,
  "tax_year_start_day": 1,
  "gst_registered": false,
  "gst_number": "",
  "gst_registered_from": null,
  "gst_deregistered_from": null,
  "gst_filing_frequency": null,
  "gst_accounting_basis": null,
  "gst_registration_monitoring": {
    "enabled": true,
    "threshold_nzd": 60000,
    "lookback_months": 12,
    "forecast_months": 12
  },
  "depreciation_method": "DV",
  "vehicle_business_percent": 80,
  "phone_business_percent": 70,
  "home_office_percent": 0
}
```

GST rules:
- If `gst_registered` is `false`, do not produce GST return outputs, do not claim input GST, and use `No GST` or the user's equivalent Xero tax rate for exports.
- If `gst_registered` is `true`, GST reports and claimability checks are enabled from `gst_registered_from`.
- Keep observed receipt GST even when not registered, but mark it as not claimable.

## Monthly Period Files

Monthly period folder: `ledger/periods/YYYY-MM/`.

### receipts.json

Array of normalized supplier receipts and purchase evidence:

```json
[
  {
    "id": "rec_20260315_001",
    "date": "2026-03-15",
    "period": "2026-03",
    "source_file": "inbox/receipts/2026-03/bunnings-20260315.jpg",
    "merchant": "Bunnings Warehouse",
    "supplier_gst_number": "123-456-789",
    "items": [
      {
        "description": "Timber 2x4 3.6m",
        "quantity": 10,
        "unit_price": 12.5,
        "amount_incl_gst": 125.0
      }
    ],
    "amounts": {
      "total_incl_gst": 174.0,
      "gst_observed": 22.7,
      "gst_calculated": 22.7,
      "gst_claimable": 0.0,
      "total_excl_gst_for_tax": 174.0
    },
    "gst_treatment": {
      "business_gst_registered": false,
      "supplier_gst_registered": true,
      "claim_status": "not_claimable_not_registered",
      "tax_rate": "No GST",
      "reason": "Business is not GST registered"
    },
    "category": "materials",
    "business_use_percent": 100,
    "asset_candidate": false,
    "evidence_status": "complete",
    "reconciliation_status": "unmatched",
    "bank_transaction_ids": [],
    "created_at": "2026-03-15T10:30:00Z",
    "updated_at": "2026-03-15T10:30:00Z"
  }
]
```

### income.json

Array of invoices, sales, and other income records:

```json
[
  {
    "id": "inc_20260317_001",
    "date": "2026-03-17",
    "period": "2026-03",
    "source_file": "inbox/income/2026-03/inv-2026-015.pdf",
    "client": "ABC Homes Ltd",
    "description": "Bathroom renovation - 42 Rimu St",
    "invoice_number": "INV-2026-015",
    "amounts": {
      "amount_charged": 9775.0,
      "gst_charged": 0.0,
      "income_excl_gst_for_tax": 9775.0
    },
    "gst_treatment": {
      "business_gst_registered": false,
      "gst_charged_to_customer": false,
      "tax_rate": "No GST",
      "invoice_wording": "Not GST registered. No GST has been charged."
    },
    "status": "paid",
    "reconciliation_status": "unmatched",
    "bank_transaction_ids": [],
    "created_at": "2026-03-17T14:30:00Z",
    "updated_at": "2026-03-17T14:30:00Z"
  }
]
```

### bank-transactions.json

Array of bank statement lines. This is the cash-movement source of truth.

```json
[
  {
    "id": "bank_20260315_001",
    "date": "2026-03-15",
    "period": "2026-03",
    "amount": -174.0,
    "payee": "Bunnings Warehouse",
    "description": "BUNNINGS 1234 EFTPOS",
    "reference": "CARD 1234",
    "source_account": "Business Cheque",
    "source_file": "inbox/bank-statements/2026-03/anz-2026-03.csv",
    "status": "matched",
    "matched_record_ids": ["rec_20260315_001"],
    "category": "materials",
    "xero": {
      "account_code": "310",
      "tax_type": "No GST",
      "contact_name": "Bunnings Warehouse"
    },
    "confidence": 0.96,
    "created_at": "2026-03-31T10:30:00Z",
    "updated_at": "2026-03-31T10:35:00Z"
  }
]
```

### matches.json

Array of accepted or suggested reconciliation links:

```json
[
  {
    "id": "match_20260315_001",
    "bank_transaction_id": "bank_20260315_001",
    "record_type": "receipt",
    "record_id": "rec_20260315_001",
    "match_type": "auto",
    "confidence": 0.96,
    "reasons": ["amount exact", "date within 1 day", "merchant match"],
    "review_status": "accepted",
    "created_at": "2026-03-31T10:35:00Z"
  }
]
```

### reconciling-items.json

Array of unresolved differences identified during reconciliation:

```json
[
  {
    "id": "recitem_20260331_001",
    "period": "2026-03",
    "date_originated": "2026-03-29",
    "item_type": "needs_investigation",
    "source": "bank",
    "bank_transaction_id": "bank_20260329_004",
    "description": "Unknown card purchase",
    "amount": -86.4,
    "age_days": 2,
    "status": "open",
    "owner": "client",
    "expected_resolution": "Ask owner for receipt or private-use confirmation",
    "created_at": "2026-03-31T18:00:00Z",
    "updated_at": "2026-03-31T18:00:00Z"
  }
]
```

Allowed `item_type` values:
- `timing_difference`: expected to clear without a tax/accounting adjustment
- `adjustment_required`: likely needs an adjustment or draft journal entry
- `needs_investigation`: cannot be explained yet

### adjustments.json

Manual accounting/tax adjustments for the month:

```json
[
  {
    "id": "adj_20260331_001",
    "date": "2026-03-31",
    "type": "private_use",
    "description": "Vehicle private-use adjustment",
    "amount": -42.5,
    "gst_effect": 0.0,
    "reason": "Monthly vehicle logbook estimate",
    "created_at": "2026-03-31T18:00:00Z"
  }
]
```

### journal-entries.json

Draft double-entry adjustments for accountant or owner review. Do not mark as posted unless the user confirms posting outside this skill or a verified accounting-system connector confirms it.

```json
[
  {
    "id": "je_20260331_001",
    "period": "2026-03",
    "entry_type": "bank_fee_adjustment",
    "description": "Record unclassified bank fee",
    "source_references": ["bank_20260329_004"],
    "lines": [
      {
        "account_code": "404",
        "account_name": "Bank Fees",
        "debit": 12.5,
        "credit": 0.0,
        "tax_type": "No GST",
        "memo": "Monthly bank fee"
      },
      {
        "account_code": "090",
        "account_name": "Business Bank Account",
        "debit": 0.0,
        "credit": 12.5,
        "tax_type": "No GST",
        "memo": "Monthly bank fee"
      }
    ],
    "balanced": true,
    "status": "draft_review_required",
    "prepared_by": "operator",
    "review_required": true,
    "created_at": "2026-03-31T18:10:00Z"
  }
]
```

### review-checklist.json

Month-end close and review status for the period:

```json
{
  "period": "2026-03",
  "status": "in_progress",
  "prepared_by": "operator",
  "reviewer": null,
  "tasks": [
    {
      "id": "source_files_indexed",
      "label": "Source files indexed",
      "status": "complete",
      "completed_at": "2026-03-31T18:00:00Z"
    },
    {
      "id": "unresolved_items_reviewed",
      "label": "Unresolved reconciling items reviewed",
      "status": "open"
    }
  ],
  "signoff": {
    "prepared_at": null,
    "reviewed_at": null,
    "disclaimer_acknowledged": false
  }
}
```

### period-summary.json

Derived summary. It can be regenerated and should not be the only source of truth.

```json
{
  "period": "2026-03",
  "locked": false,
  "generated_at": "2026-03-31T18:05:00Z",
  "bank_income": 29670.0,
  "bank_expenses": -8420.5,
  "source_income": 29670.0,
  "source_expenses": 8420.5,
  "gst_registered": false,
  "gst_output_tax": 0.0,
  "gst_input_tax_claimable": 0.0,
  "unmatched_bank_lines": 3,
  "needs_review": 2,
  "draft_journal_entries": 1,
  "material_variances": 2,
  "review_status": "in_progress"
}
```

## Annual Files

Tax-year folder: `ledger/tax-years/YYYY-YYYY/`, for example `ledger/tax-years/2025-2026/`.

Use annual files for:
- depreciation schedules
- annual income tax summaries
- provisional tax tracking
- annual summaries

Keep `ledger/registers/assets-master.json` as the long-lived asset register, and write calculated yearly depreciation into `ledger/tax-years/YYYY-YYYY/depreciation.json`.

## Index and Migration Rules

- `ledger/indexes/document-index.json` maps every source file to the normalized records created from it.
- Legacy flat files such as `ledger/receipts.json` may be copied into period folders during migration, but do not continue appending to them.
- New write operations must target period or tax-year files.
- Reports can read a date range by loading only the required monthly folders.
- If a month is locked, do not edit its files directly. Write corrections into a later period's `adjustments.json` or `journal-entries.json` unless the user explicitly unlocks the period.
