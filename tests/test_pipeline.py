"""
Retail Analytics Pipeline - Unit Testing Suite
Author: Juan Alejandro Escobar Mendoza
Purpose: Executes unit testing coverage using standard library unittest module.
"""

import unittest
from datetime import date
from pipeline.schema import TransactionRecord, PipelineSummary
from pipeline.validator import validate_transaction_dict, process_raw_dataset
from pipeline.transformer import (
    filter_high_value_transactions,
    filter_by_customer_tier,
    extract_transaction_ids,
)


class TestRetailPipeline(unittest.TestCase):

    def test_transaction_record_net_revenue_calculation(self):
        """Validates net revenue formula application."""
        record = TransactionRecord(
            transaction_id="TX999",
            branch_id="TEST-01",
            transaction_date=date(2026, 10, 1),
            customer_tier="VIP",
            item_count=2,
            raw_revenue=100.0,
            tax_rate=0.10,
        )
        self.assertEqual(record.net_revenue, 110.0)

    def test_validate_transaction_dict_valid_entry(self):
        """Validates successful conversion of a valid raw dictionary."""
        raw = {
            "transaction_id": "TX100",
            "branch_id": "BRANCH-A",
            "transaction_date": "2026-10-15",
            "customer_tier": "REGULAR",
            "item_count": 5,
            "raw_revenue": 200.0,
            "tax_rate": 0.05,
        }
        record = validate_transaction_dict(raw)
        self.assertEqual(record.transaction_id, "TX100")
        self.assertEqual(record.net_revenue, 210.0)

    def test_validate_transaction_dict_invalid_date_raises_error(self):
        """Ensures improper date formats raise a ValueError."""
        raw = {
            "transaction_id": "TX101",
            "branch_id": "BRANCH-A",
            "transaction_date": "15-10-2026",
            "customer_tier": "REGULAR",
            "item_count": 1,
            "raw_revenue": 50.0,
            "tax_rate": 0.05,
        }
        with self.assertRaises(ValueError):
            validate_transaction_dict(raw)

    def test_process_raw_dataset_filtering(self):
        """Ensures corrupt entries are safely skipped in process_raw_dataset."""
        dataset = [
            {
                "transaction_id": "TX1",
                "branch_id": "B1",
                "transaction_date": "2026-10-01",
                "customer_tier": "VIP",
                "item_count": 1,
                "raw_revenue": 100.0,
                "tax_rate": 0.10,
            },
            {
                "transaction_id": "TX2",
                "branch_id": "B1",
                "transaction_date": "2026-10-01",
                "customer_tier": "VIP",
                "item_count": 1,
                "raw_revenue": -50.0,  # Invalid negative revenue
                "tax_rate": 0.10,
            },
        ]
        clean_records, total = process_raw_dataset(dataset)
        self.assertEqual(total, 2)
        self.assertEqual(len(clean_records), 1)
        self.assertEqual(clean_records[0].transaction_id, "TX1")

    def test_functional_transformers(self):
        """Validates map and filter operations on records."""
        r1 = TransactionRecord("TX1", "B1", date(2026, 10, 1), "VIP", 1, 100.0, 0.0)
        r2 = TransactionRecord("TX2", "B1", date(2026, 10, 1), "REGULAR", 1, 50.0, 0.0)
        records = [r1, r2]

        ids = extract_transaction_ids(records)
        self.assertEqual(ids, ["TX1", "TX2"])

        vip_records = filter_by_customer_tier(records, "VIP")
        self.assertEqual(len(vip_records), 1)
        self.assertEqual(vip_records[0].transaction_id, "TX1")

        high_val = filter_high_value_transactions(records, 80.0)
        self.assertEqual(len(high_val), 1)
        self.assertEqual(high_val[0].transaction_id, "TX1")

    def test_pipeline_summary_retention_rate(self):
        """Validates summary class aggregations."""
        r1 = TransactionRecord("TX1", "B1", date(2026, 10, 1), "VIP", 1, 100.0, 0.0)
        summary = PipelineSummary(records=[r1], total_ingested=2)
        self.assertEqual(summary.clean_record_count, 1)
        self.assertEqual(summary.retention_rate, 50.0)


if __name__ == "__main__":
    unittest.main()
