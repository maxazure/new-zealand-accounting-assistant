# Ledger File Format

Use this reference whenever implementing storage, imports, reconciliation, reports, or migrations.

## Design Principles

- Do not store all bookkeeping records in one large JSON file.
- Store monthly facts in monthly period folders.
- Store annual tax/register data in tax-year folders.
- Store reusable reference data globally for the business.
- Treat generated summaries as rebuildable outputs, not the source of truth.
- Preserve original source files separately from normalized ledger records.

## Business Directory Layout

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
│   │       ├── adjustments.json
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
└── outputs/
```

## Config Fields

`config.json` records business-level tax status and defaults:

```json
{
  "business_name": "My Construction Ltd",
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
  "needs_review": 2
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
- If a month is locked, do not edit its files directly. Write corrections into a later period's `adjustments.json` unless the user explicitly unlocks the period.

