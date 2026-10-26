import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from datetime import datetime
from scraper import (
    scrape_top_10,
    get_latest_csv_path,
    get_history_csv_path,
    LATEST_CSV_PATH,
    CSV_HISTORY_PATH
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "crypto_tracker_secret_key_college_project")

def format_price(val):
    """Formats price with commas and dynamic decimal places depending on magnitude."""
    try:
        val_float = float(val)
        if val_float >= 100:
            return f"${val_float:,.2f}"
        elif val_float >= 1:
            return f"${val_float:,.2f}"
        elif val_float > 0:
            # For lower-priced coins, show more decimals
            return f"${val_float:,.4f}"
        return "$0.00"
    except (ValueError, TypeError):
        return "$0.00"

def format_market_cap(val):
    """Formats market cap to standard currency format."""
    try:
        val_int = int(float(val))
        return f"${val_int:,}"
    except (ValueError, TypeError):
        return "$0"

def format_timestamp_display(timestamp_str):
    """
    Converts timestamp from 'YYYY-MM-DD HH:MM:SS' to 'DD Mon YYYY, HH:MM AM/PM' format.
    Example: '2026-06-13 15:35:42' -> '13 Jun 2026, 03:35 PM'
    """
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except (ValueError, TypeError):
        return "N/A"

@app.route("/")
def index():
    # Return empty list and startup state on main load
    return render_template(
        "index.html",
        coins=[],
        last_updated="N/A",
        min_price="",
        sort_gainers=False
    )

@app.route("/scrape")
def scrape():
    try:
        # Perform live cryptocurrency data retrieval
        df = scrape_top_10()
        
        # Format values for AJAX JSON payload
        coins_list = []
        latest_timestamp = df["Timestamp"].max()
        formatted_timestamp = format_timestamp_display(latest_timestamp)
        
        for _, row in df.iterrows():
            coins_list.append({
                "Rank": int(row["Rank"]),
                "Name": str(row["Name"]),
                "Symbol": str(row["Symbol"]),
                "Price": float(row["Price"]),
                "FormattedPrice": format_price(row["Price"]),
                "Change": float(row["24h_Change"]),
                "MarketCap": int(float(row["Market_Cap"])),
                "FormattedMarketCap": format_market_cap(row["Market_Cap"]),
                "Timestamp": latest_timestamp
            })
            
        return jsonify({
            "success": True,
            "coins": coins_list,
            "last_updated": latest_timestamp,
            "last_updated_formatted": formatted_timestamp
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/download")
def download():
    latest_path = get_latest_csv_path()

    # If the file does not exist or is empty in the current runtime, attempt to generate it
    if not os.path.exists(latest_path) or os.path.getsize(latest_path) == 0:
        try:
            scrape_top_10()
            latest_path = get_latest_csv_path()
        except Exception:
            # Fall back to root latest_crypto.csv if available
            root_fallback = os.path.join(BASE_DIR, "latest_crypto.csv")
            if os.path.exists(root_fallback) and os.path.getsize(root_fallback) > 0:
                latest_path = root_fallback
            else:
                flash("No data available to download. Please click 'Scrape Data' first.", "warning")
                return redirect(url_for("index"))

    try:
        return send_file(
            latest_path,
            mimetype="text/csv",
            as_attachment=True,
            download_name="crypto_prices.csv"
        )
    except Exception as e:
        flash(f"Failed to download CSV: {str(e)}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
