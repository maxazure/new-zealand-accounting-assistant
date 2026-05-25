# Xero Chart of Accounts

Use this reference when creating or validating `mappings/xero-account-map.json`, preparing Xero precoded CSV exports, proposing account codes, or helping a user set up Xero.

Research baseline: checked 25 May 2026 against Xero Central and Xero Developer documentation.

## What the Chart of Accounts Does

Xero's chart of accounts is the list of accounts used to classify transactions for reporting, GST treatment, and bank reconciliation. Each Xero organisation has a default chart of accounts, but users and accountants commonly customise it.

Do not assume account codes are the same across Xero organisations. Before producing Xero precoded CSVs, ask the user to provide one of:

- an exported Xero chart of accounts CSV
- a completed `mappings/xero-account-map.json`
- explicit account-code and tax-rate instructions from their accountant/bookkeeper

## Xero Import CSV Format

Xero's chart import CSV uses these common columns:

| Column | Required | Notes |
|--------|----------|-------|
| `Code` | Yes | Unique account code, up to 10 characters. Treat as text to preserve leading zeros. |
| `Name` | Yes | Unique account name, up to 150 characters. |
| `Type` | Yes | Must match a Xero account type exactly as Xero expects it. |
| `Tax Code` | Yes | Must match a tax rate in that Xero organisation. |
| `Reporting Name` | No | Practice/advisor reporting name where available. |
| `Description` | No | Useful for explaining which account users should choose. Leave blank for bank accounts. |
| `Dashboard` | No | `Yes` or `No`. Bank accounts must be `No` or blank. |
| `Expense Claims` | No | `Yes` or `No`. Bank accounts must be `No` or blank. |
| `Enable Payments` | No | `Yes` or `No`. Bank accounts must be `No` or blank. |
| `Balance` | No | Conversion balance immediately before the conversion date. Leave blank unless intentionally importing balances. |

Important import rules:

- Importing a chart can update, create, or archive accounts. Do not generate an import file casually.
- If an account should remain in Xero, keep it in the import file.
- Do not change both account code and account name at the same time unless the user understands Xero may create/archive accounts.
- Xero supports up to 1000 rows including the header, but large charts can make the organisation slower to use.
- Tax rates in the file must already exist in the Xero organisation. If they do not, Xero may fall back to a zero/no-tax treatment.
- Xero uses tracking categories instead of sub-accounts, so do not encode jobs, clients, or projects as excessive COA accounts.

## Common Xero Account Types

The exact type spelling for an import should come from the user's exported Xero template. Common Xero account types include:

| Category | Account types |
|----------|---------------|
| Assets | `Bank`, `Current Asset`, `Fixed Asset`, `Inventory`, `Non-current Asset`, `Prepayment` |
| Liabilities | `Current Liability`, `Liability`, `Non-current Liability` |
| Equity | `Equity` |
| Revenue | `Sales`, `Revenue`, `Other Income` |
| Expenses | `Direct Costs`, `Expense`, `Overhead`, `Depreciation` |

API integrations may expose type codes such as `BANK`, `CURRENT`, `CURRLIAB`, `FIXED`, `DIRECTCOSTS`, `EXPENSE`, `OVERHEADS`, `REVENUE`, and `SALES`. Store both display labels and API codes when a connector supplies them.

## New Zealand GST Defaults

For New Zealand organisations:

- Xero's default GST system account is normally `820 - GST`. Do not create a separate GST account for GST return reporting.
- If the organisation is not registered for GST and GST basis is none, Xero defaults transactions and chart accounts to no-GST treatment.
- For GST-registered entities, common tax-rate display names include `15% GST on Income`, `15% GST on Expenses`, `No GST`, and import-specific rates such as `GST on Imports`.
- For non-GST-registered entities, map income and expense accounts to `No GST` unless the user's exported Xero organisation uses a different exact tax-rate label.
- Bank accounts generally use the no-tax/no-GST tax code required by the organisation's Xero template.

Always use the exact tax-rate display name from the user's Xero organisation in `mappings/xero-account-map.json` and Xero precoded exports.

