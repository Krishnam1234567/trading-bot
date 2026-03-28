from typing import Dict, Any, Optional

from .client import BinanceTestnetClient
from .validators import (
    validate_symbol, 
    validate_side, 
    validate_quantity, 
    validate_price, 
    validate_stop_price
)

def place_order(
    client: BinanceTestnetClient, 
    symbol: str, 
    side: str, 
    order_type: str, 
    qty: float, 
    price: Optional[float] = None, 
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(qty)
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": qty
    }

    if order_type == "LIMIT":
        params["price"] = validate_price(price, order_type)
        params["timeInForce"] = "GTC"
    elif order_type == "STOP_MARKET":
        params["stopPrice"] = validate_stop_price(stop_price, order_type)
        
    return client.request("POST", "/fapi/v1/order", params)

def place_market_order(client: BinanceTestnetClient, symbol: str, side: str, qty: float) -> Dict[str, Any]:
    return place_order(client, symbol, side, "MARKET", qty)

def place_limit_order(client: BinanceTestnetClient, symbol: str, side: str, qty: float, price: float) -> Dict[str, Any]:
    return place_order(client, symbol, side, "LIMIT", qty, price=price)

def place_stop_market_order(client: BinanceTestnetClient, symbol: str, side: str, qty: float, stop_price: float) -> Dict[str, Any]:
    return place_order(client, symbol, side, "STOP_MARKET", qty, stop_price=stop_price)
