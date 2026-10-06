"""
Agentic Price Drop Refund Arbiter (Zero External Dependencies)
Monitors post-purchase transactions, checks price-protection windows, and generates refund claims.
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

MERCHANT_POLICY_DAYS = {
    "SHOPIFY": 14,
    "WALMART": 30,
    "BESTBUY": 15,
    "TARGET": 14,
    "AMAZON": 7,
    "GENERIC": 14
}

class AgenticPriceDropRefundArbiter:
    def __init__(self, min_savings_threshold_usd: float = 2.0):
        self.min_threshold = min_savings_threshold_usd
        self.receipts: Dict[str, Dict[str, Any]] = {}

    def register_receipt(
        self,
        receipt_id: str,
        merchant: str,
        sku: str,
        product_name: str,
        purchase_price: float,
        purchase_timestamp: Optional[float] = None
    ) -> Dict[str, Any]:
        """Registers a completed transaction for post-purchase price monitoring."""
        merchant_norm = merchant.upper()
        p_time = purchase_timestamp or time.time()
        window_days = MERCHANT_POLICY_DAYS.get(merchant_norm, 14)
        expiration_time = p_time + (window_days * 86400)

        record = {
            "receipt_id": receipt_id,
            "merchant": merchant_norm,
            "sku": sku,
            "product_name": product_name,
            "purchase_price": float(purchase_price),
            "purchase_timestamp": p_time,
            "window_days": window_days,
            "window_expires_at": expiration_time,
            "status": "MONITORING"
        }
        self.receipts[receipt_id] = record
        return record

    def evaluate_price_drop(
        self,
        receipt_id: str,
        current_market_price: float,
        competitor_source: str = "Official Retailer Listing"
    ) -> Dict[str, Any]:
        """Evaluates whether an observed price drop qualifies for an automated price-match refund."""
        if receipt_id not in self.receipts:
            return {"error": f"Receipt {receipt_id} not found in monitoring registry"}

        receipt = self.receipts[receipt_id]
        now = time.time()
        orig_price = receipt["purchase_price"]
        curr_price = float(current_market_price)
        price_delta = round(orig_price - curr_price, 2)

        # Check time window validity
        is_within_window = now <= receipt["window_expires_at"]
        remaining_days = max(0.0, round((receipt["window_expires_at"] - now) / 86400, 1))

        # Check savings threshold
        meets_threshold = price_delta >= self.min_threshold

        eligible = is_within_window and meets_threshold

        return {
            "receipt_id": receipt_id,
            "merchant": receipt["merchant"],
            "sku": receipt["sku"],
            "original_price": orig_price,
            "current_price": curr_price,
            "potential_refund_usd": max(0.0, price_delta),
            "is_within_guarantee_window": is_within_window,
            "remaining_window_days": remaining_days,
            "eligible_for_claim": eligible,
            "claim_reason": "Price drop exceeds minimum threshold within policy window" if eligible else "Not eligible (window expired or price delta too small)"
        }

    def synthesize_refund_claim(
        self,
        receipt_id: str,
        current_market_price: float,
        proof_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synthesizes formal refund claim letter and merchant API payload."""
        eval_res = self.evaluate_price_drop(receipt_id, current_market_price)
        if not eval_res.get("eligible_for_claim"):
            return {
                "success": False,
                "reason": eval_res.get("claim_reason", "Not eligible"),
                "evaluation": eval_res
            }

        receipt = self.receipts[receipt_id]
        claim_id = "CLAIM-" + hashlib.sha256(f"{receipt_id}:{current_market_price}".encode("utf-8")).hexdigest()[:10].upper()
        
        claim_letter = (
            f"Dear {receipt['merchant']} Customer Support,\n\n"
            f"I am requesting a price protection adjustment for Order/Receipt #{receipt['receipt_id']}.\n"
            f"Item: {receipt['product_name']} (SKU: {receipt['sku']})\n"
            f"Original Purchase Price: ${receipt['purchase_price']:.2f}\n"
            f"Current Advertised Price: ${current_market_price:.2f}\n"
            f"Refund Amount Due: ${eval_res['potential_refund_usd']:.2f}\n"
            f"Verified Reference URL: {proof_url or 'https://retailer.com/item/' + receipt['sku']}\n\n"
            f"Under your {receipt['window_days']}-day Price Match Guarantee, please credit this difference back to the original payment method.\n\n"
            f"Thank you,\nGenPark Autonomous Commerce Agent"
        )

        receipt["status"] = "CLAIM_FILED"

        return {
            "success": True,
            "claim_id": claim_id,
            "receipt_id": receipt_id,
            "refund_amount_usd": eval_res["potential_refund_usd"],
            "claim_letter": claim_letter,
            "merchant_webhook_payload": {
                "event": "price_protection_refund_request",
                "order_id": receipt_id,
                "sku": receipt["sku"],
                "credit_amount": eval_res["potential_refund_usd"],
                "claim_id": claim_id
            }
        }
