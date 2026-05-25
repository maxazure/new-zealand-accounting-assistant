# Xero Import and IRD Filing Reference

Research date: 2026-05-25.

Use this reference when implementing or reviewing Xero exports, IRD GST filing outputs, direct IRD filing concepts, or bookkeeping evidence requirements.

## Xero Bank Statement Imports

### Standard manual bank statement import

Xero lets users manually import bank statement lines when a bank feed is unavailable or incomplete. Supported statement file formats include CSV, OFX, QFX, QIF, and QuickBooks formats. Xero recommends OFX when the bank can export it cleanly. PDF bank statements are not imported directly into Xero; they need to be converted into an importable transaction file first.

For CSV, the skill should generate a clean single-amount bank statement file:

```csv
Date,Amount,Payee,Description,Reference
15/03/2026,-174.00,Bunnings Warehouse,BUNNINGS EFTPOS,CARD123
17/03/2026,9775.00,ABC Homes Ltd,INV-2026-015,INV-2026-015
```

Rules:
- Use one bank account per import file.
- Use signed amounts in one `Amount` column: positive for money in, negative for money out.
- Use plain numeric amounts: no currency symbols, no thousands separators, no CR/DR suffixes.
- Use a Xero-supported date format. For New Zealand users, prefer `DD/MM/YYYY`.
- Remove blank rows.
- Do not include zero-value transactions.
- Keep references within 255 characters and cheque numbers within 20 characters if those fields are used.
- Split large files before import; Xero says files with more than 1,000 bank transactions need splitting, and precoded files may need smaller batches.
- Expect Xero to detect and exclude duplicates for OFX/QFX/QIF/QuickBooks imports. For CSV, still de-duplicate locally before export because CSV duplicate behavior is more error-prone.

### Precoded bank statement CSV

A Xero precoded CSV is not just a categorised statement. When successfully imported, Xero:

1. Creates bank statement lines.
2. Creates spend money or receive money transactions from the imported details.
3. Reconciles those bank statement lines against the created transactions.

Mandatory fields for a successful precoded import are:

- `Date`
- `Amount`
- `Account Code`
- `Tax Rate (Display Name)` mapped to Xero's `Tax Type` field during import.

Recommended/optional fields include:

- `Payee`
- `Description`
- `Reference`
- `Cheque number`
- `Tracking1`
- `Tracking2`
- `Transaction Type`
- `Analysis code`

The skill's export column names should stay easy to map in Xero:

```csv
Date,Amount,Payee,Description,Reference,AccountCode,TaxType,ContactName
15/03/2026,-174.00,Bunnings Warehouse,BUNNINGS EFTPOS,CARD123,310,15% GST on Expenses,Bunnings Warehouse
17/03/2026,9775.00,ABC Homes Ltd,INV-2026-015,INV-2026-015,200,15% GST on Income,ABC Homes Ltd
```

Rules:
- `AccountCode` must be the account code only, not the account name.
- `TaxType` should be the exact tax rate display name from the user's Xero organisation.
- For New Zealand Xero organisations, common default tax rate display names include `15% GST on Expenses`, `15% GST on Income`, and `No GST`, but users can change names or create custom rates. Validate against the user's own settings where possible.
- `ContactName`/payee should match an existing Xero contact exactly where possible, otherwise duplicate contacts may be created.
- Do not invent Xero account codes. Require `mappings/xero-account-map.json` or explicit user/accountant input.
- If a precoded file is missing a mandatory field, Xero may import statement lines without creating reconciled transactions. The skill should fail validation before generating such a file.

## Direct IRD Filing Without Xero

### Normal small-business path: myIR or paper return

For a normal GST-registered small business not using Xero or another approved software integration, the direct path is usually:

1. Prepare totals from bookkeeping records.
2. Log in to myIR.
3. Open the GST account return for the filing period.
4. Choose either `GST amounts` or `Total sales and purchases`.
5. Enter sales/income, purchases/expenses, and any credit/debit adjustments.
6. Review the assessment.
7. Submit and pay or receive refund.

IRD says the user needs:

- total sales and income
- total purchases and expenses
- adjustments from the GST calculation sheet

The GST101A paper/PDF return uses boxes that map cleanly to skill output:

| Box | Meaning | Skill output |
| --- | --- | --- |
| 5 | Total sales and income including GST and zero-rated supplies | `total_sales_income_incl_gst` |
| 6 | Zero-rated supplies included in Box 5 | `zero_rated_supplies` |
| 7 | Box 5 minus Box 6 | calculated |
| 8 | Box 7 x 3/23 | `gst_collected_on_sales` |
| 9 | Debit adjustments | user/accountant adjustment |
| 10 | Box 8 + Box 9 | total GST collected |
| 11 | Total purchases and expenses including GST, excluding imported goods | `total_purchases_expenses_incl_gst` |
| 12 | Box 11 x 3/23 | `gst_credit_on_purchases` |
| 13 | Credit adjustments | user/accountant adjustment |
| 14 | Box 12 + Box 13 | total GST credit |
| 15 | Box 10 minus Box 14 | GST to pay or refund |

Implementation implication: the skill should produce an IRD-ready GST summary and GST101A-style worksheet. It should not imply that a generic CSV can be uploaded directly to IRD for GST filing through myIR.

