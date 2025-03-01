"""
CryptAPI's Python Helper

This module provides a Python wrapper for the CryptAPI cryptocurrency payment gateway.
It allows developers to easily integrate cryptocurrency payments into their applications.

The CryptAPIHelper class provides methods for creating payment addresses, generating QR codes,
checking payment logs, and performing various cryptocurrency-related operations.
"""

import requests

from .exceptions import CryptAPIException
from .utils import process_supported_coins


class CryptAPIHelper:
    """
    Helper class for interacting with the CryptAPI cryptocurrency payment gateway.

    This class provides methods to create payment addresses, retrieve logs,
    generate QR codes, and perform other cryptocurrency-related operations.

    Attributes:
        CRYPTAPI_URL (str): Base URL for the CryptAPI service.
        CRYPTAPI_HOST (str): Host header value for API requests.
        coin (str): The cryptocurrency ticker (e.g., 'btc', 'eth', 'bep20_usdt').
        own_address (str): Your wallet address where funds will be forwarded.
        callback_url (str): URL that will be called when payment is received.
        parameters (dict): Custom parameters to be appended to the callback URL.
        ca_params (dict): Additional parameters for CryptAPI requests.
        payment_Address (str): Generated payment address for receiving funds.
    """

    CRYPTAPI_URL = "https://api.cryptapi.io/"
    CRYPTAPI_HOST = "api.cryptapi.io"

    def __init__(
        self, coin, own_address, callback_url, parameters=None, ca_params=None
    ):
        """
        Initialize a new CryptAPIHelper instance.

        Args:
            coin (str): The cryptocurrency ticker (e.g., 'btc', 'eth', 'bep20_usdt').
            own_address (str): Your wallet address where funds will be forwarded.
            callback_url (str): URL that will be called when payment is received.
            parameters (dict, optional): Custom parameters to append to callback URL. Defaults to {}.
            ca_params (dict, optional): Additional parameters for CryptAPI requests. Defaults to {}.

        Raises:
            Exception: If callback_url, coin, or own_address is missing.
        """
        if not parameters:
            parameters = {}

        if not ca_params:
            ca_params = {}

        if not callback_url:
            raise Exception("Callback URL is Missing")

        if not coin:
            raise Exception("Coin is Missing")

        if not own_address:
            raise Exception("Address is Missing")

        coin = coin.replace("/", "_")

        self.coin = coin
        self.own_address = own_address
        self.callback_url = callback_url
        self.parameters = parameters
        self.ca_params = ca_params
        self.payment_Address = ""

    def get_address(self):
        """
        Generate a new payment address for receiving cryptocurrency.

        This method creates a new payment address that forwards funds to your wallet,
        and sets up the callback notification.

        Returns:
            dict: Response from the CryptAPI service containing the generated address
                 and other payment information.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        coin = self.coin

        # 使用requests.PreparedRequest来处理URL，而不是调用_prepare_callback_url
        callback_url = self.callback_url

        if self.parameters:
            req = requests.models.PreparedRequest()
            req.prepare_url(self.callback_url, self.parameters)
            callback_url = req.url

        params = {"address": self.own_address, "callback": callback_url}

        if self.ca_params:
            params.update(self.ca_params)

        response_obj = CryptAPIHelper.process_request(
            coin, endpoint="create", params=params
        )

        if "address_in" in response_obj:
            self.payment_Address = response_obj["address_in"]

        return response_obj

    def get_logs(self):
        """
        Retrieve logs for the callback URL.

        This method fetches the payment logs associated with the current callback URL.

        Returns:
            dict: Response from the CryptAPI service containing the callback logs.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        coin = self.coin

        # 使用requests.PreparedRequest来处理URL，而不是完全编码
        callback_url = self.callback_url

        if self.parameters:
            req = requests.models.PreparedRequest()
            req.prepare_url(self.callback_url, self.parameters)
            callback_url = req.url

        params = {"callback": callback_url}

        return CryptAPIHelper.process_request(coin, endpoint="logs", params=params)

    def get_qrcode(self, value="", size=300):
        """
        Generate a QR code for the payment address.

        Args:
            value (str, optional): The amount to pay. Defaults to '' (empty string).
            size (int, optional): Size of the QR code in pixels. Defaults to 300.

        Returns:
            dict: Response from the CryptAPI service containing the QR code data.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        params = {"address": self.payment_Address, "size": size}

        if value:
            params["value"] = value

        return CryptAPIHelper.process_request(
            self.coin, endpoint="qrcode", params=params
        )

    def get_conversion(self, from_coin, value):
        """
        Get conversion rates between currencies.

        Args:
            from_coin (str): Source currency code (e.g., 'usd', 'eur').
            value (float): Amount to convert.

        Returns:
            dict: Response from the CryptAPI service containing conversion information.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        params = {"from": from_coin, "value": value}

        return CryptAPIHelper.process_request(
            self.coin, endpoint="convert", params=params
        )

    @staticmethod
    def get_info(coin=""):
        """
        Get information about a specific coin or all supported coins.

        Args:
            coin (str, optional): Coin ticker. If empty, returns info for all coins. Defaults to ''.

        Returns:
            dict: Response from the CryptAPI service containing coin information.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        return CryptAPIHelper.process_request(coin, endpoint="info")

    @staticmethod
    def get_supported_coins():
        """
        Get a list of all supported cryptocurrencies.

        Returns:
            dict: Dictionary of supported coins with tickers as keys and names as values.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        _info = CryptAPIHelper.get_info("")
        return process_supported_coins(_info)

    @staticmethod
    def get_estimate(coin, addresses=1, priority="default"):
        """
        Get an estimate of the network fees.

        Args:
            coin (str): Coin ticker.
            addresses (int, optional): Number of addresses. Defaults to 1.
            priority (str, optional): Transaction priority ('default', 'fast', 'fastest'). Defaults to 'default'.

        Returns:
            dict: Response from the CryptAPI service containing fee estimates.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        params = {"addresses": addresses, "priority": priority}

        return CryptAPIHelper.process_request(coin, endpoint="estimate", params=params)

    def _prepare_callback_url(self):
        """
        Process the callback URL by adding user parameters.

        This method appends the user parameters to the callback URL as query parameters.
        The callback URL is also URL encoded to ensure it's properly handled by the API.

        Returns:
            str: The processed and URL encoded callback URL with parameters.
        """
        if not self.parameters:
            return self.callback_url

        req = requests.models.PreparedRequest()
        req.prepare_url(self.callback_url, self.parameters)
        return req.url

    @staticmethod
    def process_request(coin=None, endpoint="", params=None):
        """
        Process an API request to the CryptAPI service.

        Args:
            coin (str, optional): Coin ticker. Defaults to None.
            endpoint (str, optional): API endpoint. Defaults to ''.
            params (dict, optional): Request parameters. Defaults to None.

        Returns:
            dict: JSON response from the API.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        if coin:
            if "/" not in coin:
                coin = coin.replace("_", "/")
            coin += "/"
        else:
            coin = ""

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=CryptAPIHelper.CRYPTAPI_URL,
                coin=coin,
                endpoint=endpoint,
            ),
            params=params,
            headers={"Host": CryptAPIHelper.CRYPTAPI_HOST},
        )

        response_obj = response.json()

        if response_obj.get("status") == "error":
            raise CryptAPIException(response_obj["error"])

        return response_obj
