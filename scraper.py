#!/usr/bin/env python3
"""
Pokemon Events Scraper
Scrapes events from events.pokemon.com and saves to events.json
Uses Selenium with Chrome to handle bot protection
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import hashlib

# US major cities grid for 100-mile radius coverage
SEARCH_LOCATIONS = [
    # West Coast
    {"city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    {"city": "Portland", "lat": 45.5152, "lon": -122.6784},
    {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"city": "San Diego", "lat": 32.7157, "lon": -117.1611},
    {"city": "Sacramento", "lat": 38.5816, "lon": -121.4944},
    {"city": "Fresno", "lat": 36.7378, "lon": -119.7871},
    
    # Mountain West
    {"city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"city": "Tucson", "lat": 32.2226, "lon": -110.9747},
    {"city": "Albuquerque", "lat": 35.0844, "lon": -106.6504},
    {"city": "Denver", "lat": 39.7392, "lon": -104.9903},
    {"city": "Salt Lake City", "lat": 40.7608, "lon": -111.8910},
    {"city": "Boise", "lat": 43.6150, "lon": -116.2023},
    
    # Southwest
    {"city": "El Paso", "lat": 31.7619, "lon": -106.4850},
    {"city": "San Antonio", "lat": 29.4241, "lon": -98.4936},
    {"city": "Austin", "lat": 30.2672, "lon": -97.7431},
    {"city": "Dallas", "lat": 32.7767, "lon": -96.7970},
    {"city": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"city": "Oklahoma City", "lat": 35.4676, "lon": -97.5164},
    {"city": "Tulsa", "lat": 36.1540, "lon": -95.9928},
    
    # Midwest
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
    
    # South
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
    
    # Northeast
    {"city": "Richmond", "lat": 37.5407, "lon": -77.4360},
    {"city": "Washington DC", "lat": 38.9072, "lon": -77.0369},
    {"city": "Baltimore", "lat": 39.2904, "lon": -76.6122},
    {"city": "Philadelphia", "lat": 39.9526, "lon": -75.1652},
    {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    {"city": "Newark", "lat": 40.7357, "lon": -74.1724},
    {"city": "Boston", "lat": 42.3601, "lon": -71.0589},
    {"city": "Buffalo", "lat": 42.8864, "lon": -78.8784},
    {"city": "Pittsburgh", "lat": 40.4406, "lon": -79.9959},
    
    # Additional coverage
    {"city": "Spokane", "lat": 47.6588, "lon": -117.4260},
    {"city": "Billings", "lat": 45.7833, "lon": -108.5007},
    {"city": "Fargo", "lat": 46.8772, "lon": -96.7898},
    {"city": "Des Moines", "lat": 41.5868, "lon": -93.6250},
    {"city": "Little Rock", "lat": 34.7465, "lon": -92.2896},
    {"city": "Jackson", "lat": 32.2988, "lon": -90.1848},
    {"city": "Louisville", "lat": 38.2527, "lon": -85.7585},
    {"city": "Charleston", "lat": 32.7765, "lon": -79.9311},
    {"city": "Columbia", "lat": 34.0007, "lon": -81.0348},
    {"city": "Greenville", "lat": 34.8526, "lon": -82.3940},
    {"city": "Providence", "lat": 41.8240, "lon": -71.4128},
    {"city": "Hartford", "lat": 41.7658, "lon": -72.6734},
    {"city": "Portland", "lat": 43.6591, "lon": -70.2568},
    {"city": "Manchester", "lat": 42.9956, "lon": -71.4548},
    {"city": "Burlington", "lat": 44.4759, "lon": -73.2121},
    {"city": "Anchorage", "lat": 61.2181, "lon": -149.9003},
    {"city": "Honolulu", "lat": 21.3099, "lon": -157.8581},
]

def create_driver():
    """Create and configure Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Try to use Chrome/Chromium
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Chrome not available, trying chromium-browser: {e}")
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def get_event_id(event_data):
    """Generate unique ID for an event based on its attributes"""
    # Create a hash from event details
    event_str = f"{event_data.get('title', '')}|{event_data.get('date', '')}|{event_data.get('location', '')}|{event_data.get('address', '')}"
    return hashlib.md5(event_str.encode()).hexdigest()

