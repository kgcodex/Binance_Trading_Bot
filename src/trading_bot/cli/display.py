from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from trading_bot.client.models import OrderRequest, OrderResult

console = Console()


def show_welcome() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]Binance Futures Testnet Interactive Trading Bot.[/bold cyan]",
            border_style="cyan",
        )
    )


def show_order_request(order: OrderRequest) -> None:
    table = Table(title="Order Summary", show_header=False)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Symbol", order.symbol)
    table.add_row("Side", order.side)
    table.add_row("Type", order.order_type)
    table.add_row("Quantity", str(order.quantity))
    table.add_row("Price", str(order.price) if order.price is not None else "N/A")

    console.print(table)


def show_order_result(result: OrderResult) -> None:
    table = Table(title="Order Response", show_header=False)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Order ID", str(result.order_id))
    table.add_row("Status", result.status or "N/A")
    table.add_row("Executed Quantity", result.executed_qty or "N/A")
    table.add_row("Average Price", result.avg_price or "N/A")

    console.print(table)
    console.print(_build_result_panel(result))


def show_error(message: str) -> None:
    console.print(Panel(message, title="Error", border_style="red"))


def show_info(message: str) -> None:
    console.print(f"[yellow]{message}[/yellow]")


def _build_result_panel(result: OrderResult) -> Panel:
    status = (result.status or "").upper()

    if result.order_type == "MARKET":
        if status == "FILLED":
            message = "MARKET order executed successfully."
            style = "green"
        else:
            message = (
                "MARKET order was accepted, but execution could not be confirmed "
                "from the latest response."
            )
            style = "yellow"
    else:
        if status == "FILLED":
            message = "LIMIT order executed successfully."
            style = "green"
        elif status == "NEW":
            message = "LIMIT order placed successfully and is currently open."
            style = "green"
        else:
            message = f"LIMIT order placed with status: {result.status or 'UNKNOWN'}."
            style = "yellow"

    return Panel(message, title="Result", border_style=style)
