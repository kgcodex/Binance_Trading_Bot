import sys

from trading_bot.cli.cli import (
    build_parser,
    print_order_request_summary,
    print_order_result,
)
from trading_bot.cli.interactive import run_interactive
from trading_bot.client.client import BinanceFuturesClient
from trading_bot.client.exceptions import (
    BinanceClientError,
    ValidationError,
)
from trading_bot.client.validators import validate_order_request
from trading_bot.logging.config import logger


def main() -> int:
    # Interactive CLI UX
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        return run_interactive()

    # Normal CLI
    parser = build_parser()
    args = parser.parse_args()

    try:
        order = validate_order_request(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        client = BinanceFuturesClient()
        result = client.place_order(order)

        print_order_request_summary(order)
        print_order_result(result)

        return 0

    except ValidationError as exc:
        print(f"\nResult: Failed to place order - {exc}")
        return 1

    except BinanceClientError as exc:
        logger.error(f"Binance client error:{exc}")
        print(f"\nResult: Failed to place order - {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
