# Pokemon Events Locator

A lightweight, user-friendly website for finding official Pokemon events across the United States. Data is automatically updated daily and hosted via GitHub Pages.

## Features

- 🗺️ **Comprehensive US Coverage**: Searches 65+ major cities with 100-mile radius to cover the entire United States
- 🔍 **Smart Search**: Search by city, state, or zip code with adjustable radius (25-500 miles)
- 📱 **Mobile Friendly**: Lightweight design that works on any device
- 🔄 **Auto-Updates**: Daily automated scraping via GitHub Actions
- ⚡ **Fast & Efficient**: Minimal resource usage with clean, simple interface
- 🎯 **Deduplication**: Automatically removes duplicate events from overlapping search areas

## Live Demo

Once deployed, your site will be available at: `https://YOUR-USERNAME.github.io/REPO-NAME/`

## Setup Instructions

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `pokemon-events` or `pokemon-event-locator`
3. Make it **Public** (required for GitHub Pages free hosting)
4. Initialize with a README (optional)

### 2. Upload Files

Upload all the following files to your repository:

```
pokemon-events/
├── index.html              # Main website
├── events.json             # Events data (will be auto-updated)
├── scraper.py              # Python scraper script
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── update-events.yml  # GitHub Actions workflow
└── README.md              # This file
```

### 3. Enable GitHub Pages

1. Go to your repository **Settings**
2. Navigate to **Pages** in the left sidebar
3. Under **Source**, select:
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
4. Click **Save**
5. Your site will be published at `https://YOUR-USERNAME.github.io/REPO-NAME/`

### 4. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"** if prompted
3. The scraper will now run automatically every day at 6 AM UTC
4. You can also trigger it manually by going to Actions → Update Pokemon Events → Run workflow

### 5. First Run

To populate the initial data:

1. Go to **Actions** tab
2. Click on **Update Pokemon Events** workflow
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**
5. Wait for it to complete (takes ~10-15 minutes)

## How It Works

### Data Collection

The scraper (`scraper.py`) works by:

1. **Geographic Coverage**: Uses a grid of 65+ US cities strategically placed to ensure 100-mile radius coverage of the entire country
2. **Web Scraping**: Uses Selenium with headless Chrome to navigate events.pokemon.com
3. **Deduplication**: Generates unique IDs for events to prevent duplicates from overlapping search areas
4. **Automated Updates**: GitHub Actions runs the scraper daily and commits updated data

### Search Locations

The scraper covers major population centers including:
- All 50 US states
- Major metropolitan areas
- Strategic coverage points for rural areas
- Alaska and Hawaii

### User Interface

The website (`index.html`) provides:
- **Search by Location**: Enter any US city, state, or zip code
- **Radius Filter**: Choose search radius from 25 to 500 miles
- **Geocoding**: Uses OpenStreetMap's free Nominatim API to convert locations to coordinates
- **Distance Calculation**: Uses Haversine formula to calculate distances
- **Real-time Filtering**: Events are filtered client-side for fast performance

## Customization

### Adjust Scraping Schedule

Edit `.github/workflows/update-events.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
  # Change to:
  - cron: '0 */12 * * *'  # Every 12 hours
  - cron: '0 0 * * 0'     # Weekly on Sunday
```

### Modify Search Locations

Edit `scraper.py` and adjust the `SEARCH_LOCATIONS` list to add/remove cities:

```python
SEARCH_LOCATIONS = [
    {"city": "Your City", "lat": 40.7128, "lon": -74.0060},
    # Add more locations...
]
```

### Customize Website Appearance

Edit `index.html` to modify:
- Colors (search for color codes like `#0066cc`)
- Layout and spacing
- Text and labels
- Add your own branding

## Technical Details

### Dependencies

- **Python 3.11+**
- **Selenium**: Web automation framework
- **Chrome/Chromium**: Headless browser
- **GitHub Actions**: Automated workflow execution

### Browser Compatibility

The website works on:
- Chrome, Firefox, Safari, Edge (desktop)
- iOS Safari, Chrome Mobile, Samsung Internet (mobile)
- Works with JavaScript disabled (displays all events)

### Performance

- **Page Load**: < 1 second (static HTML + JSON)
- **Search Time**: < 500ms (client-side filtering)
- **Data Size**: ~50-200KB (depending on number of events)
- **Bandwidth**: Minimal - no external dependencies except geocoding API

### Rate Limiting

- **Scraper**: 2-second delay between locations to be respectful
- **Geocoding**: Cached locally to minimize API calls
- **GitHub Actions**: 10-15 minute runtime per day

## Troubleshooting

### Events Not Loading

- Check that `events.json` exists in your repository
- Verify GitHub Pages is enabled and deployed
- Clear your browser cache

### Scraper Failing

- Go to Actions tab and check the workflow logs
- Common issues:
  - Website structure changed (need to update selectors)
  - Rate limiting (increase delays in scraper)
  - ChromeDriver version mismatch

### Search Not Working

- Ensure you have internet connection (required for geocoding)
- Try searching with different terms (full city name, state abbreviation, etc.)
- Check browser console for JavaScript errors

## Data Source

All event data is sourced directly from [events.pokemon.com](https://events.pokemon.com/EventLocator/Home), the official Pokemon events website.

## Privacy & Terms

- No user data is collected or stored
- No cookies or tracking
- Geocoding uses OpenStreetMap's Nominatim API (see their [usage policy](https://operations.osmfoundation.org/policies/nominatim/))
- This is an unofficial fan project, not affiliated with Pokemon or Nintendo

## Contributing

Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Fork and modify for your own use

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs for scraper issues
3. Open an issue on GitHub

---

**Note**: This tool is for informational purposes only. Always verify event details on the official Pokemon website before attending.
