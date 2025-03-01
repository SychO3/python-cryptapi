from cryptapi import CryptAPIHelper

ca = CryptAPIHelper(
    "bep20_usdt",
    "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d",
    "https://webhook.site/13308bd5-d20b-4d19-8597-bd9be7db36fe",
    {"order_id": "1345e13232"},
    {"convert": 1, "multi_token": 1},
)

print("====== Testing CryptAPI Synchronous Methods ======")

try:
    """
    Get CA Address
    """
    print("\n[Test] get_address:")
    address = ca.get_address()["address_in"]
    print(f"Obtained address: {address}")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get coin information
    """
    print("\n[Test] get_info:")
    info = CryptAPIHelper.get_info("btc")
    print(f"Obtained information: Success")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get all supported coins
    """
    print("\n[Test] get_supported_coins:")
    coins = CryptAPIHelper.get_supported_coins()
    print(f"Number of supported coins: {len(coins)}")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get Logs
    """
    print("\n[Test] get_logs:")

    # Get logs
    logs = ca.get_logs()
    print(f"Retrieved logs: {logs.get('status', 'unknown')}")
    print(f"Number of callback records: {len(logs.get('callbacks', []))}")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get QR Code
    """
    print("\n[Test] get_qrcode:")
    qr = ca.get_qrcode()
    print(f"Retrieved QR code: {'success' if 'qr_code' in qr else 'failed'}")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get Conversion
    """
    print("\n[Test] get_conversion:")
    conv = ca.get_conversion("eur", 100)
    print(f"Retrieved exchange rate: {conv.get('exchange_rate', 'unknown')}")
except Exception as e:
    print(f"Error: {str(e)}")

try:
    """
    Get Estimate
    """
    print("\n[Test] get_estimate:")
    est = CryptAPIHelper.get_estimate("btc", "eth", 0.01)
    print(f"Retrieved estimate: {est}")
except Exception as e:
    print(f"Error: {str(e)}")
