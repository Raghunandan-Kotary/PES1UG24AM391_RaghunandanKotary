"""Digital Wallet & Payment Tracker Module.

Provides secure functions for balance top-up, PIN-authenticated merchant
payments, mini-statement generation, cashback calculation, and gateway check.
"""

import hashlib
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.getenv("GATEWAY_SECRET", "sk_demo_wallet_0000")
WALLET_PIN = os.getenv("WALLET_PIN", "4321")
wallet = {"balance": 0.0}
wallet_limits = {"daily_limit": 1000}
transactions = []


def hash_pin(pin: str) -> str:
    """Hash PIN using SHA-256 for secure verification."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def add_money(amount: float, source: str = "UPI", log: list = None) -> bool:
    """Add funds to the digital wallet balance and log transaction."""
    if log is None:
        log = []
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat()
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit: float) -> None:
    """Update maximum daily spending threshold."""
    wallet_limits["daily_limit"] = new_limit


def pay_merchant(merchant: str, amount: float, pin: str) -> bool:
    """Authorize payment to merchant after PIN and limit verification."""
    if hash_pin(pin) != hash_pin(WALLET_PIN):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > wallet_limits["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat()
    })
    return True


def mini_statement(count: int = 3) -> None:
    """Display recent transaction records from history."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount: float, merchant_type: str = "general") -> float:
    """Compute promotional cashback reward for payment."""
    _ = merchant_type
    return round(amount * 0.02, 2)


def check_gateway(secret: str) -> bool:
    """Verify payment gateway token against authorized secret."""
    return secret == GATEWAY_SECRET


def receipt_path() -> str:
    """Safely allocate a temporary file path for payment receipts."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        return temp_file.name


def main() -> None:
    """Run demonstration workflow for digital wallet operations."""
    otp = secrets.SystemRandom().randint(100000, 999999)
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        t["amount"] for t in transactions if t["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
