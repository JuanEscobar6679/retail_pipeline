"""
Retail Analytics Pipeline - Schema Definition
Author: Juan Alejandro Escobar Mendoza
Purpose: Defines data entities and interaction classes for retail pipeline.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Dict


@dataclass(frozen=True)
class TransactionRecord:
    """
    Immutable representation of a validated retail transaction record.
    Encapsulates validated attributes and standardized field types.
    """

    transaction_id: str
    branch_id: str
    transaction_date: date
    customer_tier: str
    item_count: int
    raw_revenue: float
    tax_rate: float

    @property
    def net_revenue(self) -> float:
        """Calculates net revenue after applying regional tax rate."""
        return round(self.raw_revenue * (1.0 + self.tax_rate), 2)


class PipelineSummary:
    """
    Encapsulates a collection of TransactionRecord objects and aggregates
    operational and business statistics. Demonstrates class interaction.
    """

    def __init__(self, records: List[TransactionRecord], total_ingested: int):
        self.records: List[TransactionRecord] = records
        self.total_ingested: int = total_ingested

    @property
    def clean_record_count(self) -> int:
        """Returns total valid records retained."""
        return len(self.records)

    @property
    def retention_rate(self) -> float:
        """Calculates clean record retention percentage."""
        if self.total_ingested == 0:
            return 0.0
        return round((self.clean_record_count / self.total_ingested) * 100, 2)

    def total_gross_sales(self) -> float:
        """Sums net revenue across all retained records."""
        return round(sum(record.net_revenue for record in self.records), 2)

    def branch_performance(self) -> Dict[str, float]:
        """Calculates total net revenue aggregated by branch ID."""
        branch_totals: Dict[str, float] = {}
        for record in self.records:
            branch_totals[record.branch_id] = (
                branch_totals.get(record.branch_id, 0.0) + record.net_revenue
            )
        return branch_totals

    def customer_tier_breakdown(self) -> Dict[str, int]:
        """Counts transaction occurrences grouped by customer tier."""
        tier_counts: Dict[str, int] = {}
        for record in self.records:
            tier_counts[record.customer_tier] = (
                tier_counts.get(record.customer_tier, 0) + 1
            )
        return tier_counts
