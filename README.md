# google-maps-unlimited-scraper-playwright
"Advanced Python &amp; Playwright solution to bypass Google Maps 120-result limit, enabling unlimited business data extraction for market research, lead generation, and competitive analysis."
<br>
# Unlimited Google Maps Business Data Extraction

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)
![Google Maps](https://img.shields.io/badge/Google%20Maps-Data-red.svg)
![Asyncio](https://img.shields.io/badge/Asyncio-Concurrency-purple.svg)

## Project Overview

This repository presents a cutting-edge web scraping solution engineered to overcome the significant challenge of Google Maps' inherent 120-result limitation. Utilizing Python with Playwright and asynchronous programming, this system enables the extraction of an unlimited volume of business data, providing a powerful tool for market research, lead generation, and competitive intelligence.

## The Challenge: Bypassing the 120-Result Limit

Google Maps typically restricts search results to approximately 120 entries, making comprehensive data collection impossible for many business needs. This project directly addresses this limitation by implementing advanced techniques to bypass these restrictions and access a complete dataset.

## Key Features

-   **Unlimited Data Extraction:** Successfully bypasses Google Maps' 120-result limit to extract comprehensive business data.
-   **Advanced Anti-Bot Measures:** Employs sophisticated Playwright techniques to navigate dynamic content and evade anti-scraping mechanisms.
-   **High Concurrency & Speed:** Leverages `asyncio` and multiple browser instances for rapid and efficient data collection.
-   **Comprehensive Data Fields:** Extracts:
    -   Shop Name
    -   Shop Type
    -   Shop Address
    -   Phone Number
    -   Website
    -   Plus Code (if available)
-   **Robust Error Handling:** Designed for resilience against network issues and website changes.
-   **Scalable Architecture:** Built to handle large-scale data extraction needs.

## Technologies Used

-   **Python 3.x**
-   **Playwright** (for browser automation)
-   **Asyncio** (for asynchronous operations)
-   **Pandas** (for data processing and structuring)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hajra-wajid/google-maps-unlimited-scraper-playwright.git
    cd google-maps-unlimited-scraper-playwright
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    _Note: A `requirements.txt` file will be provided in the actual repository containing `playwright`, `pandas`, and other required packages._

4.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

## Usage

1.  **Prepare `terms.txt`:** Create a `terms.txt` file in the project root, with each line containing a search query (e.g., "restaurants in New York", "plumbers in London").

2.  **Run the scraper:**
    ```bash
    python main.py
    ```

## Data Output

The extracted data will be saved in `results.xlsx` with the following columns:

-   `Shop Name`
-   `Shop Type`
-   `Shop Address`
-   `Phone Number`
-   `Website`
-   `Website Plus Code`
