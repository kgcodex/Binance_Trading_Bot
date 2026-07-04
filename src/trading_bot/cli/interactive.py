from __future__ import annotations

import questionary

from trading_bot.cli.display import (
    show_error,
    show_info,
    show_order_request,
    show_order_result,
    show_welcome,
)
from trading_bot.client.client import BinanceFuturesClient
from trading_bot.client.exceptions import BinanceClientError, ValidationError
from trading_bot.client.validators import validate_order_request
from trading_bot.logging.config import logger

SYMBOL_CHOICES = ["BTCUSDT"]


def run_interactive() -> int:
    show_welcome()
    try:
        symbol = questionary.select(
            "Select symbol",
            choices=SYMBOL_CHOICES,
        ).ask()
        if symbol is None:
            return 1

        side = questionary.select(
            "Select side",
            choices=["BUY", "SELL"],
        ).ask()
        if side is None:
            return 1

        order_type = questionary.select(
            "Select order type",
            choices=["MARKET", "LIMIT"],
        ).ask()
        if order_type is None:
            return 1

        quantity = questionary.text(
            "Enter quantity",
            validate=lambda text: _validate_non_empty(text, "Quantity is required."),
        ).ask()
        if quantity is None:
            return 1

        price: str | None = None
        if order_type == "LIMIT":
            price = questionary.text(
                "Enter limit price",
                validate=lambda text: _validate_non_empty(text, "Price is required."),
            ).ask()
            if price is None:
                return 1

        order = validate_order_request(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        show_order_request(order)

        confirmed = questionary.confirm(
            "Confirm order?",
            default=True,
        ).ask()

        if not confirmed:
            show_info("Order cancelled by user.")
            return 0

        client = BinanceFuturesClient()
        result = client.place_order(order)
        show_order_result(result)

        return 0

    except ValidationError as exc:
        logger.error(f"Validation error: {exc}")
        show_error(f"Failed to place order - {exc}")
        return 1

    except BinanceClientError as exc:
        logger.error(f"Binance client error: {exc}")
        show_error(f"Failed to place order - {exc}")
        return 1

    except KeyboardInterrupt:
        show_info("Operation cancelled.")
        return 1

    except Exception as exc:
        logger.exception(f"Unhandled error: {exc}")
        show_error(f"Failed to place order - unexpected error: {exc}")
        return 1


def _validate_non_empty(value: str, error_message: str) -> bool | str:
    if value.strip():
        return True
    return error_message
