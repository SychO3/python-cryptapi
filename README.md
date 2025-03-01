[<img src="https://i.imgur.com/IfMAa7E.png" width="300"/>](image.png)


# CryptAPI's Python Library

Python implementation of CryptAPI's payment gateway with both synchronous and asynchronous support.

This library provides a simple and powerful interface to integrate cryptocurrency payments into your Python applications using the CryptAPI payment gateway. It supports all cryptocurrencies available on CryptAPI.

## Features

- Simple integration with CryptAPI payment gateway
- Support for all cryptocurrencies offered by CryptAPI
- Easy generation of payment addresses and QR codes
- Callback handling for payment notifications
- Real-time payment log retrieval
- Currency conversion utilities
- Fee estimation tools
- Support for both synchronous and asynchronous operations
- Utility functions for URL preparation and encoding

## Requirements:

```
Python >= 3.0
Requests >= 2.20
aiohttp >= 3.9.1 (for async support)
certifi >= 2024.2.2 (for async support)
```

## Installation

Install the package using pip:

```shell script
pip install python-cryptapi
```

Available [on PyPI](https://pypi.python.org/pypi/python-cryptapi) or [on GitHub](https://github.com/cryptapi/python-cryptapi)

## Usage

The library offers two main classes:
- `CryptAPIHelper`: For synchronous (blocking) API calls
- `AsyncCryptAPIHelper`: For asynchronous (non-blocking) API calls

### Importing in your project

```python
from cryptapi import CryptAPIHelper  # Synchronous API
from cryptapi import AsyncCryptAPIHelper  # Asynchronous API
```

### Basic Configuration

Both synchronous and asynchronous classes require the same initialization parameters:

```python
# Common parameters for both APIs
coin = 'btc'  # The cryptocurrency to use (e.g., 'btc', 'eth', 'bep20_usdt')
my_address = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'  # Your wallet address where funds will be forwarded
callback_url = 'https://example.com/payment/callback'  # URL that will be called when payment is received
params = {  # Custom parameters to append to callback URL
    'order_id': '12345',
    'customer_id': 'C12345'
}
cryptapi_params = {  # Additional parameters for CryptAPI
    'convert': 1,
    'multi_token': 1,
    'post': 1  # Use POST instead of GET for callbacks
}
```

### Generating a Payment Address

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

# Initialize the helper
ca = CryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)

# Generate a new payment address
result = ca.get_address()
address = result['address_in']
print(f"Payment address: {address}")

# Access other information in the result
print(f"Address URL: {result.get('address_url', '')}")
print(f"Minimum confirmations: {result.get('minimum_confirmations', '')}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    # Initialize the async helper
    ca = AsyncCryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)
    
    # Generate a new payment address
    result = await ca.get_address()
    address = result['address_in']
    print(f"Payment address: {address}")
    
    # Access other information in the result
    print(f"Address URL: {result.get('address_url', '')}")
    print(f"Minimum confirmations: {result.get('minimum_confirmations', '')}")

# Run the async function
asyncio.run(main())
```

The `get_address()` method returns a dictionary containing:
- `address_in`: The generated payment address
- `address_out`: Your own address where funds will be forwarded
- `callback_url`: The processed callback URL with your parameters
- `address_url`: URL to a CryptAPI page showing payment status
- And other information about the payment setup

### Getting Notified When Payment is Received

Once your customer makes a payment, CryptAPI will send a callback to your `callback_url`. The callback data includes:

- `address_in`: The payment address
- `address_out`: Your wallet address
- `coin`: The cryptocurrency used
- `confirmations`: Number of confirmations
- `txid_in`: Transaction ID on the blockchain
- `value`: Amount received
- And any custom parameters you provided in the `params` dictionary

By default, callbacks are sent as `GET` requests, but you can set `post: 1` in the `cryptapi_params` to receive `POST` requests instead.

> **Note**: The callback URL is automatically URL encoded to ensure it's properly handled by the API. The library preserves the structure of the URL by maintaining essential special characters (:/?=&) while encoding other characters that might cause issues.

For more details on callback parameters, refer to the [CryptAPI documentation](https://docs.cryptapi.io/#operation/confirmedcallbackget).

### Utility Functions

The library provides utility functions that you can use directly in your application:

```python
from cryptapi import prepare_url

