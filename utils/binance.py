import hashlib
import hmac
import time
import httpx
from typing import Optional, Dict, Any
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET

BASE_URL = "https://api.binance.com"


def create_signature(query_string: str) -> str:
    return hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


async def get_account_info() -> Optional[Dict[str, Any]]:
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = create_signature(query_string)

    url = f"{BASE_URL}/api/v3/account"
    params = {"signature": signature, "timestamp": timestamp}

    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None


async def withdraw_usdt(address: str, amount: float, network: str = "TRX") -> Dict[str, Any]:
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        return {"success": False, "error": "Binance API not configured"}

    timestamp = int(time.time() * 1000)
    coin = "USDT"

    if network.upper() == "TRX":
        network = "TRC20USDT"

    query_string = f"asset={coin}&address={address}&amount={amount}&network={network}&timestamp={timestamp}"
    signature = create_signature(query_string)

    url = f"{BASE_URL}/wapi/v3/withdraw.html"
    params = {
        "asset": coin,
        "address": address,
        "amount": amount,
        "network": network,
        "signature": signature,
        "timestamp": timestamp
    }
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, params=params, timeout=30)
            data = response.json()

            if response.status_code == 200 and "success" in data and data["success"]:
                return {
                    "success": True,
                    "tx_id": data.get("id", ""),
                    "amount": amount,
                    "address": address
                }
            else:
                return {
                    "success": False,
                    "error": data.get("msg", "Unknown error")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


async def get_deposit_address(asset: str = "USDT", network: str = "TRC20") -> Optional[str]:
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        return None

    timestamp = int(time.time() * 1000)

    if network.upper() == "TRX":
        network = "TRC20"

    query_string = f"coin={asset}&network={network}&timestamp={timestamp}"
    signature = create_signature(query_string)

    url = f"{BASE_URL}/sapi/v1/capital/deposit/address"
    params = {
        "coin": asset,
        "network": network,
        "signature": signature,
        "timestamp": timestamp
    }
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("address")
            return None
        except Exception:
            return None
