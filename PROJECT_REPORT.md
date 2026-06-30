# CryptoHub - Real-Time Cryptocurrency Price Tracker & Market Analytics
## Comprehensive Project Report

---

## 1. Introduction

**CryptoHub** is a real-time cryptocurrency price tracking and market analytics application designed to monitor the top 10 cryptocurrencies from CoinMarketCap. The application provides a user-friendly web interface for viewing live cryptocurrency prices, market capitalization, 24-hour price changes, and historical price data logging. Users can scrape live data from CoinMarketCap, apply filters based on price thresholds, sort by gainers, and download historical data in CSV format for further analysis.

**Project Type:** Web Application (Flask-based)  
**Purpose:** To provide real-time cryptocurrency market data with filtering, analysis, and data export capabilities  
**Target Users:** Cryptocurrency investors, traders, and market analysts

---

## 2. Pre-Requisites

Before setting up and running the CryptoHub application, ensure the following prerequisites are met:

### System Requirements
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python Version:** Python 3.8 or higher
- **RAM:** Minimum 4GB
- **Disk Space:** At least 500MB available

### Software Requirements
- **Python 3.8+** installed and configured in system PATH
- **pip** (Python package manager)
- **Google Chrome or Chromium browser** installed (required for Selenium WebDriver)
- **ChromeDriver** compatible with your Chrome version (automatically managed by Selenium if using modern versions)
- **Code Editor:** Visual Studio Code, PyCharm, or any text editor

### Network Requirements
- Active internet connection to access CoinMarketCap website
- No firewall/proxy blocking access to https://coinmarketcap.com/
- Permission to scrape data from CoinMarketCap (for educational purposes)

### Knowledge Prerequisites
- Basic understanding of Python programming
- Familiarity with Flask web framework
- Understanding of web scraping concepts
- CSV file format knowledge

---

## 3. Technologies Used

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 2.3.3+ | Web framework for building web application |
| **Pandas** | 2.0.0+ | Data manipulation, cleaning, and CSV operations |
| **Selenium** | 4.15.2+ | Web scraping and browser automation |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | - | Structure and markup |
| **CSS3** | - | Styling and animations |
| **Bootstrap 5** | 5.3.0 | Responsive UI components |
| **JavaScript (Vanilla)** | ES6+ | Client-side interactivity |
| **Bootstrap Icons** | 1.10.5 | Icon library |

### Data Storage
- **CSV Files** - Local file storage for historical and latest cryptocurrency data

### Web Browser
- **Google Chrome** - For Selenium-based web scraping

### Development Tools
- **Visual Studio Code** - Code editor
- **Git** - Version control (optional)
- **Chrome DevTools** - Debugging (optional)

---

## 4. Install Required Libraries

### Step 1: Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
pip list
```

Expected output should show:
- Flask >= 2.3.3
- pandas >= 2.0.0
- selenium >= 4.15.2

### Step 4: ChromeDriver Setup (If Needed)
For Selenium to work, you need ChromeDriver:
1. Check your Chrome version: **Chrome Menu → Help → About Google Chrome**
2. Download matching ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
3. Place it in your project directory or add to PATH

**Alternative:** Use `webdriver-manager` package for automatic driver management:
```bash
pip install webdriver-manager
```

---

## 5. Python Libraries Used

### Core Libraries

#### **Flask**
- **Purpose:** Web framework for building the web application
- **Key Functions Used:**
  - `Flask()` - Create application instance
  - `@app.route()` - Define URL routes
  - `render_template()` - Render HTML templates with variables
  - `request` - Handle HTTP requests
  - `jsonify()` - Convert Python objects to JSON responses
  - `send_file()` - Handle file downloads
  - `redirect()`, `url_for()` - URL handling and redirection
  - `flash()` - Display user notifications

#### **Pandas**
- **Purpose:** Data manipulation, analysis, and CSV file operations
- **Key Functions Used:**
  - `pd.DataFrame()` - Create data frames from dictionaries
  - `.to_csv()` - Write data to CSV files
  - `.read_csv()` - Read CSV files
  - `.iterrows()` - Iterate through DataFrame rows
  - `.max()` - Get maximum values
  - Data cleaning and transformation

#### **Selenium**
- **Purpose:** Automated web scraping and browser automation
- **Key Components Used:**
  - `webdriver.Chrome()` - Initialize Chrome WebDriver
  - `ChromeOptions()` - Configure browser options
  - `driver.get()` - Navigate to URLs
  - `WebDriverWait()` - Explicit waits for elements
  - `expected_conditions.EC` - Wait conditions
  - `find_elements()`, `find_element()` - Locate DOM elements
  - `By.CSS_SELECTOR`, `By.TAG_NAME` - Element location strategies
  - `.text` - Extract text from elements
  - `.get_attribute()` - Get HTML attributes

### Built-in Libraries

#### **os**
- File path handling and environment variables
- Functions: `os.path.join()`, `os.path.exists()`, `os.path.dirname()`

#### **datetime**
- Timestamp generation and formatting
- Functions: `datetime.now()`, `datetime.strptime()`, `strftime()`

#### **traceback**
- Error tracking and debugging
- Function: `traceback.print_exc()`

---

## 6. Coding (Step by Step)

### Project Structure
```
crypto currency tracker/
│
├── app.py                    # Main Flask application
├── scraper.py               # Web scraping module
├── requirements.txt         # Python dependencies
├── crypto_history.csv       # Historical data archive
├── latest_crypto.csv        # Latest top 10 data
│
├── templates/
│   └── index.html          # HTML template
│
└── static/
    └── style.css           # CSS styling
