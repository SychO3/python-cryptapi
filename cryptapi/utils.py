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
    
    for coin_ticker, coin_info in info_response.items():
        if isinstance(coin_info, dict) and "coin" in coin_info:
            result[coin_ticker] = coin_info.get("coin", "")
    
    if "tokens" in info_response and isinstance(info_response["tokens"], dict):
        for chain, tokens in info_response["tokens"].items():
            if isinstance(tokens, dict):
                for token_ticker, token_info in tokens.items():
                    key = f"{chain}/{token_ticker}"
                    result[key] = token_info.get("coin", "")
    
    return result