## NZ Small-Business Baseline

There is no single legally required New Zealand chart of accounts. Accountants often adapt Xero's default chart for the entity type and industry. For this skill, keep the default baseline compact and add detail only when it improves review, GST treatment, or management reporting.

Suggested high-level structure:

| Area | Typical use | Xero type |
|------|-------------|-----------|
| Bank and clearing | Business bank accounts, payment clearing accounts | `Bank` or `Current Asset` |
| Current assets | Accounts receivable, prepayments, deposits, inventory | `Current Asset`, `Prepayment`, `Inventory` |
| Fixed assets | Vehicles, tools, plant, computer equipment, accumulated depreciation | `Fixed Asset` |
| Current liabilities | Accounts payable, GST, PAYE, wages payable, income tax payable, short-term loans | `Current Liability` |
| Non-current liabilities | Long-term loans and hire purchase | `Non-current Liability` |
| Equity | Owner contributions, drawings, share capital, retained earnings | `Equity` |
| Income | Sales, service income, other trading income | `Sales` or `Revenue` |
| Direct costs | Materials, subcontractors, job costs, cost of goods sold | `Direct Costs` |
| Operating expenses | Vehicle, fuel, rent, insurance, advertising, phone, software, office, legal/accounting, bank fees | `Expense` or `Overhead` |
| Tax and depreciation | Depreciation expense, income tax expense, rounding, realised currency gains/losses | `Depreciation`, `Expense`, or relevant system account |

Suggested bookkeeping categories for a small NZ service/trade business:

| Skill category | Typical Xero account | Xero type | GST-registered tax rate | Non-GST tax rate |
|----------------|----------------------|-----------|--------------------------|------------------|
| `sales` | Sales / Service Income | `Sales` or `Revenue` | `15% GST on Income` | `No GST` |
| `materials` | Materials / Job Materials | `Direct Costs` | `15% GST on Expenses` | `No GST` |
| `subcontractor` | Subcontractors | `Direct Costs` | `15% GST on Expenses` | `No GST` |
| `tools_small` | Small Tools and Equipment | `Expense` | `15% GST on Expenses` | `No GST` |
| `fuel` | Fuel / Motor Vehicle Expenses | `Expense` | `15% GST on Expenses` or apportioned | `No GST` |
| `vehicle` | Motor Vehicle Expenses | `Expense` | `15% GST on Expenses` or apportioned | `No GST` |
| `phone` | Telephone and Internet | `Expense` | `15% GST on Expenses` or apportioned | `No GST` |
| `software` | Software / Subscriptions | `Expense` | depends on supplier and GST evidence | `No GST` |
| `office` | Office Expenses / Printing and Stationery | `Expense` | `15% GST on Expenses` | `No GST` |
| `professional_fees` | Accounting / Legal / Professional Fees | `Expense` | `15% GST on Expenses` | `No GST` |
| `bank_fees` | Bank Fees | `Expense` | usually `No GST` | `No GST` |
| `asset_purchase` | Fixed Asset account by asset class | `Fixed Asset` | `15% GST on Expenses` if claimable | `No GST` |
| `private_use` | Drawings / Shareholder Current Account | `Equity` or `Current Liability` | `No GST` | `No GST` |

These are starting points only. The user's accountant or exported Xero chart overrides this baseline.

## Skill Rules

- Never invent account codes for Xero exports.
- Keep account mappings per entity, not globally across all clients.
- Store user-confirmed mappings in `mappings/xero-account-map.json`.
- Validate that every Xero precoded row has `AccountCode` and `TaxType`.
- Validate that expense categories use expense/direct-cost/fixed-asset type accounts, and income categories use sales/revenue type accounts.
- Keep the chart compact. Prefer Xero tracking categories for jobs, projects, locations, or business units.

## Sources

- Xero Central: Import a chart of accounts
- Xero Central: Components of an account in your chart of accounts
- Xero Central: How GST works in Xero NZ
- Xero Developer: Integration best practices
- Xero Developer: Creating invoices and account mapping
- Xero Developer: Tax and the Xero API