```

### Step 1: Web Scraping Module (scraper.py)

**Purpose:** Extract real-time cryptocurrency data from CoinMarketCap

**Key Functions:**

1. **`scrape_top_10()` - Main Scraping Function**
   - Initializes Chrome WebDriver with Selenium options
   - Navigates to CoinMarketCap website
   - Waits for cryptocurrency table to load (explicit wait: 25 seconds)
   - Extracts top 10 cryptocurrency data:
     - Rank, Name, Symbol, Price
     - 24-hour Price Change, Market Cap
   - Adds timestamp to all records
   - Handles data type conversions (strings → floats/integers)
   - Saves data to two CSV files:
     - `crypto_history.csv` - Append mode (historical archive)
     - `latest_crypto.csv` - Overwrite mode (latest records)
   - Proper error handling and browser cleanup

**Data Extraction Logic:**
- Row filtering: Extract only top 10 records
- Price parsing: Remove `$` and `,` characters, convert to float
- Change calculation: Detect positive/negative by HTML icon analysis
- Market Cap parsing: Handle large numbers with scientific notation

**CSV Output Format:**
```
Timestamp,Rank,Name,Symbol,Price,24h_Change,Market_Cap
2026-06-13 15:35:42,1,Bitcoin,BTC,45000.50,-2.35,882000000000
```

### Step 2: Flask Application (app.py)

**Purpose:** Build web interface and API endpoints for data display and management

**Key Components:**

1. **Utility Functions**
   - `format_price(val)` - Format prices with currency symbol and decimals
   - `format_market_cap(val)` - Format large numbers with commas
   - `format_timestamp_display()` - Convert timestamps to readable format

2. **Routes and Endpoints**

   **a) Index Route (`/`)**
   - Route: `GET /`
   - Returns: HTML template with empty state
   - Purpose: Display initial dashboard

   **b) Scrape Route (`/scrape`)**
   - Route: `GET /scrape`
   - Calls: `scrape_top_10()` from scraper module
   - Returns: JSON response with:
     - Success status flag
     - Top 10 coins array with formatted data
     - Last updated timestamp (formatted & raw)
   - Handles: AJAX requests from frontend
   - Error handling: Returns error messages in JSON

   **c) Download Route (`/download`)**
   - Route: `GET /download`
   - Validates: Checks if latest_crypto.csv exists
   - Returns: CSV file as attachment for download
   - Fallback: Redirects to index if file not available

3. **Flash Messaging System**
   - Notifies users of success/warning/error messages
   - Displayed as toast notifications in UI

### Step 3: Frontend HTML Template (index.html)

**Purpose:** Provide interactive user interface for data display and interaction

**Key Sections:**

1. **Header/Dashboard**
   - Application title: "CryptoHub"
   - Tagline: Real-time tracking and analytics
   - Action buttons: Scrape Data, Download CSV

2. **Filter Panel (Left Sidebar)**
   - Minimum price input field
   - Sort by 24h Gainers checkbox toggle
   - Apply Filters button
   - Reset Filters button
   - Network status indicator
   - Last updated timestamp display

3. **Data Table Section (Main Content)**
   - Table headers: Rank, Name, Symbol, Price, 24h Change, Market Cap
   - Dynamic rows populated via JavaScript
   - Color-coded gains (green) and losses (red)
   - Responsive design for mobile/tablet

4. **Toast Notifications**
   - Position: Top-right corner
   - Types: Success, Error, Warning
   - Auto-dismiss functionality

5. **Bootstrap Integration**
   - Responsive grid system
   - Cards for sections
   - Badges for status indicators
   - Icons via Bootstrap Icons

### Step 4: Styling (style.css)

**Purpose:** Create modern, visually appealing dark-themed interface

**Key Design Elements:**

1. **Color Scheme**
   - Primary: Cyan/Blue neon colors
   - Background: Dark gradient
   - Text: Light/white colors
   - Accent: Green (gains), Red (losses)

2. **Typography**
   - Font: Google's "Outfit" family
   - Responsive sizing

3. **Visual Effects**
   - Glass-morphism background
   - Gradient text effects
   - Pulse animations
   - Smooth transitions

4. **Responsive Design**
   - Mobile-first approach
   - Breakpoints for tablet/desktop

### Step 5: Client-Side JavaScript

**Key Functions:**

1. **`triggerScrape()` - Initiate Data Scraping**
   - Sends AJAX GET request to `/scrape`
   - Shows loading spinner
   - Handles response and updates table
   - Updates timestamp and status

2. **`populateTable(coins)` - Render Cryptocurrency Table**
   - Creates table rows from coin data
   - Formats prices and percentage changes
   - Applies color coding
   - Handles empty state

3. **`applyFilters()` - Filter and Sort Data**
   - Filters by minimum price
   - Sorts by 24-hour change (gainers)
   - Re-renders table with filtered results

4. **`resetFilters()` - Clear All Filters**
   - Resets all filter inputs
   - Displays full unfiltered data

5. **Status Updates**
   - Updates last-updated timestamp
   - Changes status indicator color/animation
   - Displays success/error messages

---

## 7. Troubleshooting Table

| Issue | Symptoms | Cause | Solution |
|-------|----------|-------|----------|
| **ModuleNotFoundError: No module named 'flask'** | Application crashes on startup | Flask not installed | Run `pip install flask` |
| **ModuleNotFoundError: No module named 'selenium'** | Scraping feature crashes | Selenium not installed | Run `pip install selenium` |
| **ModuleNotFoundError: No module named 'pandas'** | CSV operations fail | Pandas not installed | Run `pip install pandas` |
| **ChromeDriver version mismatch** | WebDriver crashes when scraping | Chrome version doesn't match driver version | Download matching ChromeDriver or use webdriver-manager |
| **Connection timeout on CoinMarketCap** | Scraping hangs for 25+ seconds | Website not responding or firewall blocking | Check internet connection, disable VPN, check firewall rules |
| **SSL Certificate Error** | HTTPS connection fails | SSL/TLS verification issue | Update certifi: `pip install --upgrade certifi` |
| **CSV file already exists** | Multiple scrapes overwrite data | File handling conflict | Check permissions, ensure crypto_history.csv is not read-only |
| **No data in table after scraping** | Table remains empty | Parsing failed to extract data | Verify CoinMarketCap HTML structure hasn't changed, check CSS selectors |
| **Download CSV fails** | Download button shows error | File not found or corrupted | Run scraper first to generate latest_crypto.csv |
| **Port 5000 already in use** | Flask fails to start | Another process using port | Kill process or change port in `app.py` |
| **JavaScript AJAX request fails** | Data doesn't update in UI | Flask endpoint returning error | Check browser console for error messages, verify /scrape route |
| **Invalid JSON response** | UI shows "Error loading data" | Flask returning malformed JSON | Check scraper output, verify data types in jsonify() |
| **Table CSS not loading** | Unstyled table appears | Static CSS file not found | Verify `style.css` location in `static/` directory |
| **Timestamp format error** | Timestamps showing "N/A" | Date parsing format mismatch | Verify timestamp format matches `"%Y-%m-%d %H:%M:%S"` |
| **Filter not applying** | Buttons not responsive | JavaScript not loaded | Check browser console, verify script tags in HTML |

---

## 8. Scope of the Project

### Functional Scope

**In Scope:**
- ✅ Real-time scraping of top 10 cryptocurrencies
- ✅ Display current prices, market caps, 24-hour changes
- ✅ Filter cryptocurrencies by minimum price
- ✅ Sort by 24-hour gainers
- ✅ Historical data logging to CSV
- ✅ Download latest data as CSV file
- ✅ Responsive web interface
- ✅ Toast notifications for user feedback
- ✅ Error handling and recovery
- ✅ Status indicators

**Out of Scope:**
- ❌ User authentication and accounts
- ❌ Multi-user data isolation
- ❌ Database backend (uses CSV only)
- ❌ Mobile native applications
- ❌ Real-time WebSocket updates
- ❌ Advanced charting/technical analysis
- ❌ Predictive analytics
- ❌ Multiple exchange support (CoinMarketCap only)
- ❌ API authentication (no API keys required)
- ❌ Email alerts or notifications

### Data Scope
- **Data Source:** CoinMarketCap website
- **Data Points:** Top 10 cryptocurrencies by market cap
- **Metrics:** Rank, Name, Symbol, Price (USD), 24h Change (%), Market Cap (USD)
- **Update Frequency:** Manual scraping (on-demand)
- **Historical Range:** All past scrapes stored in history CSV
- **Retention:** Until manually deleted

### Geographical Scope
- **Global access** to CoinMarketCap data
- **No regional restrictions** in application logic
- **All prices in USD** (CoinMarketCap default)

### Performance Scope
- **Response Time:** ~3-5 seconds for scraping (dependent on network)
- **User Limit:** Single user (no concurrent access handling)
- **Data Volume:** 10 cryptocurrencies × ~6 columns
- **Storage:** CSV files (no size limits for typical use)

---

## 9. Methodology

### Development Methodology: Iterative Development

**Approach:**
1. **Requirements Analysis** - Identify functionality needs
2. **Design Phase** - Plan architecture and data flow
3. **Implementation** - Build features incrementally
4. **Testing** - Validate functionality at each step
5. **Refinement** - Optimize and add enhancements

### Technical Approach

**Data Collection Strategy:**
- Web scraping using Selenium (dynamic content loading)
- Target: CoinMarketCap top 10 list
- Method: CSS selectors for element location
- Wait strategy: Explicit waits for element presence

**Data Processing Pipeline:**
```
Raw HTML Extraction
        ↓
