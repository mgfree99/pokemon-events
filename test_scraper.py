#!/usr/bin/env python3
"""
Test script for Pokemon Events Scraper
Tests a single location to verify the scraper is working
"""

import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_driver():
    """Create and configure Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error creating driver: {e}")
        print("\nMake sure Chrome and ChromeDriver are installed:")
        print("  pip install selenium webdriver-manager")
        return None

def test_scrape():
    """Test scraping a single location"""
    print("Pokemon Events Scraper - Test Mode")
    print("=" * 50)
    
    driver = create_driver()
    if not driver:
        return
    
    try:
        # Test with Oklahoma City
        lat = 35.4676
        lon = -97.5164
        today = datetime.now().strftime('%Y-%m-%d')
        
        url = f"https://events.pokemon.com/EventLocator/Home?iskm=false&longitude={lon}&latitude={lat}&locale=en-US&range=100&startdate={today}"
        
        print(f"\nTesting with Oklahoma City")
        print(f"URL: {url}")
        print("\nLoading page...")
        
        driver.get(url)
        time.sleep(5)
        
        # Save screenshot for debugging
        try:
            driver.save_screenshot('test_screenshot.png')
            print("Screenshot saved as test_screenshot.png")
        except:
            pass
        
        # Save page source for inspection
        with open('test_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Page source saved as test_page_source.html")
        
        # Try to find events
        print("\nSearching for events...")
        
        selectors = [
            (By.CLASS_NAME, "event-item"),
            (By.CLASS_NAME, "event-card"),
            (By.CLASS_NAME, "event"),
            (By.CSS_SELECTOR, "[class*='event']"),
        ]
        
        events_found = False
        for by, selector in selectors:
            try:
                elements = driver.find_elements(by, selector)
                if elements:
                    print(f"✓ Found {len(elements)} elements with selector: {selector}")
                    events_found = True
                    
                    # Print first event details if found
                    if len(elements) > 0:
                        print("\nFirst event element HTML:")
                        print(elements[0].get_attribute('outerHTML')[:500])
                    break
            except Exception as e:
                print(f"✗ Selector {selector} failed: {e}")
        
        if not events_found:
            print("\n⚠ No events found. This could mean:")
            print("  1. No events are currently scheduled in this area")
            print("  2. The website structure has changed")
            print("  3. Bot protection is blocking the request")
            print("\nCheck test_page_source.html to inspect the actual page content")
        else:
            print("\n✓ Successfully found events!")
            print("\nNext steps:")
            print("  1. Review the HTML structure in test_page_source.html")
            print("  2. Update selectors in scraper.py if needed")
            print("  3. Run the full scraper: python scraper.py")
    
    finally:
        driver.quit()
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_scrape()
