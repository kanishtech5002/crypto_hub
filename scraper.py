import os
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CSV_HISTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto_history.csv")
LATEST_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "latest_crypto.csv")

# Legacy path for backward compatibility
CSV_PATH = CSV_HISTORY_PATH

# Global Headless Configuration (False by default to allow visible browser windows)
HEADLESS_MODE = False

def scrape_top_10():
    """
    Scrapes the top 10 cryptocurrencies from CoinMarketCap using Selenium.
    Cleans and processes the data using Pandas, appends it to crypto_prices.csv
    with a timestamp, and returns the current top 10 DataFrame.
    """
    options = webdriver.ChromeOptions()
    if HEADLESS_MODE:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Configure user-specific Chrome binary if available (standard on the test environment)
    user_chrome = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')
    if os.path.exists(user_chrome):
        options.binary_location = user_chrome

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Selenium WebDriver...")
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://coinmarketcap.com/"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Navigating to {url}...")
        driver.get(url)
        
        # Explicit wait for the main cryptocurrency table to load
        wait = WebDriverWait(driver, 25)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table")))
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Table loaded. Processing rows...")
        rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")
        
        scraped_data = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for idx, row in enumerate(rows):
            if len(scraped_data) >= 10:
                break
                
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 8:
                continue
                
            rank_text = cells[1].text.strip()
            if not rank_text.isdigit():
                # Skip non-cryptocurrency rows (e.g. index/banner headers)
                continue
                
            rank = int(rank_text)
            
            # Extract name and symbol
            # Typically text structure: "Bitcoin\nBTC\nBuy" or "Ethereum\nETH"
            name_cell_text = cells[2].text.strip()
            name_parts = name_cell_text.split('\n')
            if len(name_parts) >= 2:
                name = name_parts[0].strip()
                symbol = name_parts[1].strip()
            else:
                name = name_cell_text
                symbol = ""
                
            # Extract price and convert to float
            price_text = cells[3].text.strip()
            price_clean = price_text.replace('$', '').replace(',', '').strip()
            try:
                price = float(price_clean)
            except ValueError:
                price = 0.0
                
            # Extract 24h Change and handle positive/negative signs
            change_cell = cells[5]
            change_text = change_cell.text.strip()
            change_clean = change_text.replace('%', '').replace(',', '').strip()
            try:
                change_val = float(change_clean)
            except ValueError:
                change_val = 0.0
                
            # Determine direction (positive/negative) by checking innerHTML for caret-down icon
            inner_html = change_cell.get_attribute("innerHTML")
            if "icon-Caret-down" in inner_html or "caret-down" in inner_html:
                change_val = -abs(change_val)
            elif "icon-Caret-up" in inner_html or "caret-up" in inner_html:
                change_val = abs(change_val)
                
            # Extract Market Cap and convert to int/float
            mcap_text = cells[7].text.strip()
            mcap_clean = mcap_text.replace('$', '').replace(',', '').strip()
            try:
                market_cap = float(mcap_clean)
            except ValueError:
                market_cap = 0.0
                
            scraped_data.append({
                "Timestamp": timestamp,
                "Rank": rank,
                "Name": name,
                "Symbol": symbol,
                "Price": price,
                "24h_Change": change_val,
                "Market_Cap": market_cap
            })
            
            print(f"  Scraped: Rank {rank} - {name} ({symbol}) | Price: {price} | 24h Change: {change_val}% | Market Cap: {market_cap}")
            
        if not scraped_data:
            raise Exception("No cryptocurrency data could be scraped from the page.")
            
        df = pd.DataFrame(scraped_data)
        
        # Save to CSV (Historical Logging in crypto_history.csv)
        # If the file does not exist, write it with headers. If it does exist, append without headers.
        if not os.path.exists(CSV_HISTORY_PATH):
            df.to_csv(CSV_HISTORY_PATH, index=False)
            print(f"Created new historical CSV file: {CSV_HISTORY_PATH}")
        else:
            df.to_csv(CSV_HISTORY_PATH, mode='a', header=False, index=False)
            print(f"Appended scraped data to historical CSV: {CSV_HISTORY_PATH}")
        
        # Save only the latest Top 10 to latest_crypto.csv (overwrite mode)
        df.to_csv(LATEST_CSV_PATH, index=False)
        print(f"Saved latest Top 10 records to: {LATEST_CSV_PATH}")
            
        return df
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    # Test execution
    print("Running scraper test...")
    try:
        df_result = scrape_top_10()
        print("\nScraping successful! Results:")
        print(df_result)
    except Exception as ex:
        print(f"Failed: {ex}")
