"""
Retail Analytics Pipeline - Data Validation Module
Author: Juan Alejandro Escobar Mendoza
Purpose: Cleans raw retail dictionary records, handles exceptions, and enforces types.
"""

from datetime import datetime
from typing import List, Dict, Any, Tuple
from pipeline.schema import TransactionRecord


def parse_iso_date(date_str: str):
    """Converts a YYYY-MM-DD string into a datetime.date object."""
    if not isinstance(date_str, str):
        raise ValueError("Date must be a string format YYYY-MM-DD.")
    return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()


def validate_transaction_dict(raw_data: Dict[str, Any]) -> TransactionRecord:
    """
    Validates dictionary fields and type conversions for a single transaction record.
    Raises ValueError or TypeError if mandatory validations fail.
    """
    required_keys = [
        "transaction_id",
        "branch_id",
        "transaction_date",
        "customer_tier",
        "item_count",
        "raw_revenue",
        "tax_rate",
    ]

    for key in required_keys:
        if key not in raw_data or raw_data[key] is None:
            raise ValueError(f"Missing mandatory field: {key}")

    tx_id = str(raw_data["transaction_id"]).strip()
    branch = str(raw_data["branch_id"]).strip()
    tier = str(raw_data["customer_tier"]).strip()

    if not tx_id or not branch or not tier:
        raise ValueError("String identifier fields cannot be empty.")

    parsed_date = parse_iso_date(raw_data["transaction_date"])

    item_count = int(raw_data["item_count"])
    if item_count <= 0:
        raise ValueError("item_count must be a positive integer.")

    raw_revenue = float(raw_data["raw_revenue"])
    if raw_revenue < 0.0:
        raise ValueError("raw_revenue cannot be negative.")

    tax_rate = float(raw_data["tax_rate"])
    if not (0.0 <= tax_rate <= 1.0):
        raise ValueError("tax_rate must be between 0.0 and 1.0.")

    return TransactionRecord(
        transaction_id=tx_id,
        branch_id=branch,
        transaction_date=parsed_date,
        customer_tier=tier,
        item_count=item_count,
        raw_revenue=raw_revenue,
        tax_rate=tax_rate,
    )


def process_raw_dataset(
    raw_dataset: List[Dict[str, Any]]
) -> Tuple[List[TransactionRecord], int]:
    """
    Processes a list of raw transaction dictionaries, filtering out corrupted rows.
    Returns clean TransactionRecord objects and total processed count.
    """
    clean_records: List[TransactionRecord] = []
    total_count = len(raw_dataset)

    for entry in raw_dataset:
        try:
            validated_record = validate_transaction_dict(entry)
            clean_records.append(validated_record)
        except (ValueError, TypeError, KeyError):
            # Gracefully ignore invalid or corrupt rows
            continue

    return clean_records, total_count