### Attachments and documents

myIR may allow receipts/correspondence to be attached when filing a GST return, and IRD has separate "send us a document" flows when IRD requests documents. Attachments support evidence or correspondence; they are not a substitute for filing the GST return figures.

For gateway services, IRD's document service can upload supporting material with a return. The public intermediary page says the document service supports associated returns, has a 9 MB maximum file size, and uploading documents does not hold a return or trigger manual intervention.

### Software/gateway path

IRD offers GST and income tax filing through gateway services for digital service providers. For GST, the return service can file and amend returns, retrieve due dates/status, and retrieve filed returns. Access to the detailed technical documentation requires registering the organisation or using the Gateway Customer Support Portal.

Gateway-service implications:
- The skill should not claim to file directly through IRD unless the project becomes an approved digital service provider integration.
- Direct API filing would require myIR logon/access rights, OAuth/gateway setup, approval/onboarding, security review, and use of IRD's return service.
- A local open-source skill can still generate the figures and workpapers needed for manual myIR filing.

## Record Keeping and Legal Requirements

### Retention and storage

IRD record-keeping guidance says businesses must keep records, including electronic records, for at least 7 tax years. Records must be in English or Māori unless IRD approves another language. If records are stored offshore, the taxpayer or cloud provider needs IRD approval.

The Goods and Services Tax Act 1985, section 75, says GST records include books of account in manual/mechanical/electronic form, vouchers, bank statements, invoices, taxable supply information, supply correction information, receipts, and other documents needed to verify accounting entries. Section 75 requires records sufficient for IRD to readily ascertain GST liability and requires retention for at least 7 years after the end of the taxable period.

Implementation implication: keep original evidence under `inbox/`, normalized JSON under `ledger/`, exportable CSV/XLSX under `outputs/`, and keep mapping/system documentation under `mappings/` or `references/`.

### Computer audit readiness

IRD says computer-based records must:

- confirm tax liability
- be in English or te reo Māori unless approved otherwise
- contain legally required information
- be kept for at least 7 years
- be retrievable and readable at all times

IRD lists useful audit data formats including text, delimited files such as CSV/tab/pipe, MS Access, DBF, print files, and XML.

Implementation implication: JSON is useful internally, but the skill should always be able to export CSV/XLSX audit packs with record layouts and field explanations.

### Taxable supply information

Since 1 April 2023, New Zealand GST rules replaced "tax invoice" terminology with "taxable supply information" and related supply correction information. IRD says various records, such as invoices, bank statements, supplier agreements, and contracts, can support GST return figures either alone or in combination.

For ordinary supplies, IRD's March 2026 GST guide describes the buyer/seller record requirements by value:

- $200 or less: seller name or trade name, date of invoice or time of supply, description of goods/services, and total consideration. Seller GST number and buyer details are not required.
- More than $200 and up to $1,000: seller name or trade name, seller GST number, date of invoice or time of supply, description, and either GST-exclusive/GST/GST-inclusive amounts or a GST-inclusive amount plus a statement that GST is included at the standard rate.
- More than $1,000: the same information as the $200-$1,000 band, plus buyer details if the buyer is GST registered. Buyer details means buyer name plus at least one identifying item such as address, phone number, email address, trading name, New Zealand Business Number, or website URL.

IRD's 2026 compliance simplification commentary says the buyer-detail requirement for supplies over $1,000 is limited to GST-registered buyers. This matters because an unregistered buyer cannot claim GST input tax.

Implementation implication: receipt extraction should grade evidence completeness by threshold and mark missing GST registration number, recipient details, or GST amount where required.

## Sources

- Xero Central: About manually importing bank statements — https://central.xero.com/s/article/About-manually-importing-bank-statements
- Xero Central: Import a precoded bank statement in CSV format — https://central.xero.com/s/article/Import-a-precoded-CSV-bank-statement
- Xero Central: Resolve errors when manually importing a bank statement — https://central.xero.com/s/article/Troubleshoot-a-bank-statement-manual-import-error-CA
- Xero Developer: Accounting API Tax Rates — https://developer.xero.com/documentation/api/accounting/taxrates
- Inland Revenue: File your GST return — https://www.ird.govt.nz/gst/filing-and-paying-gst-and-refunds/filing-gst/file-your-gst-return
- Inland Revenue: Filing GST — https://www.ird.govt.nz/gst/filing-and-paying-gst-and-refunds/filing-gst
- Inland Revenue: GST for digital service providers — https://www.ird.govt.nz/digital-service-providers/services-catalogue/returns-and-information/goods-and-services-tax
- Inland Revenue: Gateway services — https://www.ird.govt.nz/topics/intermediaries/gateway-services
- Inland Revenue: Record keeping — https://www.ird.govt.nz/managing-my-tax/record-keeping
- Inland Revenue: Computer record keeping for audit — https://www.ird.govt.nz/managing-my-tax/record-keeping/computer-record-keeping-for-audit
- Inland Revenue: How taxable supply information for GST works — https://www.ird.govt.nz/gst/tax-invoices-for-gst/how-tax-invoices-for-gst-work
- New Zealand Legislation: Goods and Services Tax Act 1985 — https://www.legislation.govt.nz/act/public/1985/0141/latest/DLM82419.html
