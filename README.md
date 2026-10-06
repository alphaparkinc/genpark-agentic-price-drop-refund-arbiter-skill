# genpark-agentic-price-drop-refund-arbiter-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Skill-blue.svg)](https://genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Autonomous Post-Purchase Price Drop Monitor & Retailer Refund Claim Arbiter. Tracks online purchases across Shopify, Walmart, Best Buy, and Target, detects price drops within the merchant price-match guarantee window, verifies eligibility conditions, and synthesizes automated refund claims.

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License

Licensed under the [MIT License](LICENSE). Copyright © 2026 GenPark AI.