Data Parsing & Cleaning
        ↓
Type Conversion (str → float/int)
        ↓
Timestamp Addition
        ↓
DataFrame Creation (Pandas)
        ↓
CSV Storage (History + Latest)
        ↓
JSON Formatting for Frontend
```

**Architecture Pattern: MVC-Inspired**
- **Model:** Data layer (scraper.py) handles data retrieval
- **View:** Presentation layer (HTML/CSS/JS) handles UI
- **Controller:** Business logic (app.py) coordinates operations

### Testing Strategy

**Manual Testing:**
- Scraping functionality validation
- Filter and sort operations
- CSV download verification
- UI responsiveness testing
- Error scenario handling

**Edge Cases Tested:**
- Empty data scenarios
- Network timeout handling
- Large number formatting
- Negative percentage changes
- Non-existent file handling

---

## 10. Implementation

### Installation Steps

#### Step 1: Clone/Setup Project
```bash
# Navigate to project directory
cd "crypto currency tracker"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Verify Chrome Installation
- Ensure Google Chrome is installed on your system
- The application will auto-detect Chrome location

#### Step 4: Run the Application
```bash
python app.py
```

#### Step 5: Access the Web Interface
- Open web browser
- Navigate to: `http://127.0.0.1:5000`
- Press **Scrape Data** button to fetch cryptocurrency data

