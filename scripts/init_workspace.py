#!/usr/bin/env python3
"""Initialize a local New Zealand Accounting Assistant bookkeeping workspace."""

import argparse
import json
import re
from datetime import date
from pathlib import Path


DEFAULT_ROOT = "~/KiwiBooks"
GLOBAL_CONFIG = "~/.openclaw/data/kiwi-receipts/config.json"


BUSINESS_DIRS = [
    "inbox",
    "ledger/periods",
    "ledger/tax-years",
    "ledger/registers",
    "ledger/indexes",
    "mappings",
    "working/reconciliations",
    "outputs/monthly",
    "outputs/ird/gst",
    "outputs/ird/ir3",
    "outputs/xero/standard",
    "outputs/xero/precoded",
    "outputs/accountant",
    "archive",
]


PERIOD_FILES = {
    "receipts.json": [],
    "income.json": [],
    "bank-transactions.json": [],
    "matches.json": [],
    "adjustments.json": [],
    "period-summary.json": {},
}


TAX_YEAR_FILES = {
    "assets.json": [],
    "depreciation.json": [],
    "income-tax.json": {},
    "provisional-tax.json": {},
    "annual-summary.json": {},
}


REGISTER_FILES = {
    "ledger/registers/contacts.json": [],
    "ledger/registers/assets-master.json": [],
    "ledger/registers/bank-accounts.json": [],
    "ledger/indexes/document-index.json": [],
}


MAPPING_FILES = {
    "mappings/categories.json": {},
    "mappings/xero-account-map.json": {
        "defaults": {
            "expense_tax_type": "No GST",
            "income_tax_type": "No GST",
            "no_gst_tax_type": "No GST",
        },
        "income": {},
        "categories": {},
    },
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "business"


def period_from_date(value: date) -> str:
    return f"{value.year:04d}-{value.month:02d}"


def tax_year_from_date(value: date) -> str:
    end_year = value.year + 1 if value.month >= 4 else value.year
    return f"{end_year - 1}-{end_year}"


def read_json(path: Path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def write_json_if_missing(path: Path, data) -> bool:
    if path.exists():
        return False
    write_json(path, data)
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize a New Zealand Accounting Assistant workspace")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="Bookkeeping root directory")
    parser.add_argument("--business-name", required=True, help="Business name")
    parser.add_argument("--slug", default=None, help="Business slug")
    parser.add_argument("--gst-registered", action="store_true", help="Business is registered for GST")
    parser.add_argument("--gst-number", default="", help="GST/IRD number")
    parser.add_argument("--gst-registered-from", default=None, help="GST registration start date, YYYY-MM-DD")
    parser.add_argument("--gst-deregistered-from", default=None, help="GST deregistration date, YYYY-MM-DD")
    parser.add_argument("--balance-date", default="31-march", help="Balance date")
    parser.add_argument("--gst-filing-frequency", default=None, help="GST filing frequency")
    parser.add_argument("--gst-accounting-basis", default=None, help="GST accounting basis")
    parser.add_argument("--depreciation-method", default="DV", help="Default depreciation method")
    parser.add_argument("--vehicle-business-percent", type=float, default=80)
    parser.add_argument("--phone-business-percent", type=float, default=70)
    parser.add_argument("--home-office-percent", type=float, default=0)
    parser.add_argument("--period", default=None, help="Initial monthly period to create, YYYY-MM")
    parser.add_argument("--tax-year", default=None, help="Initial tax year to create, YYYY-YYYY")
    parser.add_argument("--global-config", default=GLOBAL_CONFIG, help="Global pointer config path")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    slug = args.slug or slugify(args.business_name)
    business_dir = root / "businesses" / slug
    initial_period = args.period or period_from_date(date.today())
    initial_tax_year = args.tax_year or tax_year_from_date(date.today())

    created_dirs = []
    for rel in ["shared/chart-of-accounts", "shared/templates"]:
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(path))

    for rel in BUSINESS_DIRS:
        path = business_dir / rel
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(path))

    for source in ["receipts", "income", "bank-statements", "notes"]:
        path = business_dir / "inbox" / source / initial_period
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(path))

    period_dir = business_dir / "ledger" / "periods" / initial_period
    period_dir.mkdir(parents=True, exist_ok=True)
    created_dirs.append(str(period_dir))

    tax_year_dir = business_dir / "ledger" / "tax-years" / initial_tax_year
    tax_year_dir.mkdir(parents=True, exist_ok=True)
    created_dirs.append(str(tax_year_dir))

    created_files = []
    business_config_path = business_dir / "config.json"
    business_config = read_json(business_config_path, {})
    business_config.update({
        "schema_version": 2,
        "business_name": args.business_name,
        "balance_date": args.balance_date,
        "tax_year_start_month": 4,
        "tax_year_start_day": 1,
        "gst_registered": args.gst_registered,
        "gst_number": args.gst_number,
        "gst_registered_from": args.gst_registered_from,
        "gst_deregistered_from": args.gst_deregistered_from,
        "gst_filing_frequency": args.gst_filing_frequency,
        "gst_accounting_basis": args.gst_accounting_basis,
        "gst_registration_monitoring": {
            "enabled": True,
            "threshold_nzd": 60000,
            "lookback_months": 12,
            "forecast_months": 12,
        },
        "depreciation_method": args.depreciation_method,
        "vehicle_business_percent": args.vehicle_business_percent,
        "phone_business_percent": args.phone_business_percent,
        "home_office_percent": args.home_office_percent,
    })
    write_json(business_config_path, business_config)
    created_files.append(str(business_config_path))

    for filename, default in PERIOD_FILES.items():
        path = period_dir / filename
        if write_json_if_missing(path, default):
            created_files.append(str(path))

    for filename, default in TAX_YEAR_FILES.items():
        path = tax_year_dir / filename
        if write_json_if_missing(path, default):
            created_files.append(str(path))

    for rel, default in REGISTER_FILES.items():
        path = business_dir / rel
        if write_json_if_missing(path, default):
            created_files.append(str(path))

    mapping_files = dict(MAPPING_FILES)
    if args.gst_registered:
        mapping_files["mappings/xero-account-map.json"] = {
            "defaults": {
                "expense_tax_type": "15% GST on Expenses",
                "income_tax_type": "15% GST on Income",
                "no_gst_tax_type": "No GST",
            },
            "income": {},
            "categories": {},
        }

    for rel, default in mapping_files.items():
        path = business_dir / rel
        if write_json_if_missing(path, default):
            created_files.append(str(path))

    global_config_path = Path(args.global_config).expanduser().resolve()
    global_config = read_json(global_config_path, {})
    businesses = global_config.get("businesses") or {}
    businesses[slug] = str(business_dir)
    global_config.update({
        "books_root": str(root),
        "active_business": slug,
        "businesses": businesses,
    })
    write_json(global_config_path, global_config)
    created_files.append(str(global_config_path))

    print(json.dumps({
        "books_root": str(root),
        "active_business": slug,
        "business_dir": str(business_dir),
        "initial_period": initial_period,
        "initial_tax_year": initial_tax_year,
        "created_dirs": created_dirs,
        "touched_files": created_files,
    }, indent=2))


if __name__ == "__main__":
    main()
