from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import cast, get_args

from trading_bot.client.exceptions import ValidationError
from trading_bot.client.models import OrderRequest, OrderSide, OrderType


# Only valid positive number
def parse_positive_decimal(value: str, field_name: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc

    if parsed <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")

    return parsed


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()

    if not symbol:
        raise ValidationError("symbol is required.")

    if not symbol.isalnum():
        raise ValidationError("symbol must contain only letters and numbers.")

    return symbol


def validate_side(side: str) -> OrderSide:
    side = side.strip().upper()

    if side not in get_args(OrderSide):
        raise ValidationError("side must be BUY or SELL.")

    return cast(OrderSide, side)


def validate_order_type(order_type: str) -> OrderType:
    order_type = order_type.strip().upper()

    if order_type not in get_args(OrderType):
        raise ValidationError("order type must be MARKET or LIMIT.")

    return cast(OrderType, order_type)


def validate_order_request(
    *,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> OrderRequest:

    # Validate all the inputs
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_order_type = validate_order_type(order_type)
    validated_quantity = parse_positive_decimal(quantity, "quantity")

    validated_price = None
    if validated_order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required for LIMIT orders.")
        validated_price = parse_positive_decimal(price, "price")
    else:
        if price is not None:
            raise ValidationError("price should not be provided for MARKET orders.")

    return OrderRequest(
        symbol=validated_symbol,
        side=validated_side,
        order_type=validated_order_type,
        quantity=validated_quantity,
        price=validated_price,
    )
