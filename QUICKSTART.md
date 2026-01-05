# Quick Start Guide

This guide will get your Pokemon Events Locator up and running in 10 minutes.

## Step-by-Step Setup

### 1. Create GitHub Account (if needed)
- Go to https://github.com
- Sign up for free

### 2. Create New Repository
1. Click the **+** icon in top right
2. Select **New repository**
3. Repository name: `pokemon-events`
4. Select **Public**
5. Check **Add a README file**
6. Click **Create repository**

### 3. Upload Files

**Option A: Via Web Interface**
1. Click **Add file** → **Upload files**
2. Drag and drop all files from this folder:
   - index.html
   - events.json
   - scraper.py
   - requirements.txt
   - README.md
   - .gitignore
3. Create folder structure for GitHub Actions:
   - Click **Add file** → **Create new file**
   - Type: `.github/workflows/update-events.yml`
   - Paste content from update-events.yml
   - Click **Commit new file**

**Option B: Via Git Command Line**
```bash
# Clone your new repository
git clone https://github.com/YOUR-USERNAME/pokemon-events.git
cd pokemon-events

# Copy all files into this directory
cp -r /path/to/downloaded/files/* .

# Add, commit, and push
git add .
git commit -m "Initial commit"
git push
```

### 4. Enable GitHub Pages
1. Go to repository **Settings**
2. Click **Pages** in left sidebar
3. Under **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 1-2 minutes
6. Your site will be at: `https://YOUR-USERNAME.github.io/pokemon-events/`

### 5. Run First Scrape
1. Go to **Actions** tab
2. Click **Update Pokemon Events**
3. Click **Run workflow** dropdown
4. Click green **Run workflow** button
5. Wait 10-15 minutes for completion
6. Check the workflow run for any errors

### 6. Test Your Site
1. Visit `https://YOUR-USERNAME.github.io/pokemon-events/`
2. Try searching for your city
3. Verify events are displayed

## Verification Checklist

- [ ] Repository is created and public
- [ ] All files are uploaded
- [ ] GitHub Pages is enabled
- [ ] Workflow has run successfully
- [ ] events.json contains data
- [ ] Website loads and displays events
- [ ] Search functionality works

## Common Issues

### "Page Not Found" Error
- Wait 5 minutes after enabling GitHub Pages
- Verify repository is public
- Check Settings → Pages shows the site URL

### No Events Showing
- Run the workflow manually from Actions tab
- Wait for workflow to complete
- Refresh the website page
- Check events.json has been updated

### Workflow Failing
- Click on the failed workflow run
- Read the error messages
- Most common: Website structure changed or rate limiting
- Try running again after a few hours

## Daily Updates

The scraper automatically runs every day at 6 AM UTC. You can:
- Check the Actions tab to see recent runs
- Manually trigger a run anytime
- Adjust the schedule in `.github/workflows/update-events.yml`

## Need Help?

1. Check the full README.md for detailed instructions
2. Review GitHub Actions logs for errors
3. Test locally with: `python test_scraper.py`
4. Create an issue on GitHub

## What's Next?

### Customization Ideas
- Change color scheme in index.html
- Add your own logo/branding
- Modify search radius options
- Add more search locations in scraper.py

### Advanced Features
- Add email notifications for new events
- Create an event calendar view
- Add filtering by event type
- Export events to CSV

---

**Congratulations!** Your Pokemon Events Locator is now live! 🎉

Visit your site at: `https://YOUR-USERNAME.github.io/pokemon-events/`