# Prepare and encode a URL with parameters
base_url = "https://example.com/callback"
params = {"order_id": "12345", "customer_id": "C12345"}
encoded_url = prepare_url(base_url, params)
print(f"Encoded URL: {encoded_url}")
```

The `prepare_url` function:
- Appends parameters to a URL using the appropriate separator (? or &)
- URL-encodes the result while preserving essential URL structure characters (:/?=&)
- Works with both absolute and relative URLs

### Checking Payment Logs

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

ca = CryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)

# Get logs for this callback URL
logs = ca.get_logs()

# Process the logs
if logs.get('status') == 'success':
    callbacks = logs.get('callbacks', [])
    print(f"Found {len(callbacks)} callback records")
    
    for callback in callbacks:
        print(f"Transaction: {callback.get('txid_in')}")
        print(f"Amount: {callback.get('value')} {coin}")
        print(f"Confirmations: {callback.get('confirmations')}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    ca = AsyncCryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)
    
    # Get logs for this callback URL
    logs = await ca.get_logs()
    
    # Process the logs
    if logs.get('status') == 'success':
        callbacks = logs.get('callbacks', [])
        print(f"Found {len(callbacks)} callback records")
        
        for callback in callbacks:
            print(f"Transaction: {callback.get('txid_in')}")
            print(f"Amount: {callback.get('value')} {coin}")
            print(f"Confirmations: {callback.get('confirmations')}")

# Run the async function
asyncio.run(main())
```

The `get_logs()` method returns a dictionary containing:
- `status`: The status of the request ('success' or 'error')
- `callbacks`: An array of callback records, each containing transaction details
- Additional information about the callback history

### Generating a QR Code

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

ca = CryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)

# First, generate the address
ca.get_address()

# Then generate a QR code with an optional amount and custom size
value = '0.001'  # Optional amount to pay
size = 300  # Size in pixels (default is 300)
qr_result = ca.get_qrcode(value, size)

# The QR code is provided as a base64 encoded image
qr_code_base64 = qr_result.get('qr_code')
print(f"QR Code (base64): {qr_code_base64}")

