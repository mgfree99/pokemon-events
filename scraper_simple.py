#!/usr/bin/env python3
"""
Alternative Pokemon Events Scraper - Simple Version
Uses requests with retry logic if Selenium has issues
Note: May not work if site has strict bot protection
"""

import json
import time
import requests
from datetime import datetime
import hashlib

# Same locations as main scraper
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
]

def get_event_id(event_data):
    """Generate unique ID for an event"""
    event_str = f"{event_data.get('title', '')}|{event_data.get('date', '')}|{event_data.get('location', '')}"
    return hashlib.md5(event_str.encode()).hexdigest()

def fetch_events_api(lat, lon, city):
    """
    Try to fetch events via API endpoint
    Note: This is speculative - the actual API endpoint may be different
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://events.pokemon.com/'
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Try potential API endpoints
    endpoints = [
        f"https://events.pokemon.com/api/events?latitude={lat}&longitude={lon}&range=100",
        f"https://events.pokemon.com/api/v1/events?lat={lat}&lng={lon}&radius=100",
        f"https://events.pokemon.com/EventLocator/api/search?lat={lat}&lon={lon}&range=100",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data and isinstance(data, (list, dict)):
                        print(f"✓ Found API endpoint: {endpoint}")
                        return parse_api_response(data, city, lat, lon)
                except:
                    pass
        except:
            continue
    
    return None

def parse_api_response(data, city, lat, lon):
    """Parse API response into events list"""
    events = []
    
    # Handle different possible response formats
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # Try common keys
        items = data.get('events', data.get('results', data.get('data', [])))
    else:
        return events
    
    for item in items:
        try:
            event = {
                'id': get_event_id(item),
                'title': item.get('name', item.get('title', 'Unknown Event')),
                'date': item.get('date', item.get('start_date', 'Date TBA')),
                'location': item.get('location', item.get('venue', 'Location TBA')),
                'address': item.get('address', ''),
                'description': item.get('description', ''),
                'event_type': item.get('type', item.get('event_type', '')),
                'search_city': city,
                'search_lat': lat,
                'search_lon': lon,
                'last_seen': datetime.now().isoformat()
            }
            events.append(event)
        except:
            continue
    
    return events

def main():
    """Main scraping function"""
    print("Alternative Pokemon Events Scraper")
    print("Attempting to find API endpoints...")
    
    all_events = {}
    successful_locations = 0
    
    for i, location in enumerate(SEARCH_LOCATIONS[:10]):  # Test first 10
        city = location['city']
        lat = location['lat']
        lon = location['lon']
        
        print(f"\n[{i+1}/10] Testing {city}...")
        
        events = fetch_events_api(lat, lon, city)
        
        if events:
            successful_locations += 1
            for event in events:
                event_id = event['id']
                if event_id not in all_events:
                    all_events[event_id] = event
            print(f"  Found {len(events)} events")
        else:
            print(f"  No API endpoint found")
        
        time.sleep(1)
    
    if successful_locations == 0:
        print("\n⚠ Could not find working API endpoint")
        print("This scraper requires an accessible API.")
        print("Please use the main scraper.py with Selenium instead.")
        return
    
    # Save results
    events_list = list(all_events.values())
    events_list.sort(key=lambda x: x.get('date', ''))
    
    output = {
        'last_updated': datetime.now().isoformat(),
        'total_events': len(events_list),
        'events': events_list
    }
    
    with open('events.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Success! Found {len(events_list)} unique events")
    print("Data saved to events.json")

if __name__ == "__main__":
    main()
