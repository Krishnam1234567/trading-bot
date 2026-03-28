import re

def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not re.match(r"^[A-Z0-9]{3,20}$", symbol):
        raise ValueError(f"Invalid symbol format: '{symbol}'")
    return symbol

def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in ("BUY", "SELL"):
        raise ValueError(f"Invalid side: '{side}'")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    valid_types = ("MARKET", "LIMIT", "STOP_MARKET")
    if order_type not in valid_types:
        raise ValueError(f"Invalid order type: '{order_type}'")
    return order_type

def validate_quantity(qty: float) -> float:
    if qty <= 0:
        raise ValueError(f"Invalid quantity: {qty}")
    return qty

def validate_price(price: float, order_type: str) -> float:
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError(f"Price is required and must be > 0 for LIMIT orders.")
    return price

def validate_stop_price(stop_price: float, order_type: str) -> float:
    if order_type == "STOP_MARKET":
        if stop_price is None or stop_price <= 0:
            raise ValueError(f"Stop Price is required and must be > 0 for STOP_MARKET orders.")
    return stop_price
