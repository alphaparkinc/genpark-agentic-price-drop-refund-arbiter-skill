"""Example usage for AgenticPriceDropRefundArbiter."""
import sys
import json
from client import AgenticPriceDropRefundArbiter

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agentic Commerce Price Drop & Refund Arbiter Demo ===")
    arbiter = AgenticPriceDropRefundArbiter()

    # 1. Register post-purchase transaction
    print("\n--- 1. Registering Best Buy Purchase Receipt ---")
    receipt = arbiter.register_receipt(
        receipt_id="BB-2026-90412",
        merchant="BESTBUY",
        sku="APPLE-MBP-14",
        product_name="MacBook Pro 14-inch M4",
        purchase_price=1999.00
    )
    print(f"Registered Receipt #{receipt['receipt_id']}, Window: {receipt['window_days']} Days")

    # 2. Evaluate sudden retailer price drop
    print("\n--- 2. Evaluating Price Drop from $1999 to $1799 ---")
    evaluation = arbiter.evaluate_price_drop("BB-2026-90412", 1799.00)
    print(f"Eligible for Claim: {evaluation['eligible_for_claim']} (Savings: ${evaluation['potential_refund_usd']:.2f})")

    # 3. Synthesize autonomous refund claim letter
    print("\n--- 3. Synthesizing Retailer Price Protection Claim ---")
    claim = arbiter.synthesize_refund_claim("BB-2026-90412", 1799.00, "https://bestbuy.com/deal/APPLE-MBP-14")
    print(f"Claim ID: {claim['claim_id']}")
    print(claim["claim_letter"])

if __name__ == "__main__":
    main()
