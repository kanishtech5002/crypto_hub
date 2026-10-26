import os
import tempfile
from datetime import datetime
import pandas as pd
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_data_dir():
    """
    Returns a writable directory for saving CSV exports.
    On Vercel and serverless platforms where root is read-only, uses the temporary directory.
    """
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return tempfile.gettempdir()
    
    local_dir = os.path.dirname(os.path.abspath(__file__))
    if os.access(local_dir, os.W_OK):
        return local_dir
        
    return tempfile.gettempdir()

def get_latest_csv_path():
    """Returns the absolute path to the latest CSV file."""
    return os.path.join(get_data_dir(), "latest_crypto.csv")

def get_history_csv_path():
    """Returns the absolute path to the historical CSV file."""
    return os.path.join(get_data_dir(), "crypto_history.csv")

# Export paths for compatibility
LATEST_CSV_PATH = get_latest_csv_path()
CSV_HISTORY_PATH = get_history_csv_path()
CSV_PATH = CSV_HISTORY_PATH


def _save_output(df):
    """
    Saves dataframe to both latest and historical CSV files.
    Safely ignores write errors in strictly read-only serverless environments.
    """
    try:
        data_dir = get_data_dir()
        latest_path = os.path.join(data_dir, "latest_crypto.csv")
        history_path = os.path.join(data_dir, "crypto_history.csv")

        if not os.path.exists(history_path):
            df.to_csv(history_path, index=False)
            print(f"Created new historical CSV: {history_path}")
        else:
            df.to_csv(history_path, mode='a', header=False, index=False)
            print(f"Appended records to historical CSV: {history_path}")

        df.to_csv(latest_path, index=False)
        print(f"Saved latest Top 10 records to: {latest_path}")
    except Exception as e:
        print(f"Warning: Unable to save CSV to disk: {e}")


def _fetch_from_coinmarketcap(api_key):
    """
    Fetches the top 10 cryptocurrencies from CoinMarketCap Pro API.
    Endpoint: https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "X-CMC_PRO_API_KEY": api_key.strip(),
        "Accept": "application/json",
        "User-Agent": "CryptoHub/1.0"
    }
    params = {
        "start": 1,
        "limit": 10,
        "convert": "USD"
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching top 10 coins from CoinMarketCap API...")
    response = requests.get(url, headers=headers, params=params, timeout=12)
    
    if response.status_code != 200:
        try:
            err_data = response.json()
            err_msg = err_data.get("status", {}).get("error_message") or response.text
        except Exception:
            err_msg = response.text
        raise ValueError(f"CoinMarketCap API HTTP {response.status_code}: {err_msg}")

    payload = response.json()
    coins = payload.get("data", [])
    if not coins or not isinstance(coins, list):
        raise ValueError("Invalid or empty data received from CoinMarketCap API.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for idx, coin in enumerate(coins[:10], start=1):
        quote_usd = coin.get("quote", {}).get("USD", {})
        price = float(quote_usd.get("price") or 0.0)
        change_24h = float(quote_usd.get("percent_change_24h") or 0.0)
        market_cap = float(quote_usd.get("market_cap") or 0.0)

        rows.append({
            "Timestamp": timestamp,
            "Rank": int(coin.get("cmc_rank", idx)),
            "Name": str(coin.get("name", "")),
            "Symbol": str(coin.get("symbol", "")).upper(),
            "Price": price,
            "24h_Change": change_24h,
            "Market_Cap": market_cap
        })

    df = pd.DataFrame(rows)
    _save_output(df)
    return df


def _fetch_from_coinpaprika():
    """
    Reliable zero-authentication fallback using CoinPaprika API.
    Provides live price, 24h change, and market cap for top cryptocurrencies.
    """
    url = "https://api.coinpaprika.com/v1/tickers"
    headers = {
        "User-Agent": "CryptoHub/1.0",
        "Accept": "application/json"
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching top 10 coins from CoinPaprika API...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    tickers = response.json()
    if not isinstance(tickers, list) or len(tickers) == 0:
        raise ValueError("Invalid response format from CoinPaprika API.")

    ranked = sorted([t for t in tickers if t.get("rank")], key=lambda x: x["rank"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []

    for idx, coin in enumerate(ranked[:10], start=1):
        usd_quote = coin.get("quotes", {}).get("USD", {})
        price = float(usd_quote.get("price") or 0.0)
        change_24h = float(usd_quote.get("percent_change_24h") or 0.0)
        market_cap = float(usd_quote.get("market_cap") or 0.0)

        rows.append({
            "Timestamp": timestamp,
            "Rank": int(coin.get("rank", idx)),
            "Name": str(coin.get("name", "")),
            "Symbol": str(coin.get("symbol", "")).upper(),
            "Price": price,
            "24h_Change": change_24h,
            "Market_Cap": market_cap
        })

    df = pd.DataFrame(rows)
    _save_output(df)
    return df


def _fetch_from_coingecko():
    """
    Public API fallback using CoinGecko markets endpoint.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h"
    }
    headers = {
        "User-Agent": "CryptoHub/1.0",
        "Accept": "application/json"
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching top 10 coins from CoinGecko API...")
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) == 0:
        raise ValueError("Invalid response format from CoinGecko API.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for idx, coin in enumerate(payload[:10], start=1):
        rows.append({
            "Timestamp": timestamp,
            "Rank": idx,
            "Name": str(coin.get("name", "")),
            "Symbol": str(coin.get("symbol", "")).upper(),
            "Price": float(coin.get("current_price") or 0.0),
            "24h_Change": float(coin.get("price_change_percentage_24h") or 0.0),
            "Market_Cap": float(coin.get("market_cap") or 0.0)
        })

    df = pd.DataFrame(rows)
    _save_output(df)
    return df


def scrape_top_10():
    """
    Fetches real-time market data for the top 10 cryptocurrencies.
    
    Order of operations:
    1. If COINMARKETCAP_API_KEY (or CMC_API_KEY) is configured in environment variables,
       fetch directly from CoinMarketCap Pro API.
    2. If no CoinMarketCap key is provided or if CMC returns an error/rate limit,
       fall back to CoinPaprika API for reliable live market data.
    3. If CoinPaprika fails, fall back to CoinGecko API.
    """
    cmc_key = os.environ.get("COINMARKETCAP_API_KEY") or os.environ.get("CMC_API_KEY")
    errors = []

    if cmc_key and cmc_key.strip():
        try:
            return _fetch_from_coinmarketcap(cmc_key)
        except Exception as e:
            msg = f"CoinMarketCap API error: {e}"
            print(msg)
            errors.append(msg)
    else:
        print("Note: COINMARKETCAP_API_KEY not configured. Using live cryptocurrency data API fallback.")

    # Try CoinPaprika
    try:
        return _fetch_from_coinpaprika()
    except Exception as e:
        msg = f"CoinPaprika fallback error: {e}"
        print(msg)
        errors.append(msg)

    # Try CoinGecko
    try:
        return _fetch_from_coingecko()
    except Exception as e:
        msg = f"CoinGecko fallback error: {e}"
        print(msg)
        errors.append(msg)

    # If all sources failed, raise an informative exception
    raise RuntimeError(
        "Failed to retrieve live cryptocurrency data from all providers. "
        + " | ".join(errors)
    )


if __name__ == "__main__":
    print("Testing cryptocurrency data retrieval...")
    try:
        df_result = scrape_top_10()
        print("\nSuccess! Retrieved top 10 cryptocurrencies:")
        print(df_result[["Rank", "Name", "Symbol", "Price", "24h_Change", "Market_Cap"]])
    except Exception as err:
        print(f"Failed: {err}")
