class TradingBotError(Exception):
    """Base application exception."""


class ValidationError(TradingBotError):
    """Raised when CLI/user input is invalid."""


class BinanceClientError(TradingBotError):
    """Raised when Binance API interaction fails."""