### Project Configuration

**Flask Configuration (app.py):**
```python
app.secret_key = "crypto_tracker_secret_key_college_project"  # Secret for session management
app.run(debug=True, host="127.0.0.1", port=5000)  # Development settings
```

**Selenium Configuration (scraper.py):**
```python
HEADLESS_MODE = False  # Show browser window (True hides it)
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--no-sandbox')  # Security option for Linux
```

**CSV File Locations:**
- **Historical:** `crypto_history.csv` (append mode)
- **Latest:** `latest_crypto.csv` (overwrite mode)

### Data Flow Diagram

```
┌─────────────────────────────────┐
│  User Clicks "Scrape Data"      │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  AJAX Request: GET /scrape      │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  app.py: /scrape Route          │
│  Calls: scrape_top_10()         │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  scraper.py: Web Scraping       │
│  - Selenium WebDriver           │
│  - Parse CoinMarketCap HTML     │
│  - Extract 10 Cryptocurrencies  │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  Data Cleaning & Processing     │
│  - Convert to DataFrame         │
│  - Add Timestamp                │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  Save to CSV Files              │
│  - crypto_history.csv (append)  │
│  - latest_crypto.csv (new)      │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  JSON Response to Frontend      │
│  - Coin data array              │
│  - Formatted values             │
│  - Timestamp                    │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  JavaScript: Update UI          │
│  - Populate table rows          │
│  - Update timestamp             │
│  - Show success message         │
└─────────────────────────────────┘
```

