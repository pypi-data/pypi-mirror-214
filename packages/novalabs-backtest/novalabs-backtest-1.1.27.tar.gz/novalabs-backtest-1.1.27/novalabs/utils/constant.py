from typing import Dict

STD_CANDLE_FORMAT = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
]

VAR_NEEDED_FOR_POSITION = [
    "all_entry_time",
    "entry_signal",
    "all_entry_price",
    "all_exit_time",
    "all_exit_point",
    "take_profit",
    "stop_loss",
    "position_size",
]

DATA_FORMATING = {
    "binance": {
        "columns": [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "nb_of_trades",
            "taker_base_volume",
            "taker_quote_volume",
            "ignore",
        ],
        "num_var": [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_asset_volume",
            "nb_of_trades",
            "taker_base_volume",
            "taker_quote_volume",
        ],
        "date_var": ["open_time", "close_time"],
    },
    "ftx": {
        "columns": ["startTime", "time", "open", "high", "low", "close", "volume"],
        "num_var": ["open", "high", "low", "close", "volume"],
    },
    "bybit": {
        "columns": ["open_time", "open", "high", "low", "close", "volume", "turnover"],
        "num_var": ["open", "high", "low", "close", "volume", "turnover"],
    },
    "kraken": {
        "columns": ["open_time", "open", "high", "low", "close", "volume"],
        "num_var": [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
        "date_var": ["open_time", "close_time"],
    },
    "coinbase": {
        "columns": ["open_time", "low", "high", "open", "close", "volume"],
        "num_var": [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
        "date_var": ["open_time", "close_time"],
    },
    "kucoin": {
        "columns": ["open_time", "open", "high", "low", "close", "volume"],
        "num_var": [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
        "date_var": ["open_time", "close_time"],
    },
    "okx": {
        "columns": [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume_contract",
            "volume",
            "quote_asset_volume",
            "confirm",
        ],
        "num_var": [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "volume_contract",
            "volume",
            "quote_asset_volume",
        ],
        "date_var": ["open_time", "close_time"],
    },
    "btcex": {
        "columns": ["tick", "open", "high", "low", "close", "volume"],
        "num_var": ["open", "high", "low", "close", "volume"],
    },
}

FEES: Dict[str, float] = {
    "binance": 0.0002,
    "btcex": 0.0002,
    "bybit": 0.0001,
    "okx": 0.00015,
    "huobi": 0.0002,
    "kucoin": 0.0002,
    "oanda": 0.0001,
}

SECONDS_PER_UNIT: Dict[str, int] = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
}
