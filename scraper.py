#!/usr/bin/env python3
"""
Pokemon Events Scraper - Robust Version
Enhanced bot protection evasion and error handling
"""

import json
import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
import random

# Reduced location set for faster testing - covers major regions
SEARCH_LOCATIONS = [
    # Major cities only - strategic coverage
    {"city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"city": "Denver", "lat": 39.7392, "lon": -104.9903},
    {"city": "Dallas", "lat": 32.7767, "lon": -96.7970},
    {"city": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"city": "Atlanta", "lat": 33.7490, "lon": -84.3880},
    {"city": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    {"city": "Boston", "lat": 42.3601, "lon": -71.0589},
    {"city": "Washington DC", "lat": 38.9072, "lon": -77.0369},
]

def create_driver():
    """Create and configure Chrome driver with enhanced stealth"""
    chrome_options = Options()
    
    # Essential options
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Enhanced bot detection evasion
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Realistic user agent
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    # Window size
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Additional stealth
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    
    try:
        print("Installing ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to mask automation
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✓ ChromeDriver ready")
        return driver
        
    except Exception as e:
        print(f"✗ Error creating driver: {e}")
        raise

def get_event_id(event_data):
    """Generate unique ID for an event"""
    event_str = f"{event_data.get('title', '')}|{event_data.get('date', '')}|{event_data.get('location', '')}|{event_data.get('address', '')}"
    return hashlib.md5(event_str.encode()).hexdigest()

def scrape_location(driver, location, retry=0):
    """Scrape events for a specific location with retries"""
    lat = location['lat']
    lon = location['lon']
    city = location['city']
    
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://events.pokemon.com/EventLocator/Home?iskm=false&longitude={lon}&latitude={lat}&locale=en-US&range=100&startdate={today}"
    
    print(f"Scraping {city} ({lat}, {lon})...", flush=True)
    
    try:
        driver.get(url)
        
        # Random wait to appear more human-like
        wait_time = random.uniform(3, 6)
        time.sleep(wait_time)
        
        # Check for bot detection page
        page_source = driver.page_source.lower()
        if 'incapsula' in page_source or 'access denied' in page_source or 'security' in page_source:
            print(f"  ⚠ Bot protection detected for {city}")
            if retry < 2:
                print(f"  Retrying in 10 seconds... (attempt {retry + 1}/2)")
                time.sleep(10)
                return scrape_location(driver, location, retry + 1)
            return []
        
        # Save page for debugging if needed
        if os.getenv('DEBUG'):
            with open(f'debug_{city}.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
        
        events = []
        
        # Try multiple selectors for events
        selectors_to_try = [
            (By.CLASS_NAME, "event-item"),
            (By.CLASS_NAME, "event-card"),
            (By.CLASS_NAME, "event"),
            (By.CSS_SELECTOR, "[data-event-id]"),
            (By.CSS_SELECTOR, ".event-listing"),
            (By.CSS_SELECTOR, "div[class*='event']"),
        ]
        
        event_elements = []
        for by, selector in selectors_to_try:
            try:
                elements = driver.find_elements(by, selector)
                if elements and len(elements) > 0:
                    event_elements = elements
                    print(f"  ✓ Found {len(elements)} potential events using {selector}")
                    break
            except:
                continue
        
        if not event_elements:
            # Check if page says "no events"
            if 'no events' in page_source or 'no results' in page_source:
                print(f"  → No events scheduled in {city}")
            else:
                print(f"  ⚠ Could not find events in {city} (selectors may need update)")
            return []
        
        # Parse events
        for i, elem in enumerate(event_elements[:20]):  # Limit to 20 per location
            try:
                event_data = {
                    'search_city': city,
                    'search_lat': lat,
                    'search_lon': lon
                }
                
                # Try to extract text content
                text_content = elem.text.strip()
                if not text_content:
                    continue
                
                # Basic parsing - adjust based on actual structure
                lines = text_content.split('\n')
                if len(lines) >= 2:
                    event_data['title'] = lines[0] if len(lines) > 0 else "Unknown Event"
                    event_data['date'] = lines[1] if len(lines) > 1 else "Date TBA"
                    event_data['location'] = lines[2] if len(lines) > 2 else city
                    event_data['address'] = lines[3] if len(lines) > 3 else ""
                    event_data['description'] = '\n'.join(lines[4:]) if len(lines) > 4 else ""
                else:
                    event_data['title'] = text_content[:100]
                    event_data['date'] = "Date TBA"
                    event_data['location'] = city
                    event_data['address'] = ""
                    event_data['description'] = ""
                
                event_data['event_type'] = ""
                event_data['id'] = get_event_id(event_data)
                event_data['last_seen'] = datetime.now().isoformat()
                
                events.append(event_data)
                
            except Exception as e:
                print(f"  ⚠ Error parsing event {i}: {str(e)[:50]}")
                continue
        
        print(f"  ✓ Extracted {len(events)} events from {city}")
        return events
        
    except WebDriverException as e:
        print(f"  ✗ WebDriver error in {city}: {str(e)[:100]}")
        return []
    except Exception as e:
        print(f"  ✗ Error scraping {city}: {str(e)[:100]}")
        return []

def main():
    """Main scraping function"""
    print("=" * 60)
    print("Pokemon Events Scraper - Starting")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Locations to scrape: {len(SEARCH_LOCATIONS)}")
    print("=" * 60, flush=True)
    
    driver = None
    
    try:
        driver = create_driver()
        all_events = {}
        successful_scrapes = 0
        
        for i, location in enumerate(SEARCH_LOCATIONS):
            print(f"\n[{i+1}/{len(SEARCH_LOCATIONS)}] ", end='', flush=True)
            
            events = scrape_location(driver, location)
            
            if events:
                successful_scrapes += 1
                for event in events:
                    event_id = event['id']
                    if event_id not in all_events:
                        all_events[event_id] = event
                    else:
                        all_events[event_id]['last_seen'] = event['last_seen']
            
            # Rate limiting with randomization
            if i < len(SEARCH_LOCATIONS) - 1:
                wait = random.uniform(3, 7)
                time.sleep(wait)
        
        # Convert to list and sort
        events_list = list(all_events.values())
        events_list.sort(key=lambda x: x.get('date', ''))
        
        # Save results
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_events': len(events_list),
            'locations_scraped': len(SEARCH_LOCATIONS),
            'successful_scrapes': successful_scrapes,
            'events': events_list
        }
        
        with open('events.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("\n" + "=" * 60)
        print("✓ SCRAPING COMPLETE")
        print("=" * 60)
        print(f"Locations scraped: {successful_scrapes}/{len(SEARCH_LOCATIONS)}")
        print(f"Unique events found: {len(events_list)}")
        print(f"Data saved to: events.json")
        print("=" * 60, flush=True)
        
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}", flush=True)
        raise
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    main()