def scrape_location(driver, location):
    """Scrape events for a specific location"""
    lat = location['lat']
    lon = location['lon']
    city = location['city']
    
    # Get today's date in the format the site expects
    today = datetime.now().strftime('%Y-%m-%d')
    
    url = f"https://events.pokemon.com/EventLocator/Home?iskm=false&longitude={lon}&latitude={lat}&locale=en-US&range=100&startdate={today}"
    
    print(f"Scraping {city} ({lat}, {lon})...")
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load and bypass initial checks
        
        # Wait for events to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "event-item"))
            )
        except TimeoutException:
            # Try alternative selectors
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "event-card"))
                )
            except TimeoutException:
                print(f"No events found for {city}")
                return []
        
        events = []
        
        # Try multiple possible selectors
        event_elements = driver.find_elements(By.CLASS_NAME, "event-item")
        if not event_elements:
            event_elements = driver.find_elements(By.CLASS_NAME, "event-card")
        if not event_elements:
            event_elements = driver.find_elements(By.CLASS_NAME, "event")
        
        for event_elem in event_elements:
            try:
                event_data = {
                    'search_city': city,
                    'search_lat': lat,
                    'search_lon': lon
                }
                
                # Extract event details
                try:
                    event_data['title'] = event_elem.find_element(By.CLASS_NAME, "event-title").text
                except:
                    try:
                        event_data['title'] = event_elem.find_element(By.TAG_NAME, "h3").text
                    except:
                        event_data['title'] = "Unknown Event"
                
                try:
                    event_data['date'] = event_elem.find_element(By.CLASS_NAME, "event-date").text
                except:
                    try:
                        event_data['date'] = event_elem.find_element(By.CLASS_NAME, "date").text
                    except:
                        event_data['date'] = "Date TBA"
                
                try:
                    event_data['location'] = event_elem.find_element(By.CLASS_NAME, "event-location").text
                except:
                    try:
                        event_data['location'] = event_elem.find_element(By.CLASS_NAME, "location").text
                    except:
                        event_data['location'] = "Location TBA"
                
                try:
                    event_data['address'] = event_elem.find_element(By.CLASS_NAME, "event-address").text
                except:
                    try:
                        event_data['address'] = event_elem.find_element(By.CLASS_NAME, "address").text
                    except:
                        event_data['address'] = ""
                
                try:
                    event_data['description'] = event_elem.find_element(By.CLASS_NAME, "event-description").text
                except:
                    event_data['description'] = ""
                
                try:
                    event_data['event_type'] = event_elem.find_element(By.CLASS_NAME, "event-type").text
                except:
                    event_data['event_type'] = ""
                
                # Generate unique ID
                event_data['id'] = get_event_id(event_data)
                event_data['last_seen'] = datetime.now().isoformat()
                
                events.append(event_data)
                
            except Exception as e:
                print(f"Error parsing event: {e}")
                continue
        
        print(f"Found {len(events)} events in {city}")
        return events
        
    except Exception as e:
        print(f"Error scraping {city}: {e}")
        return []

def main():
    """Main scraping function"""
    print("Starting Pokemon Events Scraper")
    print(f"Scraping {len(SEARCH_LOCATIONS)} locations...")
    
    driver = create_driver()
    all_events = {}
    
    try:
        for i, location in enumerate(SEARCH_LOCATIONS):
            print(f"\nProgress: {i+1}/{len(SEARCH_LOCATIONS)}")
            events = scrape_location(driver, location)
            
            # Add events to dictionary, deduplicating by ID
            for event in events:
                event_id = event['id']
                if event_id not in all_events:
                    all_events[event_id] = event
                else:
                    # Update last_seen time for existing events
                    all_events[event_id]['last_seen'] = event['last_seen']
            
            # Rate limiting
            time.sleep(2)
        
        # Convert to list
        events_list = list(all_events.values())
        
        # Sort by date
        events_list.sort(key=lambda x: x.get('date', ''))
        
        # Save to JSON
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_events': len(events_list),
            'events': events_list
        }
        
        with open('events.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n\nScraping complete!")
        print(f"Total unique events found: {len(events_list)}")
        print(f"Data saved to events.json")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