### File Descriptions

**app.py (Main Application)**
- Lines: ~115
- Purpose: Flask application with routes and business logic
- Key Routes: `/` (index), `/scrape`, `/download`
- Handles: HTTP requests, data formatting, file downloads

**scraper.py (Web Scraping Module)**
- Lines: ~180
- Purpose: Selenium-based data extraction from CoinMarketCap
- Key Function: `scrape_top_10()`
- Handles: Browser automation, data parsing, CSV export

**templates/index.html (Frontend Template)**
- Lines: ~300+
- Purpose: HTML structure for web interface
- Components: Header, filters, data table, toast notifications
- Styling: Bootstrap 5 + custom CSS

**static/style.css (Styling)**
- Purpose: Visual design and responsive layout
- Features: Dark theme, animations, responsive breakpoints

**requirements.txt (Dependencies)**
- Flask >= 2.3.3
- pandas >= 2.0.0
- selenium >= 4.15.2

---

## 11. Output Screenshots

### Expected Application Features

**1. Initial Landing Page**
- Empty state with "No Data Available" message
- Scrape Data and Download buttons ready
- Filter panel on left with input fields
- Status showing "Idle"

**2. After Clicking "Scrape Data"**
- Loading spinner appears on button
- Status changes to "Scanning..."
- Browser window opens showing live scraping
- Toast notification: "Scraping in progress..."

**3. Data Loaded Successfully**
- Table populates with 10 rows of cryptocurrency data
- Columns: Rank, Name, Symbol, Price, 24h Change, Market Cap
- Green highlight for positive 24h change
- Red highlight for negative 24h change
- Timestamp shows "13 Jun 2026, 03:35 PM" format
- Status indicator becomes green "Synced"

**4. Applying Filters**
- Enter minimum price (e.g., "100")
- Check "Sort by 24h Gainers"
- Click "Apply Filters"
- Table updates showing only matching results
- Sorted by highest gains descending

**5. Download CSV**
- Click "Download CSV" button
- File `crypto_prices.csv` downloads to computer
- Contains all latest cryptocurrency data
- Can be opened in Excel/LibreOffice

**6. Example Table Data**
```
Rank    Name          Symbol  Price      24h Change  Market Cap
1       Bitcoin       BTC     $45,000.50 -2.35%      $882,000,000,000
2       Ethereum      ETH     $2,500.75  +1.25%      $300,000,000,000
3       Tether        USDT    $1.00      +0.05%      $95,000,000,000
4       BNB           BNB     $600.25    -1.80%      $92,000,000,000
5       XRP           XRP     $2.45      +3.10%      $130,000,000,000
```

### User Experience Flow

```
Landing Page
    ↓
[Click "Scrape Data"]
    ↓
Loading State (3-5 seconds)
    ↓
Data Table Loaded
    ↓
[Optional: Apply Filters]
    ↓
[Optional: Download CSV]
    ↓
End Session
```

---

## 12. Conclusion

