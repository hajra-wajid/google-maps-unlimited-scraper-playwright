# it's just sample...this script didn't bypass 120 results limit.
# contact to me for the full version script _ Hajra Wajid

import asyncio
import pandas as pd
import time
import random
import re
from urllib.parse import unquote
from playwright.async_api import async_playwright

# Configuration
MAX_BROWSERS = 10
MAX_SCROLL_ATTEMPTS = 6
OUTPUT_FILE = "results.xlsx"
PHONE_REGEX = re.compile(r'(\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')

class Tracker:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.stats = {
            'total': 0,
            'processed': 0,
            'errors': 0,
            'active_workers': {}
        }
    
    async def log(self, worker_id, message, is_error=False):
        async with self.lock:
            if is_error:
                self.stats['errors'] += 1
            else:
                self.stats['processed'] += 1
                self.stats['total'] += 1
            print(f"[Worker {worker_id}] {message}")

async def random_delay(min=0.5, max=1.5):
    await asyncio.sleep(random.uniform(min, max))

async def scroll_to_bottom(page, worker_id, tracker):
    last_count = 0
    attempts = 0
    
    while attempts < MAX_SCROLL_ATTEMPTS:
        await page.evaluate('''() => {
            const feed = document.querySelector('div[role="feed"]');
            if (feed) feed.scrollBy(0, feed.clientHeight * 0.8)
        }''')
        
        await random_delay(1, 2)
        await page.wait_for_load_state('networkidle')
        
        current_items = await page.query_selector_all('a.hfpxzc')
        current_count = len(current_items)
        
        if current_count > last_count:
            await tracker.log(worker_id, f"🔄 New listings: {current_count - last_count} (Total: {current_count})")
            last_count = current_count
            attempts = 0
        else:
            attempts += 1
            if attempts >= 3:
                await tracker.log(worker_id, "✅ Reached scroll limit")
                break

async def extract_phone_number(page):
    try:
        # Method 1: Direct telephone link
        tel_link = await page.query_selector('a[href^="tel:"]')
        if tel_link:
            return (await tel_link.get_attribute('href')).replace('tel:', '').strip()

        # Method 2: Copy button section
        copy_button = await page.query_selector('button[aria-label="Copy phone number"]')
        if copy_button:
            parent = await copy_button.query_selector('xpath=../..')
            if parent:
                phone_text = await parent.inner_text()
                match = PHONE_REGEX.search(phone_text)
                if match:
                    return match.group(0)

        # Method 3: Full-text search
        body_text = await page.inner_text('body')
        match = PHONE_REGEX.search(body_text)
        return match.group(0) if match else "N/A"
    except:
        return "N/A"

async def extract_website(page):
    try:
        element = await page.query_selector('a[aria-label="Open website"]')
        if not element:
            return "N/A"
            
        url = await element.get_attribute('href')
        if '/url?q=' in url:
            return unquote(url.split('q=')[1].split('&')[0])
        return url.strip()
    except:
        return "N/A"

async def process_business(page, url, term, worker_id, tracker):
    try:
        await page.goto(url, timeout=60000)
        await random_delay(0.8, 1.2)
        
        data = {
            "Search Term": term,
            "Shop Name": await page.eval_on_selector('h1.DUwDvf', 'el => el?.innerText', "N/A"),
            "Shop Type": await page.eval_on_selector('button.DkEaL', 'el => el?.innerText', "N/A"),
            "Shop Address": await page.eval_on_selector('div.Io6YTe:nth-of-type(1)', 'el => el?.innerText', "N/A"),
            "Phone Number": await extract_phone_number(page),
            "Website": await extract_website(page)
        }
        
        await tracker.log(worker_id, f"✅ Processed: {data['Shop Name'][:30]}...")
        return data
    except Exception as e:
        await tracker.log(worker_id, f"❌ Failed: {str(e)[:50]}", is_error=True)
        return None
    finally:
        await page.go_back()

async def process_term(page, term, worker_id, tracker):
    try:
        await tracker.log(worker_id, f"🚀 Starting: {term}")
        await page.goto(f"https://www.google.com/maps/search/{term.replace(' ', '+')}", timeout=60000)
        await page.wait_for_selector('div[role="feed"]', timeout=10000)
        
        await scroll_to_bottom(page, worker_id, tracker)
        
        links = await page.query_selector_all('a.hfpxzc')
        urls = [await link.get_attribute('href') for link in links]
        
        results = []
        for idx, url in enumerate(urls):
            await tracker.log(worker_id, f"⏳ Processing {idx+1}/{len(urls)}")
            data = await process_business(page, url, term, worker_id, tracker)
            if data:
                results.append(data)
        
        await tracker.log(worker_id, f"🏁 Completed: {term} ({len(results)} results)")
        return results
    except Exception as e:
        await tracker.log(worker_id, f"🔥 Term failed: {str(e)[:50]}", is_error=True)
        return []

async def browser_worker(terms, worker_id, tracker):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={"width": 1366, "height": 768}
            )
            page = await context.new_page()
            
            all_results = []
            for term in terms:
                await random_delay(2, 5)
                results = await process_term(page, term, worker_id, tracker)
                all_results.extend(results)
            
            await browser.close()
            return all_results
    except Exception as e:
        await tracker.log(worker_id, f"🚨 Worker crashed: {str(e)[:50]}", is_error=True)
        return []

def distribute_terms(terms, num_browsers):
    return [terms[i::num_browsers] for i in range(num_browsers)]

async def main():
    tracker = Tracker()
    start_time = time.time()
    
    with open("terms.txt") as f:
        terms = [line.strip() for line in f if line.strip()]
    
    term_batches = distribute_terms(terms, MAX_BROWSERS)
    tasks = [browser_worker(batch, i, tracker) for i, batch in enumerate(term_batches)]
    
    results = await asyncio.gather(*tasks)
    
    # Flatten and filter results
    combined = [item for sublist in results if sublist for item in sublist]
    
    # Save to Excel
    df = pd.DataFrame(combined)
    df.to_excel(OUTPUT_FILE, index=False)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Scraping Summary")
    print(f"{'='*50}")
    print(f"Total Terms: {len(terms)}")
    print(f"Total Businesses: {len(df)}")
    #print(f"Successful: {tracker.stats['processed']}")
    print(f"Errors: {tracker.stats['errors']}")
    print(f"Duration: {(time.time()-start_time)/60:.2f} mins")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(main())