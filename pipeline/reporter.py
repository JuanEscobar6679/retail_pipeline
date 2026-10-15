"""
Retail Analytics Pipeline - Reporting Module
Author: Juan Alejandro Escobar Mendoza
Purpose: Formats and prints aggregated pipeline statistics to standard output.
"""

from pipeline.schema import PipelineSummary
from pipeline.transformer import compute_branch_averages


def print_summary_report(summary: PipelineSummary) -> None:
    """Prints a formatted summary report of the processed transactions."""
    header = "=" * 60
    sub_header = "-" * 60

    print(header)
    print("           RETAIL ANALYTICS PIPELINE SUMMARY REPORT           ")
    print(header)
    print(f"Total Raw Records Ingested : {summary.total_ingested}")
    print(f"Clean Records Retained     : {summary.clean_record_count}")
    print(f"Data Retention Rate        : {summary.retention_rate:.2f}%")
    print(f"Total Gross Sales (Net)    : ${summary.total_gross_sales():,.2f}")
    print(sub_header)

    print("\nBRANCH PERFORMANCE (NET REVENUE)")
    print(sub_header)
    print(f"{'Branch ID':<20} | {'Total Net Sales':>20}")
    print(sub_header)

    branch_totals = summary.branch_performance()
    for branch, total in sorted(branch_totals.items()):
        print(f"{branch:<20} | ${total:>19,.2f}")

    print(sub_header)

    print("\nBRANCH PERFORMANCE (AVERAGE NET REVENUE PER TX)")
    print(sub_header)
    print(f"{'Branch ID':<20} | {'Average Sale':>20}")
    print(sub_header)

    branch_averages = compute_branch_averages(summary.records)
    for branch, avg in sorted(branch_averages.items()):
        print(f"{branch:<20} | ${avg:>19,.2f}")

    print(sub_header)

    print("\nCUSTOMER TIER BREAKDOWN")
    print(sub_header)
    print(f"{'Customer Tier':<20} | {'Transaction Count':>20}")
    print(sub_header)

    tier_counts = summary.customer_tier_breakdown()
    for tier, count in sorted(tier_counts.items()):
        print(f"{tier:<20} | {count:>20}")

    print(header)
