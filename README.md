# New Zealand Accounting Assistant

New Zealand Accounting Assistant is a free, public, open-source AI bookkeeping skill for New Zealand small businesses. It helps owners, directors, bookkeepers, and accountants collect receipts, record income, import bank statements, match transactions, and prepare the monthly/annual numbers needed for Xero, IRD, or an accountant.

It is designed to be run with **Codex** or **Claude Code**. It can also be installed as an **OpenClaw** skill.

**Important disclaimer:** this service is not a replacement for a registered accountant, tax agent, or professional tax advice. It prepares records and draft outputs only. Please have a qualified New Zealand accountant review your records and filings before submitting anything to IRD or relying on the results.

This project is not for sale and should not be presented as a paid accounting product. It is intended to remain free and public, helping small businesses keep clearer records, reduce missing paperwork, and prepare better review packs for their accountant.

## Tax Law Baseline

This project follows New Zealand tax law and IRD guidance as checked on **25 May 2026**. Do not assume the rules are still current after this date.

Current baseline sources:

- [Goods and Services Tax Act 1985](https://www.legislation.govt.nz/act/public/1985/0141/latest/versions.aspx), NZ Legislation version **as at 13 November 2025**
- [Income Tax Act 2007](https://www.legislation.govt.nz/act/public/2007/0097/latest/versions.aspx), NZ Legislation version **as at 1 January 2026**
- [Tax Administration Act 1994](https://legislation.govt.nz/act/public/1994/0166/latest/versions.aspx), NZ Legislation version **as at 18 December 2025**
- [IRD GST guide IR375](https://www.ird.govt.nz/-/media/project/ir/home/documents/forms-and-guides/ir300---ir399/ir375/ir375.pdf), **March 2026**
- [IRD Individual income tax return guide IR3G](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/what-happens-at-the-end-of-the-tax-year/individual-income-tax-return---ir3/complete-my-individual-income-tax-return---ir3), **March 2026**, with IR3 return forms for **April 2026**
- IRD depreciation guidance: [IR260 Depreciation guide](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation), **2024**, and [IR265 General depreciation rates](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation), **March 2026**
- [IRD Provisional tax guide IR289](https://www.ird.govt.nz/income-tax/provisional-tax/provisional-tax-options/estimation-option), **April 2025**

Before publishing a new release, generating filing-ready reports, or advising users on GST/IRD/Xero outputs, re-check these official sources and update this section if any version or rule has changed.

## What It Does

For a business owner, the workflow is simple:

1. Send receipt photos, supplier invoices, income notes, or bank statement files.
2. New Zealand Accounting Assistant stores them under the correct client and legal/tax entity.
3. It reads the details: dates, amounts, suppliers, customers, descriptions, GST shown, and categories.
4. It matches receipts and income records against bank statement lines.
5. It shows what is matched, what is missing, and what needs review.
6. It creates useful monthly and annual outputs.

The goal is to reduce the usual end-of-month mess: missing receipts, unclear bank lines, uncoded transactions, and manual spreadsheet work.

It is designed for more than one company. A person can keep separate books for several companies they own, and an accountant or bookkeeper can keep separate local workspaces for multiple clients. Each company, sole trader, trust, partnership, or other entity gets its own ledger folder so records are not mixed.

## What It Can Produce

New Zealand Accounting Assistant can help generate:

- Monthly income and expense summaries
- Lists of unmatched or unclear bank transactions
- Receipt and invoice ledgers
- Xero bank statement CSV exports
- Xero precoded CSV exports with account code, tax type, and contact name
- GST return worksheets for GST-registered businesses
- Income tax / IR3 workpapers
- Asset and depreciation schedules
- Accountant review packs

If the business is **not registered for GST**, New Zealand Accounting Assistant records GST shown on receipts as evidence only. It does not claim GST, does not generate GST return figures, and uses `No GST` or the user's equivalent Xero tax rate for exports.

## Recommended Use

### Codex or Claude Code

Recommended for most users who are comfortable keeping business records on their own computer.

Typical monthly prompt:

```text
Set up bookkeeping for my business, then import this month's bank statement and receipts. Match everything, show what needs review, and prepare a Xero export.
```

Typical GST-registered prompt:

```text
Reconcile March and April, then prepare the GST return worksheet and Xero precoded CSV.
```

Typical non-GST-registered prompt:

```text
Reconcile March, keep GST as non-claimable evidence, and prepare the monthly profit summary plus Xero No GST export.
```

### OpenClaw

OpenClaw is still supported. The skill can run in an OpenClaw setup where users send receipts and commands through an assistant interface.

## How Accuracy Works

New Zealand Accounting Assistant is built around evidence, not guessing.

- Bank statements are treated as the source of truth for money movement.
- Receipt photos, invoices, and notes explain the bank lines.
- Original files are preserved in an `inbox/` folder.
- Normalized records are stored in monthly JSON ledger files.
- Ambiguous matches stay visible until a person confirms them.
- Xero account codes and tax rate names must come from the business, accountant, or Xero configuration. The skill should not invent them.
- GST handling depends on whether the business is GST registered.

## First Setup

On first use, New Zealand Accounting Assistant creates a local bookkeeping workspace. The default location is:

```text
~/KiwiBooks
```

Each legal/tax entity gets its own ledger folder:

```text
~/KiwiBooks/businesses/{entity-slug}/
```

The setup model has three layers:

- Operator: the person or firm using the skill, such as a business owner, director, accountant, or bookkeeper.
- Client or owner group: the customer, family group, holding group, or owner whose entities are being managed.
- Entity: the actual company, sole trader, trust, partnership, non-profit, or other legal/tax entity being reconciled and reported.

If there is more than one entity, the assistant must confirm the active entity before saving receipts, importing bank statements, reconciling, or generating reports.

During setup it asks for practical business details:

- Operator role: owner, director, accountant, bookkeeper, or administrator
- Client or owner group name
- Business name
- Legal/tax entity type
- Whether the business is GST registered
- GST number and GST filing settings, if registered
- Balance date
- Vehicle, phone, or home-office business-use percentages if relevant
- Xero mapping details if Xero precoded exports are needed

Example:

```text
You: setup
Assistant: I will use ~/KiwiBooks as the bookkeeping root unless you want another folder.
Assistant: Are you doing books for your own business, multiple businesses you control, or clients of an accounting/bookkeeping firm?
You: multiple businesses I control
Assistant: What owner group should I use?
You: Jay Zhang Owner Group
Assistant: What is your business name?
You: My Construction Ltd
Assistant: Is the business registered for GST?
You: no
Assistant: Vehicle business use percentage? (default 80)
You: 80
Assistant: Workspace ready at ~/KiwiBooks/businesses/my-construction-ltd.
           Client/owner group: Jay Zhang Owner Group
           Active entity: My Construction Ltd
           GST mode: not registered, so GST observed on receipts is stored as evidence but not claimed.
```

## Everyday Use

### Capture Receipts

```text
You: [photo of Bunnings receipt]
Assistant: Receipt captured:
           Bunnings Warehouse
           2026-03-19
           $174.00
           Category: materials
           GST observed: $22.70, not claimable because the business is not GST registered

           Reply to save, or correct any details.
```

### Record Income

```text
You: income 9775 Bathroom renovation - 42 Rimu St, ABC Homes
Assistant: Income recorded:
           Client: ABC Homes
           Amount: $9,775.00
           GST: not charged
           Invoice wording: Not GST registered. No GST has been charged.
```

### Reconcile a Month

```text
You: reconcile 2026-03
Assistant: Monthly Summary: March 2026
           Bank income: $29,670.00
           Bank expenses: $8,420.50
           Matched receipts: 23 / 25
           Matched income records: 8 / 8
           Unmatched bank lines: 3
           Needs review: 2
```

### Export to Xero

```text
You: xero export
Assistant: Xero CSV exported: 35 transactions.
```

For Xero precoded imports, fill `mappings/xero-account-map.json` first so the export can include the correct account codes and tax rates.

```csv
Date,Amount,Payee,Description,Reference,AccountCode,TaxType,ContactName
15/03/2026,-174.00,Bunnings Warehouse,BUNNINGS EFTPOS,CARD123,310,No GST,Bunnings Warehouse
17/03/2026,9775.00,ABC Homes Ltd,INV-2026-015,INV-2026-015,200,No GST,ABC Homes Ltd
```

### GST-Registered Businesses

If the business is GST registered, New Zealand Accounting Assistant can prepare GST return worksheets.

```text
You: report
Assistant: GST Report: Mar-Apr 2026
           Total purchases: $8,420.50
           Total sales: $29,670.00
           GST to pay: $2,771.67
           [Download XLSX]
```

The worksheet maps to IRD GST101A boxes such as sales/income, GST collected, purchases/expenses, GST credits, and GST to pay/refund. The normal direct-filing path is still to enter the figures in myIR unless a formal IRD Gateway integration is built.

### End of Tax Year

```text
You: ir3
Assistant: Annual Tax Summary: 2025-2026

           Income:             $82,608.70
           Less expenses:     -$49,500.00
           Less depreciation:  -$6,246.50
           Taxable income:     $26,862.20

           Reply "export ir3" for the full XLSX report.
```

## Features

- Receipt photo capture and extraction
- Income and invoice tracking
- Multiple clients and multiple legal/tax entities under one local workspace
- Bank statement import from CSV/XLSX/PDF-derived data
- Bank reconciliation against receipts and income
- Monthly financial summaries
- GST-aware and non-GST workflows
- IRD GST worksheet support for GST-registered businesses
- IR3 / annual income tax workpapers
- Provisional tax calculations
- Asset and depreciation tracking
- Xero standard CSV export
- Xero precoded CSV export
- Local record keeping with no telemetry from this skill

## Installation

### Recommended: Codex or Claude Code

Clone or copy this repository into a local working folder and ask Codex or Claude Code to use the skill instructions in `SKILL.md`.

```bash
git clone https://github.com/maxazure/new-zealand-accounting-assistant.git
cd new-zealand-accounting-assistant
```

For XLSX report generation, install `openpyxl`:

```bash
pip install openpyxl
```

CSV and Xero precoded CSV exports can run without `openpyxl`.

### OpenClaw

After it is published under the new public name, install through ClawHub with:

```bash
npm i -g clawhub
clawhub install new-zealand-accounting-assistant
```

During the rename transition, the older published slug may still be available:

```bash
clawhub install kiwi-receipts
```

Or install manually:

```bash
git clone https://github.com/maxazure/new-zealand-accounting-assistant.git ~/.openclaw/skills/new-zealand-accounting-assistant
```

You can also copy the repository into a workspace skill directory:

```bash
cp -r new-zealand-accounting-assistant ~/.openclaw/workspace/skills/new-zealand-accounting-assistant
```

## Commands

### Setup

| Command | Description |
|---------|-------------|
| `setup` | Configure the business workspace |
| `clients` | List clients or owner groups |
| `entities` | List legal/tax entities |
| `use my-company-ltd` | Set the active entity before capture/import/report |
| `help` | Show available commands |

### Receipts

| Command | Description |
|---------|-------------|
| Send photo | Capture a receipt |
| `summary` | Current period overview with bank match status |
| `list` | Show recent receipts |
| `delete last` | Remove last receipt |

### Bank Statements

| Command | Description |
|---------|-------------|
| `import bank statement` | Import and normalize a bank CSV/XLSX/PDF |
| `reconcile` | Match current-period bank lines to receipts and income |
| `reconcile 2026-03` | Reconcile one month |
| `month 2026-03` | Monthly bank/source summary |

### Income

| Command | Description |
|---------|-------------|
| `income 9775 description` | Record sales income |
| `income list` | Show recent income entries |
| `income summary` | Current-period income total |

### Tax and Reports

| Command | Description |
|---------|-------------|
| `report` | Generate a period report XLSX |
| `report 2026-03` | Generate report for a specific period |
| `ir3` or `tax return` | Annual income tax summary |
| `export ir3` | Annual XLSX report |
| `provisional` | Calculate provisional tax instalments |
| `set last year tax 8409` | Set previous year residual income tax |

### Assets

| Command | Description |
|---------|-------------|
| `asset add name $cost` | Register a depreciable asset |
| `asset list` | Show assets with current book values |
| `asset dispose name $price` | Record asset disposal |
| `depreciation` | Calculate this year's depreciation |

### Export

| Command | Description |
|---------|-------------|
| `xero export` | Generate standard Xero bank statement CSV |
| `xero precoded export` | Generate Xero precoded CSV with AccountCode, TaxType, ContactName |

## Local Data Storage

All accounting data is stored locally by default:

```text
~/.openclaw/data/kiwi-receipts/
└── config.json                         # Pointer to KiwiBooks root and active client/entity

~/KiwiBooks/
├── registry/
│   ├── operators.json                # People/firms using the skill
│   ├── clients.json                  # Clients or owner groups
│   ├── entities.json                 # Legal/tax entities and ledger paths
│   └── assignments.json              # Operator-client-entity relationships
├── clients/
│   └── {client-or-owner-slug}/
│       ├── client.json
│       └── entity-links.json
├── shared/
│   ├── chart-of-accounts/
│   └── templates/
└── businesses/
    └── {entity-slug}/
        ├── config.json                 # Business name, GST status, tax settings
        ├── inbox/                      # Original receipts, income files, bank statements, notes
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
        ├── working/reconciliations/
        ├── outputs/
        └── archive/
```

Some compatibility paths still use the older `kiwi-receipts` or `KiwiBooks` names so existing users do not lose or duplicate local records during the rename.

New Zealand Accounting Assistant uses JSON, but not one large file. Monthly records are split into `ledger/periods/YYYY-MM/`; annual tax records are split into `ledger/tax-years/YYYY-YYYY/`; long-lived reference data goes into `ledger/registers/`.

The root-level `registry/` and `clients/` folders group many entities for one operator, such as an owner with several companies or an accountant with several clients. The actual ledgers still live under separate `businesses/{entity-slug}/` folders.

See [`ledger-file-format.md`](references/ledger-file-format.md) for field definitions, including `gst_registered`, `gst_claimable`, `claim_status`, and non-GST handling.

## Technical Notes

### Report Script

Generate a report from an entity folder:

```bash
python3 scripts/generate_report.py \
  --business-dir ~/KiwiBooks/businesses/my-construction-ltd \
  --period 2026-03 \
  --output ~/KiwiBooks/businesses/my-construction-ltd/outputs/monthly/march-report.xlsx
```

Generate a Xero CSV:

```bash
python3 scripts/generate_report.py \
  --business-dir ~/KiwiBooks/businesses/my-construction-ltd \
  --period 2026-03 \
  --output ~/KiwiBooks/businesses/my-construction-ltd/outputs/xero/standard/xero.csv \
  --format xero-csv
```

Generate a Xero precoded CSV:

```bash
python3 scripts/generate_report.py \
  --business-dir ~/KiwiBooks/businesses/my-construction-ltd \
  --period 2026-03 \
  --xero-map ~/KiwiBooks/businesses/my-construction-ltd/mappings/xero-account-map.json \
  --output ~/KiwiBooks/businesses/my-construction-ltd/outputs/xero/precoded/xero-precoded.csv \
  --format xero-precoded-csv
```

### File Structure

```text
new-zealand-accounting-assistant/
├── SKILL.md                          # Agent skill instructions
├── README.md                         # This file
├── scripts/
│   ├── init_workspace.py             # Local KiwiBooks workspace initializer
│   └── generate_report.py            # XLSX/CSV report generator
└── references/
    ├── ledger-file-format.md          # Sharded ledger schema
    ├── nz-gst-guide.md               # GST compliance reference
    ├── nz-income-tax-guide.md         # Income tax reference
    ├── nz-depreciation-rates.md       # Depreciation rates reference
    └── xero-import-and-ird-filing.md  # Xero/IRD filing research reference
```

## Compliance and Limits

This project is built with reference to:

- Goods and Services Tax Act 1985 (NZ)
- Income Tax Act 2007 (NZ)
- Tax Administration Act 1994
- IRD GST101A form and GST guidance
- IRD depreciation guidance
- Xero bank import and precoded CSV guidance

Important limits:

- This tool assists with record keeping and report preparation. It is not professional tax advice.
- For GST filing, ordinary users still enter figures in myIR unless a formal IRD Gateway integration is built.
- Xero account codes and tax rates must come from the user's Xero organisation or accountant.
- Businesses should keep records for at least 7 tax years and verify filing outputs before submission.

See the `references/` directory for detailed technical and compliance notes.

## Privacy

- Accounting data is stored locally under `~/KiwiBooks/` by default.
- Original source files are preserved under each business `inbox/`.
- The skill itself does not add telemetry or send bookkeeping data to a separate service.
- Any AI vision or model processing depends on the tool/runtime you choose, such as Codex, Claude Code, or OpenClaw.

## License

MIT