# The payment URI can be used directly in wallet apps
payment_uri = qr_result.get('payment_uri')
print(f"Payment URI: {payment_uri}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    ca = AsyncCryptAPIHelper(coin, my_address, callback_url, params, cryptapi_params)
    
    # First, generate the address
    await ca.get_address()
    
    # Then generate a QR code with an optional amount and custom size
    value = '0.001'  # Optional amount to pay
    size = 300  # Size in pixels (default is 300)
    qr_result = await ca.get_qrcode(value, size)
    
    # The QR code is provided as a base64 encoded image
    qr_code_base64 = qr_result.get('qr_code')
    print(f"QR Code (base64): {qr_code_base64}")
    
    # The payment URI can be used directly in wallet apps
    payment_uri = qr_result.get('payment_uri')
    print(f"Payment URI: {payment_uri}")

# Run the async function
asyncio.run(main())
```

**Important**: You must first call `get_address()` before generating a QR code, as the QR code is for the payment address.

The `get_qrcode()` method returns a dictionary containing:
- `qr_code`: A base64 encoded image of the QR code
- `payment_uri`: The cryptocurrency payment URI encoded in the QR code (can be used in wallet apps)

### Estimating Transaction Fees

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

# This is a static method, so you can call it directly without initializing
fees = CryptAPIHelper.get_estimate('btc', addresses=1, priority='default')

print(f"Estimated fee: {fees.get('estimated_cost')} BTC")
print(f"Estimated fee in USD: ${fees.get('estimated_cost_usd')}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    # This is a static method, so you can call it directly without initializing
    fees = await AsyncCryptAPIHelper.get_estimate('btc', addresses=1, priority='default')
    
    print(f"Estimated fee: {fees.get('estimated_cost')} BTC")
    print(f"Estimated fee in USD: ${fees.get('estimated_cost_usd')}")

# Run the async function
asyncio.run(main())
```

Parameters:
- `coin`: The cryptocurrency to check (e.g., 'btc', 'eth', 'bep20_usdt')
- `addresses`: The number of addresses to forward funds to (default: 1)
- `priority`: Transaction priority - 'default', 'fast', or 'fastest' (default: 'default')

The `get_estimate()` method returns a dictionary containing:
- `estimated_cost`: Estimated transaction fee in the cryptocurrency
- `estimated_cost_usd`: Estimated transaction fee in USD

### Converting Between Cryptocurrencies and Fiat

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

ca = CryptAPIHelper('btc', my_address, callback_url, params, cryptapi_params)

# Convert 100 EUR to BTC
conversion = ca.get_conversion('eur', 100)

print(f"100 EUR = {conversion.get('value_coin')} BTC")
print(f"Exchange rate: 1 EUR = {conversion.get('exchange_rate')} BTC")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    ca = AsyncCryptAPIHelper('btc', my_address, callback_url, params, cryptapi_params)
    
    # Convert 100 EUR to BTC
    conversion = await ca.get_conversion('eur', 100)
    
    print(f"100 EUR = {conversion.get('value_coin')} BTC")
    print(f"Exchange rate: 1 EUR = {conversion.get('exchange_rate')} BTC")

# Run the async function
asyncio.run(main())
```

Parameters:
- `from_coin`: Currency to convert from, FIAT (e.g., 'usd', 'eur') or crypto
- `value`: Amount to convert

The `get_conversion()` method returns a dictionary containing:
- `value_coin`: The converted amount in the target cryptocurrency
- `exchange_rate`: The exchange rate between the two currencies

### Getting Information About Supported Coins

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

# Get info about a specific coin
btc_info = CryptAPIHelper.get_info('btc')
print(f"BTC Info: {btc_info}")

# Get info about all coins (no parameter)
all_coins_info = CryptAPIHelper.get_info()
print(f"Total coins with info: {len(all_coins_info)}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    # Get info about a specific coin
    btc_info = await AsyncCryptAPIHelper.get_info('btc')
    print(f"BTC Info: {btc_info}")
    
    # Get info about all coins (no parameter)
    all_coins_info = await AsyncCryptAPIHelper.get_info()
    print(f"Total coins with info: {len(all_coins_info)}")

# Run the async function
asyncio.run(main())
```

Parameters:
- `coin`: (Optional) Specific coin to get info for. If omitted, returns info for all coins.

The `get_info()` method returns a dictionary containing detailed information about the requested coin(s).

### Getting a List of Supported Coins

#### Synchronous API

```python
from cryptapi import CryptAPIHelper

# Get a dictionary of all supported coins
supported_coins = CryptAPIHelper.get_supported_coins()

# Print the number of supported coins
print(f"Number of supported coins: {len(supported_coins)}")

# Print the list of supported coins
for ticker, name in supported_coins.items():
    print(f"{ticker}: {name}")
```

#### Asynchronous API

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper

async def main():
    # Get a dictionary of all supported coins
    supported_coins = await AsyncCryptAPIHelper.get_supported_coins()
    
    # Print the number of supported coins
    print(f"Number of supported coins: {len(supported_coins)}")
    
    # Print the list of supported coins
    for ticker, name in supported_coins.items():
        print(f"{ticker}: {name}")

# Run the async function
asyncio.run(main())
```

The `get_supported_coins()` method returns a dictionary with:
- Keys: Cryptocurrency tickers (e.g., 'btc', 'eth', 'bep20_usdt')
- Values: Full names of the cryptocurrencies

## Error Handling

Both APIs raise a `CryptAPIException` when the CryptAPI service returns an error. You should handle these exceptions in your code:

```python
from cryptapi import CryptAPIHelper, CryptAPIException

try:
    ca = CryptAPIHelper('btc', my_address, callback_url, params, cryptapi_params)
    address = ca.get_address()
    # Process result...
except CryptAPIException as e:
    print(f"CryptAPI error: {str(e)}")
except Exception as e:
    print(f"General error: {str(e)}")
```

For async code:

```python
import asyncio
from cryptapi import AsyncCryptAPIHelper, CryptAPIException

async def main():
    try:
        ca = AsyncCryptAPIHelper('btc', my_address, callback_url, params, cryptapi_params)
        address = await ca.get_address()
        # Process result...
    except CryptAPIException as e:
        print(f"CryptAPI error: {str(e)}")
    except Exception as e:
        print(f"General error: {str(e)}")

asyncio.run(main())
```

## SSL Configuration (Async API)

The AsyncCryptAPIHelper automatically configures a secure SSL context using the certifi package:

```python
import ssl
import certifi

# This happens automatically when you create an AsyncCryptAPIHelper instance
ssl_context = ssl.create_default_context(cafile=certifi.where())
```

## Help

Need help or support?  
Contact us @ https://cryptapi.io/contacts/

## Changelog

#### 1.0.0
* Initial Release

#### 1.0.1 - 1.0.6
* Various minor fixes and improvements
* Improved error handling

#### 1.1.0
* Added asynchronous API support via AsyncCryptAPIHelper
* Added aiohttp and certifi dependencies
* Added SSL context for secure connections
* Comprehensive documentation updates
