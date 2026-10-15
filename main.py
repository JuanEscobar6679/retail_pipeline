"""
Retail Analytics Pipeline - Main Entrypoint
Author: Juan Alejandro Escobar Mendoza
Purpose: CLI execution script for running end-to-end data processing workflow.
"""

from pipeline.validator import process_raw_dataset
from pipeline.schema import PipelineSummary
from pipeline.reporter import print_summary_report


def get_sample_raw_dataset():
    """Generates a sample dataset containing valid transactions and corrupted entries for pipeline verification."""
    return [
            {"transaction_id": "TX1001",
            "branch_id": "TORONTO-01",
            "transaction_date": "2026-10-01",
            "customer_tier": "VIP",
            "item_count": 7,
            "raw_revenue": 180.00,
            "tax_rate": 0.11,},
        {"transaction_id": "TX1002",
            "branch_id": "TORONTO-01",
            "transaction_date": "2026-10-01",
            "customer_tier": "REGULAR",
            "item_count": 1,
            "raw_revenue": 17.80,
            "tax_rate": 0.10,},
        {"transaction_id": "TX1003",
            "branch_id": "VANCOUVER-02",
            "transaction_date": "2026-10-02",
            "customer_tier": "VIP",
            "item_count": 8,
            "raw_revenue": 420.00,
            "tax_rate": 0.18,},
        # Corrupted Record 1: Negative revenue (Should be skipped)
        {"transaction_id": "TX1004",
            "branch_id": "MONTREAL-01",
            "transaction_date": "2026-10-02",
            "customer_tier": "NEW",
            "item_count": 5,
            "raw_revenue": -80.00,
            "tax_rate": 0.15,},
        {"transaction_id": "TX1005",
            "branch_id": "MONTREAL-01",
            "transaction_date": "2026-10-03",
            "customer_tier": "NEW",
            "item_count": 2,
            "raw_revenue": 110.00,
            "tax_rate": 0.15,},
        # Corrupted Record 2: Invalid Date Format (Should be skipped)
        {"transaction_id": "TX1006",
            "branch_id": "VANCOUVER-02",
            "transaction_date": "03-10-2026",
            "customer_tier": "REGULAR",
            "item_count": 1,
            "raw_revenue": 25.00,
            "tax_rate": 0.12,},
        {"transaction_id": "TX1007",
            "branch_id": "TORONTO-01",
            "transaction_date": "2026-10-04",
            "customer_tier": "VIP",
            "item_count": 4,
            "raw_revenue": 210.00,
            "tax_rate": 0.13,},]


def main():
    """Executes the data processing pipeline workflow."""
    raw_data = get_sample_raw_dataset()
    clean_records, total_ingested = process_raw_dataset(raw_data)
    summary = PipelineSummary(records=clean_records, total_ingested=total_ingested)
    print_summary_report(summary)


if __name__ == "__main__":
    main()
