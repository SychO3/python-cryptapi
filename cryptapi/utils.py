"""
CryptAPI's Python Helper Utilities

This module provides common utility functions used by both synchronous and asynchronous
CryptAPI helpers.
"""

import urllib.parse


def prepare_url(url, params=None):
    """
    Helper method to append parameters to a URL and encode it.

    This method builds a properly formatted URL with query parameters.
    The URL is also URL encoded to ensure it's properly handled by the API.

    Args:
        url (str): Base URL to append parameters to.
        params (dict, optional): Dictionary of parameters to append. Defaults to None.

    Returns:
        str: URL encoded URL with parameters appended.
    """
    result_url = url

    if params:
        separator = "&" if "?" in url else "?"
        query_params = "&".join(f"{k}={v}" for k, v in params.items())
        result_url = f"{url}{separator}{query_params}"

    return urllib.parse.quote(result_url, safe=":/?=&")


def process_supported_coins(info_response):
    """
    Process the API response to extract supported cryptocurrencies.

    Args:
        info_response (dict): Response from the get_info API call.

    Returns:
        dict: Dictionary of supported coins with tickers as keys and names as values.
    """
    info = info_response.copy()

    info.pop("fee_tiers", None)

    coins = {}

    for ticker, coin_info in info.items():
        if "coin" in coin_info.keys():
            coins[ticker] = coin_info["coin"]
        else:
            for token, token_info in coin_info.items():
                coins[ticker + "_" + token] = (
                    token_info["coin"] + " (" + ticker.upper() + ")"
                )

    return coins