### Project Summary

CryptoHub successfully demonstrates a modern web application that combines **web scraping**, **data processing**, and **interactive web interface** to deliver real-time cryptocurrency market insights. The project integrates multiple Python libraries (Flask, Selenium, Pandas) with frontend technologies (HTML, CSS, JavaScript, Bootstrap) to create a cohesive user experience.

### Key Achievements

✅ **Functional Web Application:**
- Fully operational Flask web server
- Real-time data scraping from CoinMarketCap
- Interactive data filtering and sorting
- CSV data export capability

✅ **Robust Architecture:**
- Separation of concerns (scraping vs. web server)
- Error handling throughout
- CSV-based data persistence
- Responsive design for multiple devices

✅ **User Experience:**
- Intuitive interface with clear call-to-action buttons
- Real-time feedback via toast notifications
- Efficient filtering and sorting
- Mobile-responsive layout

✅ **Data Management:**
- Historical data logging (crypto_history.csv)
- Latest data snapshot (latest_crypto.csv)
- Timestamp tracking for all records
- Proper data type handling

### Learning Outcomes

**Technical Skills Demonstrated:**
1. **Python Web Development:** Flask framework, routing, templates
2. **Web Scraping:** Selenium automation, CSS selectors, explicit waits
3. **Data Processing:** Pandas DataFrames, CSV operations
4. **Frontend Development:** HTML5, CSS3, JavaScript, Bootstrap
5. **Software Engineering:** MVC pattern, error handling, project structure
6. **API Integration:** JSON responses, AJAX communication

**Best Practices Implemented:**
- Clean code organization and modularity
- Comprehensive error handling
- Descriptive comments and documentation
- Responsive design principles
- Secure configuration management

### Limitations & Future Enhancements

**Current Limitations:**
- Single user, no concurrent access
- Manual scraping (no scheduled updates)
- No database (CSV-based storage)
- No user authentication
- Limited to top 10 cryptocurrencies
- No advanced analytics

**Future Enhancement Opportunities:**
1. **Database Integration:** Replace CSV with PostgreSQL/MongoDB
2. **Scheduled Scraping:** Implement APScheduler for automatic updates
3. **User Accounts:** Add authentication and personalized watchlists
4. **Advanced Charts:** Integrate Plotly/Chart.js for price history visualization
5. **Alert System:** Email/SMS notifications for price thresholds
6. **API Endpoints:** RESTful API for third-party integrations
7. **Multi-Exchange Support:** Add Binance, Kraken, other exchanges
8. **Mobile App:** React Native or Flutter mobile version
9. **Predictive Analytics:** Machine learning for price predictions
10. **Performance Optimization:** Redis caching, async processing

### Final Assessment

**Project Completion Status:** ✅ **COMPLETE**

CryptoHub is a **production-ready proof-of-concept** that successfully demonstrates:
- Professional-grade Python web development
- Modern frontend development practices
- Effective integration of multiple technologies
- Scalable architecture for future enhancements

The project provides an excellent foundation for learning web development, data processing, and software engineering best practices. It can be easily extended with additional features and deployed to cloud platforms (Heroku, AWS, Azure) for public access.

---

## Appendix: Quick Reference

### Commands Quick Start
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run scraper standalone
python scraper.py

# Access application
http://127.0.0.1:5000
```

### File Structure Reference
```
crypto currency tracker/
├── app.py                    # Main application (115 lines)
├── scraper.py               # Scraper module (180 lines)
├── requirements.txt         # Dependencies
├── templates/
│   └── index.html          # Web interface
├── static/
│   └── style.css           # Styling
└── Project Documentation
    └── PROJECT_REPORT.md   # This file
```

### Default Configuration
- **Host:** 127.0.0.1 (localhost)
- **Port:** 5000
- **Debug Mode:** True (development)
- **Browser:** Google Chrome (Selenium)
- **Update Mode:** Manual (on-demand)

### Support & Troubleshooting
- Check error messages in Flask terminal
- View browser console for JavaScript errors
- Verify internet connection
- Ensure Chrome is installed
- Check file permissions for CSV files

---

**Project Duration:** College Project  
**Last Updated:** June 13, 2026  
**Status:** Active Development Ready  

---

*End of Report*
