from __future__ import annotations

import os
from typing import Any

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from trading_bot.client.exceptions import BinanceClientError
from trading_bot.client.models import OrderRequest, OrderResult
from trading_bot.logging.config import logger

# Base URL
TESTNET_BASE_URL = "https://testnet.binancefuture.com/fapi"

# Key Setup
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

if not api_key or not api_secret:
    raise BinanceClientError("Missing API_KEY or SECRET_KEY in environment.")


class BinanceFuturesClient:
    def __init__(self) -> None:
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = TESTNET_BASE_URL

    def place_order(self, order: OrderRequest) -> OrderResult:
        payload: dict[str, Any] = {
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "quantity": str(order.quantity),
        }

        if order.order_type == "LIMIT":
            payload["price"] = str(order.price)
            payload["timeInForce"] = "GTC"

        logger.info(f"Placing futures order | payload={payload}")

        try:
            response: dict[str, Any] = self.client.futures_create_order(**payload)

            # Fetch Order details in case of MARKET
            if order.order_type == "MARKET":
                response.update(
                    self.client.futures_get_order(
                        symbol=order.symbol, orderId=response.get("orderId")
                    )
                )

            logger.info(f"Order response received | response={response}")

            return OrderResult(
                symbol=order.symbol,
                side=order.side,
                order_type=order.order_type,
                order_id=response.get("orderId"),
                status=response.get("status"),
                executed_qty=response.get("executedQty"),
                avg_price=response.get("avgPrice"),
            )

        except BinanceAPIException as exc:
            logger.exception(
                f"Binance API error while placing order | payload={payload} | error={exc}"
            )
            raise BinanceClientError(f"Binance API error: {exc}") from exc

        except BinanceRequestException as exc:
            logger.exception(
                f"Network/request error while placing order | payload={payload} | error={exc}"
            )
            raise BinanceClientError(f"Network/request error: {exc}") from exc

        except Exception as exc:
            logger.exception(
                f"Unexpected error while placing order | payload={payload} | error={exc}",
            )
            raise BinanceClientError(f"Unexpected order error: {exc}") from exc
