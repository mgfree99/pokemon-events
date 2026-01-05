# Running the Scraper Locally - Complete Guide

## Why Run Locally?

The Pokemon website blocks GitHub Actions servers but typically allows regular home computers. Running the scraper on your computer bypasses this issue completely!

## One-Time Setup (5 minutes)

### Step 1: Install Prerequisites

**Windows:**
1. Install Python: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
   - Download the Windows installer and run it

**Mac:**
1. Python is usually pre-installed. Open Terminal and check:
   ```bash
   python3 --version
   ```
2. If not installed, get it from: https://www.python.org/downloads/

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip chromium-browser
```

### Step 2: Install Chrome Browser

If you don't have Chrome installed:
- Download from: https://www.google.com/chrome/

### Step 3: Clone Your Repository

**Using GitHub Desktop (Easiest):**
1. Install GitHub Desktop: https://desktop.github.com
2. File → Clone Repository
3. Select your `pokemon-events` repository
4. Choose a location on your computer
5. Click "Clone"

**Using Command Line:**
```bash
cd Documents  # or wherever you want it
git clone https://github.com/YOUR-USERNAME/pokemon-events.git
cd pokemon-events
```

### Step 4: Add the Local Scraper Files

1. Download the files from this package:
   - `scraper_local.py`
   - `RUN_SCRAPER.bat` (Windows) or `run_scraper.sh` (Mac/Linux)
   
2. Copy them into your cloned repository folder

## Running the Scraper

### Windows:
**Super Easy Method:**
- Just double-click `RUN_SCRAPER.bat`
- That's it!

**Manual Method:**
1. Open Command Prompt in the repository folder
2. Run: `python scraper_local.py`

### Mac/Linux:
**Easy Method:**
1. Open Terminal in the repository folder
2. Make script executable (first time only):
   ```bash
   chmod +x run_scraper.sh
   ```
3. Run:
   ```bash
   ./run_scraper.sh
   ```

**Manual Method:**
```bash
python3 scraper_local.py
```

## What to Expect

### During Scraping:
1. **Browser opens** - You'll see Chrome/Chromium open (this is normal!)
2. **Progress updates** - You'll see each city being scraped
3. **Takes 15-25 minutes** - It goes through 65 locations
4. **Browser closes** - Automatically when done

### Example Output:
```
🎮 POKEMON EVENTS SCRAPER - LOCAL VERSION
============================================================
Started: 2026-01-05 14:30:00
Locations: 65
============================================================

Starting Chrome browser...
(You'll see the browser window - this is normal!)
✓ Browser ready

[1/65] 📍 Seattle... ✓ 5 events
[2/65] 📍 Portland... ✓ 3 events
[3/65] 📍 San Francisco... ✓ 7 events
...

============================================================
✅ SCRAPING COMPLETE!
============================================================
✓ Scraped: 65/65 locations
✓ Found: 234 unique events
✓ Saved to: events.json
============================================================

Would you like to push these results to GitHub? (y/n): 
```

### After Scraping:
1. Type `y` to push to GitHub automatically
2. Or type `n` and push manually later
3. Your website updates in 1-2 minutes!

## Troubleshooting

### "Python not found"
- Windows: Make sure you checked "Add to PATH" during Python installation
- Mac/Linux: Try `python3` instead of `python`
- Reinstall Python if needed

### "Chrome not found" or "ChromeDriver error"
- Make sure Chrome browser is installed
- The script will auto-download ChromeDriver
- If issues persist, run: `pip install --upgrade selenium webdriver-manager`

### "Git push failed" or "Permission denied"
**Option 1 - Set up Git credentials:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Option 2 - Use GitHub Desktop:**
- GitHub Desktop handles authentication automatically
- Just open the app and click "Push origin"

**Option 3 - Generate a Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Check "repo" permissions
4. Copy the token
5. Use it as your password when pushing

### Browser closes immediately or errors
- The Pokemon website might still be blocking. Try:
  1. Wait a few hours and try again
  2. Try from a different internet connection
  3. Comment out the headless mode (line 82) to see what's happening

### "Events found but selectors need update"
If the Pokemon website changed its HTML structure:
1. Open an issue on your GitHub repo
2. I can help update the selectors
3. Or manually inspect the page and update the CSS selectors in the script

## Scheduling Regular Updates

### Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly (or whatever you prefer)
4. Action: Start a program
5. Program: `C:\path\to\RUN_SCRAPER.bat`
6. Save

### Mac (cron):
1. Open Terminal
2. Edit crontab: `crontab -e`
3. Add line:
   ```
   0 9 * * 0 cd /path/to/pokemon-events && python3 scraper_local.py
   ```
   (Runs every Sunday at 9 AM)
4. Save and exit

### Linux (cron):
Same as Mac instructions above.

## How Often Should You Run It?

**Recommended: Once per week**
- Pokemon events don't change that frequently
- Sunday evenings work well (before the week starts)
- You can always run it manually if you see new events posted

**For active seasons: Twice per week**
- Major tournament seasons have more updates
- Monday and Thursday are good days

## Data Usage & Time

- **Time per run**: 15-25 minutes
- **Internet usage**: ~5-10 MB
- **CPU usage**: Low (browser automation)
- **You can use your computer** while it runs (browser runs in background)

## Tips for Best Results

1. **Run from home internet** - Less likely to be blocked than public WiFi
2. **Don't run too frequently** - Once a week is plenty
3. **Let it complete** - Don't cancel mid-run
4. **Check GitHub** - Verify the push worked (check your repo)
5. **Test your website** - Visit it to see the new events

## Still Having Issues?

1. Check this README.md for more troubleshooting
2. Run `test_scraper.py` to diagnose issues
3. Create a GitHub issue with the error message
4. Make sure Chrome and Python are up to date

---

## Quick Reference Commands

**Install dependencies:**
```bash
pip install selenium webdriver-manager
```

**Run scraper:**
```bash
python scraper_local.py
```

**Manual GitHub push:**
```bash
git add events.json
git commit -m "Update events"
git push
```

**Check if it worked:**
Visit: `https://YOUR-USERNAME.github.io/pokemon-events/`

---

**That's it! You now have a fully automated Pokemon events website that updates from your home computer!** 🎉
