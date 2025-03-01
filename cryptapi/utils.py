"""
CryptAPI's Python Helper Utilities

This module provides common utility functions used by both synchronous and asynchronous
CryptAPI helpers.
"""


def process_supported_coins(info_response):
    """
    Process the API response to extract supported cryptocurrencies.

    Args:
        info_response (dict): Response from the CryptAPI info endpoint.

    Returns:
        dict: Dictionary with coin tickers as keys and names as values.
    """
    result = {}
    coins = info_response.get("coins", [])

    for coin_type, coin_info in coins.items():
        for coin, details in coin_info.items():
            result[f"{coin_type}_{coin}"] = details.get("name", "")

    return result
