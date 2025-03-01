"""
CryptAPI's Python Async Helper

This module provides an asynchronous Python wrapper for the CryptAPI cryptocurrency payment gateway.
It allows developers to easily integrate cryptocurrency payments into their applications using
modern Python async/await syntax for improved performance and scalability.

The AsyncCryptAPIHelper class provides asynchronous methods for creating payment addresses,
generating QR codes, checking payment logs, and performing various cryptocurrency-related operations.
"""

import aiohttp
import ssl
import certifi
from .utils import prepare_url, process_supported_coins


class CryptAPIException(Exception):
    """
    Exception raised for CryptAPI-specific errors.
    Used when the API returns an error response.
    """

    pass


class AsyncCryptAPIHelper:
    """
    Asynchronous helper class for interacting with the CryptAPI cryptocurrency payment gateway.

    This class provides asynchronous methods to create payment addresses, retrieve logs,
    generate QR codes, and perform other cryptocurrency-related operations. All methods
    are designed to be used with Python's async/await syntax for non-blocking operation.

    Attributes:
        CRYPTAPI_URL (str): Base URL for the CryptAPI service.
        CRYPTAPI_HOST (str): Host header value for API requests.
        coin (str): The cryptocurrency ticker (e.g., 'btc', 'eth', 'bep20_usdt').
        own_address (str): Your wallet address where funds will be forwarded.
        callback_url (str): URL that will be called when payment is received.
        parameters (dict): Custom parameters to be appended to the callback URL.
        ca_params (dict): Additional parameters for CryptAPI requests.
        payment_Address (str): Generated payment address for receiving funds.
        ssl_context (ssl.SSLContext): SSL context for secure connections.
        conn (aiohttp.TCPConnector): TCP connector with SSL context.
    """

    CRYPTAPI_URL = "https://api.cryptapi.io/"
    CRYPTAPI_HOST = "api.cryptapi.io"

    def __init__(
        self, coin, own_address, callback_url, parameters=None, ca_params=None
    ):
        """
        Initialize a new AsyncCryptAPIHelper instance.

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

        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.conn = aiohttp.TCPConnector(ssl=self.ssl_context)

    async def get_address(self):
        """
        Asynchronously generate a new payment address for receiving cryptocurrency.

        This method creates a new payment address that forwards funds to your wallet,
        and sets up the callback notification.

        Returns:
            dict: Response from the CryptAPI service containing the generated address
                 and other payment information, or None if the request failed.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        coin = self.coin

        callback_url = prepare_url(self.callback_url, self.parameters)

        params = {"address": self.own_address, "callback": callback_url}

        if self.ca_params:
            params.update(self.ca_params)

        _address = await self.process_request(coin, endpoint="create", params=params)
        if _address:
            self.payment_Address = _address["address_in"]
            return _address

        return None

    async def get_logs(self):
        """
        Asynchronously retrieve logs for the callback URL.

        This method fetches the payment logs associated with the current callback URL.

        Returns:
            dict: Response from the CryptAPI service containing the callback logs.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        coin = self.coin
        callback_url = prepare_url(self.callback_url, self.parameters)

        params = {"callback": callback_url}

        return await self.process_request(coin, endpoint="logs", params=params)

    async def get_qrcode(self, value="", size=300):
        """
        Asynchronously generate a QR code for the payment address.

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

        return await self.process_request(self.coin, endpoint="qrcode", params=params)

    async def get_conversion(self, from_coin, value):
        """
        Asynchronously get conversion rates between currencies.

        Args:
            from_coin (str): Source currency code (e.g., 'usd', 'eur').
            value (float): Amount to convert.

        Returns:
            dict: Response from the CryptAPI service containing conversion information.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        params = {"from": from_coin, "value": value}

        return await self.process_request(self.coin, endpoint="convert", params=params)

    @staticmethod
    async def get_info(coin=""):
        """
        Asynchronously get information about a specific coin or all supported coins.

        Args:
            coin (str, optional): Coin ticker. If empty, returns info for all coins. Defaults to ''.

        Returns:
            dict: Response from the CryptAPI service containing coin information.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        return await AsyncCryptAPIHelper.process_request(coin, endpoint="info")

    @staticmethod
    async def get_supported_coins():
        """
        Asynchronously get a list of all supported cryptocurrencies.

        Returns:
            dict: Dictionary of supported coins with tickers as keys and names as values.

        Raises:
            CryptAPIException: If the API returns an error.
        """
        _info = await AsyncCryptAPIHelper.get_info("")
        return process_supported_coins(_info)

    @staticmethod
    async def get_estimate(coin, addresses=1, priority="default"):
        """
        Asynchronously get an estimate of the network fees.

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

        return await AsyncCryptAPIHelper.process_request(
            coin, endpoint="estimate", params=params
        )

    @staticmethod
    async def process_request(coin=None, endpoint="", params=None):
        """
        Process an asynchronous API request to the CryptAPI service.

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
            coin += "/"
        else:
            coin = ""

        url = "{base_url}{coin}{endpoint}/".format(
            base_url=AsyncCryptAPIHelper.CRYPTAPI_URL,
            coin=coin.replace("_", "/"),
            endpoint=endpoint,
        )

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.get(
                url=url,
                params=params,
                headers={"Host": AsyncCryptAPIHelper.CRYPTAPI_HOST},
            ) as response:
                response_obj = await response.json()

                if response_obj.get("status") == "error":
                    raise CryptAPIException(response_obj["error"])

                return response_obj
