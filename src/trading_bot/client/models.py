from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

OrderSide = Literal["BUY", "SELL"]
OrderType = Literal["MARKET", "LIMIT"]


@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    price: Decimal | None = None


@dataclass(frozen=True)
class OrderResult:
    symbol: str
    side: str
    order_type: str
    order_id: int | str | None
    status: str | None
    executed_qty: str | None
    avg_price: str | None
