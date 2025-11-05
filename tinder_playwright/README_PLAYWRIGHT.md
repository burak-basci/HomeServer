# Tinder Bot - Playwright Version

This is a refactored version of the Tinder bot that uses **Playwright** instead of Selenium for browser automation.

## What Changed?

This version has been completely refactored from Selenium to Playwright, providing several benefits:

### Why Playwright?

1. **Better Performance**: Playwright is faster and more reliable than Selenium
2. **Modern API**: Cleaner, more intuitive API for browser automation
3. **Built-in Waiting**: Smart auto-waiting for elements reduces flakiness
4. **Better Debugging**: Superior debugging capabilities with tracing and screenshots
5. **No ChromeDriver Issues**: No need to manage ChromeDriver versions separately
6. **Cross-browser Support**: Works with Chromium, Firefox, and WebKit

### Key Technical Changes

- **Browser Automation**: Replaced Selenium WebDriver with Playwright's Browser/Page API
- **Element Selection**: Modern locator API instead of `find_element(By.XPATH)`
- **Waiting Strategy**: Built-in smart waiting instead of explicit `WebDriverWait`
- **Keyboard Actions**: Direct keyboard API instead of ActionChains
- **Session Management**: Browser context with storage state for persistence

## Installation

1. **Install Python Dependencies**:
```bash
cd tinder_playwright
pip install -r requirements.txt
```

2. **Install Playwright Browsers**:
```bash
playwright install chromium
```

This will download the Chromium browser that Playwright will use.

## Usage

The usage is identical to the original version:

```bash
python daily_swipe.py <manual_login> <likes> <ratio> <sleep> <change_settings> [<latitude> <longitude> <distance_km>]
```

### Example:

```bash
# Automated login with 50 likes
python daily_swipe.py False 50 100% 2 False

# Manual login with 30 likes at 80% ratio
python daily_swipe.py True 30 80% 3 False

# With custom location
python daily_swipe.py False 50 100% 2 True 40.7128 -74.0060 50
```

### Parameters:

- `manual_login`: `True` to log in manually, `False` to use credentials from `.env`
- `likes`: Number of profiles to like
- `ratio`: Percentage of likes vs dislikes (e.g., `80%`)
- `sleep`: Base sleep time between actions (in seconds)
- `change_settings`: `True` to apply custom location/distance settings
- `latitude`: (Optional) Custom latitude
- `longitude`: (Optional) Custom longitude
- `distance_km`: (Optional) Maximum distance in kilometers

## Configuration

Create a `.env` file in the project root:

```env
TINDER_EMAIL=your.email@example.com
TINDER_PASSWORD=your_password
CHROME_BINARY=/path/to/chrome  # Optional, not used by Playwright
```

## Features

All original features are supported:

- ✅ Automated swiping (like/dislike/superlike)
- ✅ Login via Google, Facebook, or SMS
- ✅ Custom geolocation
- ✅ Profile scraping
- ✅ Match management
- ✅ Messaging
- ✅ Session persistence
- ✅ Popup handling

## Differences from Selenium Version

### API Changes

**Browser/Page Management**:
```python
# Selenium
session.browser.get("https://tinder.com")
session.browser.find_element(By.XPATH, xpath)

# Playwright
session.page.goto("https://tinder.com")
session.page.locator(xpath)
```

**Element Interaction**:
```python
# Selenium
element.send_keys("text")
element.send_keys(Keys.ENTER)

# Playwright
element.fill("text")
element.press("Enter")
```

**Waiting**:
```python
# Selenium
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)

# Playwright
page.wait_for_selector(xpath, timeout=10000)
```

### Session Persistence

Playwright uses a different approach for session persistence:
- Uses browser context with storage state
- Saves cookies and local storage to a JSON file
- More reliable than Selenium's user-data-dir approach

### Performance

Expect significantly better performance:
- Faster page loads
- More reliable element detection
- Fewer timeout errors
- Better handling of dynamic content

## Troubleshooting

### Common Issues

**1. Playwright not found**
```bash
pip install playwright
playwright install chromium
```

**2. Browser won't launch**
- Make sure Chromium is installed: `playwright install chromium`
- Check if running in headless mode on systems without display

**3. Login fails**
- Increase delay timeouts in helper files
- Try manual login mode first
- Check if Tinder has updated their UI

**4. Elements not found**
- Tinder's UI may have changed
- Check if XPaths in `helpers/xpaths.py` are still valid
- Try running in non-headless mode to debug

### Debugging

Run in non-headless mode to see what's happening:
```bash
python daily_swipe.py True 10 100% 2 False
```

Enable Playwright's debug mode:
```bash
PWDEBUG=1 python daily_swipe.py True 10 100% 2 False
```

## Migration from Original Version

If you're migrating from the Selenium version:

1. **Session Data**: Copy your `chrome_profile` directory
2. **Configuration**: Your `.env` file works as-is
3. **Scripts**: Update any custom scripts to use `session.page` instead of `session.browser`

## Project Structure

```
tinder_playwright/
├── daily_swipe.py              # Main entry point
├── requirements.txt            # Python dependencies (Playwright)
├── tinderbotj/
│   ├── session.py             # Session management (Playwright)
│   └── helpers/
│       ├── login_helper.py    # Login handlers (Playwright)
│       ├── geomatch_helper.py # Profile interaction (Playwright)
│       ├── match_helper.py    # Match management (Playwright)
│       ├── preferences_helper.py  # Settings (Playwright)
│       ├── profile_helper.py  # Profile editing (Playwright)
│       └── ...
└── chrome_profile/            # Session storage
```

## Contributing

This is a refactored version. If you find bugs or want to contribute:
1. Test your changes thoroughly
2. Ensure all features work
3. Update documentation if needed

## Credits

- Original Selenium version: [tinderbotj](https://github.com/frederikme/tinderbotj)
- Refactored to Playwright by Claude Code

## License

Same as the original project. See LICENSE.txt.

## Disclaimer

This bot is for educational purposes only. Using automated tools may violate Tinder's Terms of Service. Use at your own risk.
