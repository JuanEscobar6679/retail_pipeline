"""
Retail Analytics Pipeline - Functional Transformation Module
Author: Juan Alejandro Escobar Mendoza
Purpose: Demonstrates functional programming paradigms using map, filter, lambdas, and comprehensions.
"""

from typing import List, Dict, Callable, Any
from pipeline.schema import TransactionRecord


def filter_high_value_transactions(
    records: List[TransactionRecord], min_revenue: float
) -> List[TransactionRecord]:
    """Filters records exceeding a minimum net revenue using filter() and lambda."""
    return list(
        filter(lambda record: record.net_revenue >= min_revenue, records)
    )


def filter_by_customer_tier(
    records: List[TransactionRecord], tier: str
) -> List[TransactionRecord]:
    """Filters records matching a specific customer tier using filter() and lambda."""
    normalized_tier = tier.strip().upper()
    return list(
        filter(
            lambda record: record.customer_tier.upper() == normalized_tier,
            records,
        )
    )


def extract_transaction_ids(records: List[TransactionRecord]) -> List[str]:
    """Extracts transaction IDs using map() and lambda."""
    return list(map(lambda record: record.transaction_id, records))


def apply_custom_transformation(
    records: List[TransactionRecord],
    transform_func: Callable[[TransactionRecord], Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Higher-order function applying a transformation function to each record using map()."""
    return list(map(transform_func, records))


def compute_branch_averages(
    records: List[TransactionRecord],
) -> Dict[str, float]:
    """Computes average net revenue per branch using dict comprehension and list aggregation."""
    branches = {record.branch_id for record in records}
    return {
        branch: round(
            sum(
                r.net_revenue for r in records if r.branch_id == branch
            )
            / len([r for r in records if r.branch_id == branch]),
            2,
        )
        for branch in branches
        if len([r for r in records if r.branch_id == branch]) > 0
    }
