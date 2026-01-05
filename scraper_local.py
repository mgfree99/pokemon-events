#!/usr/bin/env python3
"""
Pokemon Events Scraper - Local Version
Run this on your home computer to bypass bot protection
Automatically pushes results to GitHub
"""

import json
import time
import os
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import hashlib
import random

# Full US coverage - 65 locations
SEARCH_LOCATIONS = [
    {"city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    {"city": "Portland", "lat": 45.5152, "lon": -122.6784},
    {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"city": "San Diego", "lat": 32.7157, "lon": -117.1611},
    {"city": "Sacramento", "lat": 38.5816, "lon": -121.4944},
    {"city": "Fresno", "lat": 36.7378, "lon": -119.7871},
    {"city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"city": "Tucson", "lat": 32.2226, "lon": -110.9747},
    {"city": "Albuquerque", "lat": 35.0844, "lon": -106.6504},
    {"city": "Denver", "lat": 39.7392, "lon": -104.9903},
    {"city": "Salt Lake City", "lat": 40.7608, "lon": -111.8910},
    {"city": "Boise", "lat": 43.6150, "lon": -116.2023},
    {"city": "El Paso", "lat": 31.7619, "lon": -106.4850},
    {"city": "San Antonio", "lat": 29.4241, "lon": -98.4936},
    {"city": "Austin", "lat": 30.2672, "lon": -97.7431},
    {"city": "Dallas", "lat": 32.7767, "lon": -96.7970},
    {"city": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"city": "Oklahoma City", "lat": 35.4676, "lon": -97.5164},
    {"city": "Tulsa", "lat": 36.1540, "lon": -95.9928},
    {"city": "Kansas City", "lat": 39.0997, "lon": -94.5786},
    {"city": "Omaha", "lat": 41.2565, "lon": -95.9345},
    {"city": "Minneapolis", "lat": 44.9778, "lon": -93.2650},
    {"city": "Milwaukee", "lat": 43.0389, "lon": -87.9065},
    {"city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"city": "St. Louis", "lat": 38.6270, "lon": -90.1994},
    {"city": "Indianapolis", "lat": 39.7684, "lon": -86.1581},
    {"city": "Detroit", "lat": 42.3314, "lon": -83.0458},
    {"city": "Cleveland", "lat": 41.4993, "lon": -81.6944},
    {"city": "Cincinnati", "lat": 39.1031, "lon": -84.5120},
    {"city": "Columbus", "lat": 39.9612, "lon": -82.9988},
    {"city": "Memphis", "lat": 35.1495, "lon": -90.0490},
    {"city": "Nashville", "lat": 36.1627, "lon": -86.7816},
    {"city": "Birmingham", "lat": 33.5186, "lon": -86.8104},
    {"city": "Atlanta", "lat": 33.7490, "lon": -84.3880},
    {"city": "Jacksonville", "lat": 30.3322, "lon": -81.6557},
    {"city": "Orlando", "lat": 28.5383, "lon": -81.3792},
    {"city": "Tampa", "lat": 27.9506, "lon": -82.4572},
    {"city": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"city": "New Orleans", "lat": 29.9511, "lon": -90.0715},
    {"city": "Charlotte", "lat": 35.2271, "lon": -80.8431},
    {"city": "Raleigh", "lat": 35.7796, "lon": -78.6382},
    {"city": "Richmond", "lat": 37.5407, "lon": -77.4360},
    {"city": "Washington DC", "lat": 38.9072, "lon": -77.0369},
    {"city": "Baltimore", "lat": 39.2904, "lon": -76.6122},
    {"city": "Philadelphia", "lat": 39.9526, "lon": -75.1652},
    {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    {"city": "Newark", "lat": 40.7357, "lon": -74.1724},
    {"city": "Boston", "lat": 42.3601, "lon": -71.0589},
    {"city": "Buffalo", "lat": 42.8864, "lon": -78.8784},
    {"city": "Pittsburgh", "lat": 40.4406, "lon": -79.9959},
    {"city": "Spokane", "lat": 47.6588, "lon": -117.4260},
    {"city": "Billings", "lat": 45.7833, "lon": -108.5007},
    {"city": "Fargo", "lat": 46.8772, "lon": -96.7898},
    {"city": "Des Moines", "lat": 41.5868, "lon": -93.6250},
    {"city": "Little Rock", "lat": 34.7465, "lon": -92.2896},
    {"city": "Jackson", "lat": 32.2988, "lon": -90.1848},
    {"city": "Louisville", "lat": 38.2527, "lon": -85.7585},
    {"city": "Charleston", "lat": 32.7765, "lon": -79.9311},
    {"city": "Columbia", "lat": 34.0007, "lon": -81.0348},
    {"city": "Providence", "lat": 41.8240, "lon": -71.4128},
    {"city": "Hartford", "lat": 41.7658, "lon": -72.6734},
    {"city": "Anchorage", "lat": 61.2181, "lon": -149.9003},
    {"city": "Honolulu", "lat": 21.3099, "lon": -157.8581},
]

def create_driver():
    """Create Chrome driver - runs in visible mode for better success"""
    chrome_options = Options()
    
    # Run in visible mode (less suspicious than headless from home computer)
    # chrome_options.add_argument('--headless=new')  # Comment out to see browser
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--window-size=1920,1080')
    
    print("Starting Chrome browser...")
    print("(You'll see the browser window - this is normal!)")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Stealth JavaScript
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✓ Browser ready\n")
        return driver
        
    except Exception as e:
        print(f"\n✗ Error: Could not start Chrome")
        print(f"Error details: {e}")
        print("\nMake sure you have:")
        print("1. Chrome browser installed")
        print("2. Run: pip install selenium")
        print("3. ChromeDriver will auto-install\n")
        raise

def get_event_id(event_data):
    """Generate unique ID for an event"""
    event_str = f"{event_data.get('title', '')}|{event_data.get('date', '')}|{event_data.get('location', '')}|{event_data.get('address', '')}"
    return hashlib.md5(event_str.encode()).hexdigest()

def scrape_location(driver, location):
    """Scrape events for a specific location"""
    lat = location['lat']
    lon = location['lon']
    city = location['city']
    
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://events.pokemon.com/EventLocator/Home?iskm=false&longitude={lon}&latitude={lat}&locale=en-US&range=100&startdate={today}"
    
    print(f"📍 {city}...", end=' ', flush=True)
    
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        
        # Check for bot detection
        page_source = driver.page_source.lower()
        if 'incapsula' in page_source or 'access denied' in page_source:
            print("⚠️ blocked")
            return []
        
        events = []
        
        # Try to find events - will need to inspect actual page to get correct selectors
        selectors = [
            (By.CLASS_NAME, "event-item"),
            (By.CLASS_NAME, "event-card"),
            (By.CSS_SELECTOR, "[class*='event']"),
        ]
        
        event_elements = []
        for by, selector in selectors:
            try:
                elements = driver.find_elements(by, selector)
                if elements and len(elements) > 0:
                    event_elements = elements
                    break
            except:
                continue
        
        if not event_elements:
            if 'no events' in page_source or 'no results' in page_source:
                print("→ no events")
            else:
                print("⚠️ need selector update")
            return []
        
        # Parse events
        for elem in event_elements[:20]:
            try:
                text = elem.text.strip()
                if not text:
                    continue
                
                lines = text.split('\n')
                event_data = {
                    'title': lines[0] if len(lines) > 0 else "Unknown Event",
                    'date': lines[1] if len(lines) > 1 else "Date TBA",
                    'location': lines[2] if len(lines) > 2 else city,
                    'address': lines[3] if len(lines) > 3 else "",
                    'description': '\n'.join(lines[4:]) if len(lines) > 4 else "",
                    'event_type': "",
                    'search_city': city,
                    'search_lat': lat,
                    'search_lon': lon,
                    'last_seen': datetime.now().isoformat()
                }
                
                event_data['id'] = get_event_id(event_data)
                events.append(event_data)
                
            except:
                continue
        
        print(f"✓ {len(events)} events")
        return events
        
    except Exception as e:
        print(f"✗ error: {str(e)[:30]}")
        return []

def push_to_github():
    """Push the updated events.json to GitHub"""
    print("\n" + "="*60)
    print("📤 Pushing to GitHub...")
    print("="*60)
    
    try:
        # Check if git is configured
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("⚠️  Git not configured. Setting up...")
            subprocess.run(['git', 'config', 'user.name', 'Pokemon Events Scraper'])
            subprocess.run(['git', 'config', 'user.email', 'scraper@pokemon-events.local'])
        
        # Add and commit
        subprocess.run(['git', 'add', 'events.json'], check=True)
        
        commit_msg = f"Update Pokemon events - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push
        result = subprocess.run(['git', 'push'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Successfully pushed to GitHub!")
            print("Your website will update in 1-2 minutes")
        else:
            print("✗ Push failed:")
            print(result.stderr)
            print("\nYou may need to:")
            print("1. Run 'git push' manually")
            print("2. Check your GitHub credentials")
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")
        print("\nYou can manually push with:")
        print("  git add events.json")
        print("  git commit -m 'Update events'")
        print("  git push")
    except FileNotFoundError:
        print("✗ Git not found. Please install Git:")
        print("  https://git-scm.com/downloads")

def main():
    """Main scraping function"""
    print("\n" + "="*60)
    print("🎮 POKEMON EVENTS SCRAPER - LOCAL VERSION")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Locations: {len(SEARCH_LOCATIONS)}")
    print("="*60 + "\n")
    
    driver = None
    
    try:
        driver = create_driver()
        all_events = {}
        successful = 0
        
        for i, location in enumerate(SEARCH_LOCATIONS):
            print(f"[{i+1}/{len(SEARCH_LOCATIONS)}] ", end='')
            
            events = scrape_location(driver, location)
            
            if events:
                successful += 1
                for event in events:
                    event_id = event['id']
                    if event_id not in all_events:
                        all_events[event_id] = event
                    else:
                        all_events[event_id]['last_seen'] = event['last_seen']
            
            # Rate limiting
            if i < len(SEARCH_LOCATIONS) - 1:
                time.sleep(random.uniform(2, 4))
        
        # Save results
        events_list = list(all_events.values())
        events_list.sort(key=lambda x: x.get('date', ''))
        
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_events': len(events_list),
            'locations_scraped': len(SEARCH_LOCATIONS),
            'successful_scrapes': successful,
            'events': events_list
        }
        
        with open('events.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("\n" + "="*60)
        print("✅ SCRAPING COMPLETE!")
        print("="*60)
        print(f"✓ Scraped: {successful}/{len(SEARCH_LOCATIONS)} locations")
        print(f"✓ Found: {len(events_list)} unique events")
        print(f"✓ Saved to: events.json")
        print("="*60)
        
        # Ask user if they want to push to GitHub
        print("\nWould you like to push these results to GitHub? (y/n): ", end='')
        response = input().strip().lower()
        
        if response == 'y':
            push_to_github()
        else:
            print("\nSkipped GitHub push. You can push manually later with:")
            print("  git add events.json")
            print("  git commit -m 'Update events'")
            print("  git push")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping cancelled by user")
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()
        
        print("\n" + "="*60)
        print("Done! Press Enter to exit...")
        input()

if __name__ == "__main__":
    main()
