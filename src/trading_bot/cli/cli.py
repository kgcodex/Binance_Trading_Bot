from __future__ import annotations

from argparse import ArgumentParser

from trading_bot.client.models import OrderRequest, OrderResult


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet."
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading symbol, e.g. BTCUSDT",
    )
    parser.add_argument(
        "--side",
        required=True,
        help="BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity, e.g. 0.001",
    )
    parser.add_argument(
        "--price",
        required=False,
        help="Price for LIMIT order only",
    )
    return parser


def print_order_request_summary(request: OrderRequest) -> None:
    print("\nOrder Request")
    print("-------------")
    print(f"Symbol   : {request.symbol}")
    print(f"Side     : {request.side}")
    print(f"Type     : {request.order_type}")
    print(f"Quantity : {request.quantity}")
    print(f"Price    : {request.price or 'N/A'}")


def print_order_result(result: OrderResult) -> None:
    print("\nOrder Response")
    print("--------------")
    print(f"Order ID          : {result.order_id}")
    print(f"Status            : {result.status or 'N/A'}")
    print(f"Executed Quantity : {result.executed_qty or 'N/A'}")
    print(f"Average Price     : {result.avg_price or 'N/A'}")

    if result.order_type == "MARKET":
        if result.status == "FILLED":
            print("\nResult: MARKET Order placed successfully.")
        else:
            print(
                "\nMarket order was accepted, but execution could not be confirmed from the latest response."
            )

    elif result.order_type == "LIMIT":
        if result.status == "FILLED":
            print("\nLIMIT order executed successfully.")
        elif result.status == "NEW":
            print("\nLIMIT order placed successfully and is currently open.")
        else:
            print(f"\nLIMIT order placed with status: {result.status or 'UNKNOWN'}.")
