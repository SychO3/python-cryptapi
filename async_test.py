#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Async CryptAPI Test File - Testing Async API functionality
"""

import asyncio
import json
from time import time
from cryptapi import AsyncCryptAPIHelper
from cryptapi.AsyncCryptAPI import CryptAPIException


def print_section(title):
    """Print a section title with separator lines"""
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def format_dict(d, indent=2):
    """Format dictionary output for better readability"""
    if not isinstance(d, dict):
        return str(d)
    try:
        return json.dumps(d, indent=indent, ensure_ascii=False)
    except:
        return str(d)


async def run_tests():
    """
    Run all async tests
    """
    start_time = time()

    print_section("Initialization")
    print("Creating AsyncCryptAPIHelper instance...")
    # Initialize AsyncCryptAPIHelper instance
    ca = AsyncCryptAPIHelper(
        "bep20_usdt",
        "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d",
        "https://webhook.site/13308bd5-d20b-4d19-8597-bd9be7db36fe",
        {"order_id": "1345e13232"},
        {"convert": 1, "multi_token": 1},
    )
    print("Instance created, starting method tests...")

    """
    Get payment address
    """
    print_section("Test: get_address()")
    try:
        address_data = await ca.get_address()
        print(f"Payment address created successfully!")
        print(f"Address: {address_data['address_in']}")
        print(f"Complete information:\n{format_dict(address_data)}")
    except CryptAPIException as e:
        print(f"Error getting address: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    """
    Get coin information
    """
    print_section("Test: get_info('btc')")
    try:
        info = await AsyncCryptAPIHelper.get_info("btc")
        if isinstance(info, dict) and "btc" in info:
            print(f"BTC information retrieved successfully!")
            btc_info = info["btc"]
            print(f"Name: {btc_info.get('coin', 'Unknown')}")
            print(f"Symbol: {btc_info.get('ticker', 'Unknown')}")
            print(
                f"Minimum transaction amount: {btc_info.get('minimum_transaction_coin', 'Unknown')} BTC"
            )
            print(
                f"Network fee estimate: {btc_info.get('network_fee_estimation', 'Unknown')} BTC"
            )
        else:
            print(f"BTC information retrieved (incomplete):\n{format_dict(info)}")
    except CryptAPIException as e:
        print(f"Error getting coin information: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    """
    Get all supported coins
    """
    print_section("Test: get_supported_coins()")
    try:
        coins = await AsyncCryptAPIHelper.get_supported_coins()
        print(f"Supported coins retrieved successfully!")
        print(f"Total supported coins: {len(coins)}")
        print("First 5 supported coins:")
        for i, (ticker, name) in enumerate(list(coins.items())[:5], 1):
            print(f"  {i}. {ticker}: {name}")
    except CryptAPIException as e:
        print(f"Error getting supported coins: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    """
    Get logs
    """
    print_section("Test: get_logs()")
    try:
        logs = await ca.get_logs()
        print(f"✅ Logs retrieved successfully!")
        print(f"Log information:\n{format_dict(logs)}")
    except CryptAPIException as e:
        print(f"⚠️ Error getting logs: {str(e)}")
        print(
            "  Note: This is normal in test environments if no real transactions exist for this callback URL."
        )
        print(
            "  The synchronous and asynchronous APIs use the same endpoint - both will return data if it exists."
        )
        print(
            "  You may need to run this with a callback URL that has associated transaction data."
        )
    except Exception as e:
        print(f"❌ Unknown error occurred: {str(e)}")

    """
    Get QR code
    """
    print_section("Test: get_qrcode()")
    try:
        qr_code = await ca.get_qrcode()
        if "qr_code" in qr_code:
            print(f"QR code retrieved successfully!")
            print(f"QR code data length: {len(qr_code['qr_code'])} characters")
            print(f"Payment URI: {qr_code.get('payment_uri', 'Not provided')}")
            print(
                "Note: QR code data is too long to display, in a real application it would be used to generate an image"
            )
        else:
            print(
                f"QR code information retrieved (incomplete):\n{format_dict(qr_code)}"
            )
    except CryptAPIException as e:
        print(f"Error getting QR code: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    """
    Get currency conversion
    """
    print_section("Test: get_conversion('eur', 100)")
    try:
        conversion = await ca.get_conversion("eur", 100)
        print(f"Currency conversion successful!")
        print(f"100 EUR = {conversion.get('value_coin', 'Unknown')} {ca.coin.upper()}")
        print(
            f"Exchange rate: 1 EUR = {conversion.get('exchange_rate', 'Unknown')} {ca.coin.upper()}"
        )
    except CryptAPIException as e:
        print(f"Error getting currency conversion: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    """
    Get fee estimate
    """
    print_section("Test: get_estimate('ltc')")
    try:
        estimate = await AsyncCryptAPIHelper.get_estimate("ltc")
        print(f"Fee estimation successful!")
        print("LTC transaction fee estimates:")
        print(
            f"Default priority: {estimate.get('estimated_cost_currency', 'Unknown')} LTC"
        )
        if "estimated_cost_currency_priority" in estimate:
            print(
                f"High priority: {estimate.get('estimated_cost_currency_priority')} LTC"
            )
        else:
            print("High priority: Not provided")
        print(f"USD estimate: ${estimate.get('estimated_cost_usd', 'Unknown')}")
    except CryptAPIException as e:
        print(f"Error getting fee estimation: {str(e)}")
    except Exception as e:
        print(f"Unknown error occurred: {str(e)}")

    # Print total duration
    end_time = time()
    duration = end_time - start_time
    print_section(f"Tests Complete")
    print(f"Total duration: {duration:.2f} seconds")


if __name__ == "__main__":
    # Run all async tests
    print("\nStarting Async CryptAPI Tests...")

    # Use recommended async execution method
    asyncio.run(run_tests())

    print("\nAsync Tests Completed!")
