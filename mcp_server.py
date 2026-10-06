"""MCP Server for Agentic Price Drop Refund Arbiter."""
import sys
import json
import time
from client import AgenticPriceDropRefundArbiter

arbiter = AgenticPriceDropRefundArbiter()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "arbitrate_price_drop_refund":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "evaluate_price_drop")
    if action == "register_receipt":
        return arbiter.register_receipt(
            receipt_id=args.get("receipt_id", "REC-001"),
            merchant=args.get("merchant", "SHOPIFY"),
            sku=args.get("sku", "SKU-99"),
            product_name=args.get("product_name", "Wireless Headphones"),
            purchase_price=float(args.get("purchase_price", 100.0))
        )
    elif action == "evaluate_price_drop":
        return arbiter.evaluate_price_drop(
            receipt_id=args.get("receipt_id", "REC-001"),
            current_market_price=float(args.get("current_market_price", 80.0))
        )
    elif action == "synthesize_refund_claim":
        return arbiter.synthesize_refund_claim(
            receipt_id=args.get("receipt_id", "REC-001"),
            current_market_price=float(args.get("current_market_price", 80.0)),
            proof_url=args.get("competitor_url")
        )
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        arbiter.register_receipt("REC-TEST-88", "WALMART", "SONY-WH1000", "Sony Noise Cancelling Headphones", 349.99)
        ev = arbiter.evaluate_price_drop("REC-TEST-88", 299.99)
        assert ev["eligible_for_claim"] is True
        assert ev["potential_refund_usd"] == 50.0
        claim = arbiter.synthesize_refund_claim("REC-TEST-88", 299.99)
        assert claim["success"] is True
        assert "WALMART Customer Support" in claim["claim_letter"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticPriceDropRefundArbiter", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "arbitrate_price_drop_refund",
                            "description": "Register purchase receipts, monitor market price drops, verify price guarantee policies, and synthesize retailer refund claim requests.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["register_receipt", "evaluate_price_drop", "synthesize_refund_claim"]},
                                    "receipt_id": {"type": "string"},
                                    "merchant": {"type": "string"},
                                    "sku": {"type": "string"},
                                    "purchase_price": {"type": "number"},
                                    "current_market_price": {"type": "number"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
