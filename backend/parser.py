import pandas as pd

def parse_csv(filepath):
    """
    Parses the CSV file to extract transaction data.
    Assumes the file has columns: Date, Description, Debit, Credit, Balance.
    """
    try:
        df = pd.read_csv(filepath)

        # Normalize column names
        df.columns = [col.strip().lower() for col in df.columns]

        transactions = []
        for _, row in df.iterrows():
            transactions.append({
                "date": row.get("date"),
                "description": row.get("description"),
                "debit": float(row.get("debit", 0) or 0),
                "credit": float(row.get("credit", 0) or 0),
                "balance": float(row.get("balance", 0) or 0)
            })

        return transactions

    except Exception as e:
        return {"error": str(e)}


def validate_balance(transactions):
    """
    Validates if closing balance = opening balance + credits - debits
    Returns a validation result dictionary.
    """
    if not transactions or len(transactions) < 2:
        return {
            "error": "Not enough transactions to validate"
        }

    opening = transactions[0]["balance"]
    closing = transactions[-1]["balance"]
    total_credits = sum(t["credit"] for t in transactions)
    total_debits = sum(t["debit"] for t in transactions)
    expected_closing = opening + total_credits - total_debits
    is_valid = abs(expected_closing - closing) < 0.01  # margin of error

    return {
        "opening_balance": round(opening, 2),
        "total_credits": round(total_credits, 2),
        "total_debits": round(total_debits, 2),
        "calculated_closing_balance": round(expected_closing, 2),
        "actual_closing_balance": round(closing, 2),
        "is_valid": is_valid
    }
