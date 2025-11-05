# Adobe Stock Upload Automation - Complete Workflow Guide

## Overview
This document details the complete workflow for automating Adobe Stock uploads using Python Playwright, based on successful testing with MCP Playwright tools.

## Workflow Summary

### 1. Authentication
- Navigate to: `https://contributor.stock.adobe.com/de/uploads?upload=1`
- Auth state can be saved to `adobe_auth_state.json` for session persistence
- Login is typically via Google OAuth (SSO)

### 2. Image Upload Process

**Key Discovery:** The file input element is hidden (`display: none`), requiring indirect interaction.

**Correct Approach:**
1. Click the "suchen" (browse) button to trigger file chooser modal
2. Use Playwright's `set_input_files()` on the hidden input element

**Selectors:**
```python
# Hidden file input (use for set_input_files)
file_input = 'input[type="file"][accept*="image"]'

# Browse button (use for triggering modal - if needed)
browse_button = 'button:has-text("suchen")'
```

**Upload Verification:**
- After upload, look for text: "Noch X Uploads…" (X uploads remaining)
- Then: "Dateitypen: Alle (X)" where X is the number of uploaded files

### 3. CSV Metadata Upload

**Selector:**
```python
csv_upload_button = 'button:has-text("CSV hochladen")'
```

**Process:**
1. Click CSV upload button
2. File chooser opens automatically
3. Upload CSV file with columns: `Filename`, `Title`, `Keywords`, `Category`
4. Wait for processing message: "Deine CSV-Datei wird verarbeitet"
5. Wait for completion (can take up to 15 minutes): "Daten aus deiner CSV-Datei wurden auf die zugehörigen Dateien angewendet"
6. Refresh page to see applied metadata

**CSV Format:**
```csv
Filename,Title,Keywords,Category
image1.jpg,AI Generated Abstract Digital Art 1,"ai generated, artificial intelligence, digital art, abstract, modern",19
```

### 4. Mark AI-Generated and Fictional People

**Critical Step:** Each uploaded image must be marked as AI-generated and have fictional people flagged.

**Approach 1: Individual Images (Safe)**
```python
# Get all thumbnails
thumbnails = page.query_selector_all('[role="option"]')

for thumbnail in thumbnails:
    # Click thumbnail to load form
    thumbnail.click()
    page.wait_for_timeout(500)

    # Check AI-generated checkbox
    ai_checkbox = page.locator('input[type="checkbox"]').filter(has_text="Mit generativen KI-Tools erstellt")
    if not ai_checkbox.is_checked():
        ai_checkbox.click()
        page.wait_for_timeout(300)

    # Check fictional people checkbox (appears after AI checkbox is checked)
    fictional_checkbox = page.locator('input[type="checkbox"]').filter(has_text="Menschen und Eigentum sind fiktiv")
    if fictional_checkbox.is_visible() and not fictional_checkbox.is_checked():
        fictional_checkbox.click()
        page.wait_for_timeout(300)
```

**Approach 2: Bulk via JavaScript (Faster)**
```python
page.evaluate("""
async () => {
    const thumbnails = document.querySelectorAll('[role="option"]');

    for (let i = 0; i < thumbnails.length; i++) {
        thumbnails[i].click();
        await new Promise(resolve => setTimeout(resolve, 500));

        const aiCheckbox = document.querySelector('input[type="checkbox"][aria-label*="generativen KI-Tools"]');
        if (aiCheckbox && !aiCheckbox.checked) {
            aiCheckbox.click();
            await new Promise(resolve => setTimeout(resolve, 300));
        }

        const fictionalCheckbox = document.querySelector('input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]');
        if (fictionalCheckbox && !fictionalCheckbox.checked) {
            fictionalCheckbox.click();
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }
}
""")
```

### 5. Verification (DO NOT AUTO-SUBMIT)

**Important:** Never auto-click the submit button. Let user verify manually.

The submit button shows: "20 Dateien einreichen" (Submit 20 files)

## Bot Detection Prevention

### Playwright Configuration

```python
from playwright.sync_api import sync_playwright
import random

def create_browser_context():
    playwright = sync_playwright().start()

    # Launch browser with anti-detection settings
    browser = playwright.chromium.launch(
        headless=False,  # Use False for production to avoid headless detection
        args=[
            '--disable-blink-features=AutomationControlled',  # Remove webdriver flag
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--window-position=0,0',
            '--ignore-certificate-errors',
            '--ignore-certificate-errors-spki-list',
            '--disable-blink-features=AutomationControlled'
        ]
    )

    # Create context with realistic fingerprint
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        locale='de-DE',
        timezone_id='Europe/Berlin',
        permissions=['geolocation'],
        geolocation={'latitude': 52.520008, 'longitude': 13.404954},  # Berlin
        color_scheme='light',
        accept_downloads=True,
        storage_state='adobe_auth_state.json' if os.path.exists('adobe_auth_state.json') else None
    )

    # Remove webdriver detection
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Override the plugins to avoid detection
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        // Override languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['de-DE', 'de', 'en-US', 'en']
        });

        // Chrome runtime
        window.chrome = {
            runtime: {}
        };

        // Permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    """)

    return playwright, browser, context
```

### Human-like Behavior

```python
import time
import random

def human_delay(min_ms=100, max_ms=500):
    """Random delay to simulate human behavior"""
    time.sleep(random.uniform(min_ms/1000, max_ms/1000))

def human_type(page, selector, text):
    """Type text with human-like delays"""
    element = page.locator(selector)
    element.click()
    human_delay(200, 400)

    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.05, 0.15))

def human_click(page, selector):
    """Click with human-like delay"""
    human_delay(300, 700)
    page.locator(selector).click()
    human_delay(200, 500)
```

### Mouse Movement Simulation

```python
def move_mouse_to_element(page, selector):
    """Move mouse to element before clicking"""
    element = page.locator(selector)
    box = element.bounding_box()

    if box:
        # Move to random point within element
        x = box['x'] + random.uniform(5, box['width'] - 5)
        y = box['y'] + random.uniform(5, box['height'] - 5)

        page.mouse.move(x, y)
        human_delay(100, 300)
        page.mouse.click(x, y)
```

## Complete Python Implementation

```python
import os
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

class AdobeStockAutomation:
    def __init__(self, headless=False, auth_state_file='adobe_auth_state.json'):
        self.headless = headless
        self.auth_state_file = auth_state_file
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        """Initialize Playwright with anti-detection"""
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )

        storage_state = self.auth_state_file if os.path.exists(self.auth_state_file) else None

        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='de-DE',
            timezone_id='Europe/Berlin',
            storage_state=storage_state,
            accept_downloads=True
        )

        # Anti-detection script
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = { runtime: {} };
        """)

        self.page = self.context.new_page()

    def close(self):
        """Cleanup resources"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def save_auth_state(self):
        """Save authentication state"""
        self.context.storage_state(path=self.auth_state_file)
        print(f"✅ Auth state saved to {self.auth_state_file}")

    def navigate_to_upload_page(self):
        """Navigate to Adobe Stock upload page"""
        print("📄 Navigating to upload page...")
        self.page.goto('https://contributor.stock.adobe.com/de/uploads?upload=1',
                       wait_until='networkidle', timeout=60000)
        time.sleep(random.uniform(1, 2))

    def upload_images(self, image_paths):
        """Upload multiple images"""
        print(f"📤 Uploading {len(image_paths)} images...")

        # Find hidden file input
        file_input = self.page.locator('input[type="file"][accept*="image"]')

        # Set files on the input element
        file_input.set_input_files(image_paths)

        # Wait for upload to complete
        print("⏳ Waiting for upload to complete...")
        time.sleep(3)

        # Verify upload
        try:
            self.page.wait_for_selector(f'text=Dateitypen: Alle ({len(image_paths)})', timeout=30000)
            print(f"✅ Successfully uploaded {len(image_paths)} images")
            return True
        except:
            print("❌ Upload verification failed")
            return False

    def upload_csv(self, csv_path):
        """Upload CSV metadata file"""
        print(f"📊 Uploading CSV metadata: {csv_path}")

        # Click CSV upload button
        csv_button = self.page.locator('button:has-text("CSV hochladen")')
        csv_button.click()

        # Wait for file chooser and upload
        time.sleep(1)

        # Find file input for CSV
        with self.page.expect_file_chooser() as fc_info:
            csv_button.click()

        file_chooser = fc_info.value
        file_chooser.set_files(csv_path)

        # Wait for processing message
        print("⏳ Waiting for CSV processing...")
        try:
            self.page.wait_for_selector('text=Deine CSV-Datei wird verarbeitet', timeout=10000)
            print("📝 CSV file is being processed...")

            # Wait for completion (can take up to 15 minutes)
            self.page.wait_for_selector('text=Daten aus deiner CSV-Datei wurden auf die zugehörigen Dateien angewendet',
                                       timeout=900000)  # 15 minutes
            print("✅ CSV metadata applied successfully")

            # Refresh to see changes
            time.sleep(2)
            self.page.reload(wait_until='networkidle')
            return True
        except:
            print("❌ CSV upload/processing failed or timed out")
            return False

    def mark_ai_generated_and_fictional(self, num_images):
        """Mark all images as AI-generated with fictional people"""
        print(f"🤖 Marking {num_images} images as AI-generated and fictional...")

        # Use JavaScript for bulk operation
        result = self.page.evaluate(f"""
        async () => {{
            const thumbnails = document.querySelectorAll('[role="option"]');
            let processed = 0;

            for (let i = 0; i < thumbnails.length; i++) {{
                thumbnails[i].click();
                await new Promise(resolve => setTimeout(resolve, 500));

                // Check AI-generated checkbox
                const aiCheckbox = document.querySelector('input[type="checkbox"][aria-label*="generativen KI-Tools"]');
                if (aiCheckbox && !aiCheckbox.checked) {{
                    aiCheckbox.click();
                    await new Promise(resolve => setTimeout(resolve, 300));
                }}

                // Check fictional people checkbox
                const fictionalCheckbox = document.querySelector('input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]');
                if (fictionalCheckbox && !fictionalCheckbox.checked) {{
                    fictionalCheckbox.click();
                    await new Promise(resolve => setTimeout(resolve, 300));
                }}

                processed++;
            }}

            return {{ processed: processed, total: thumbnails.length }};
        }}
        """)

        print(f"✅ Marked {result['processed']}/{result['total']} images")
        return result['processed'] == num_images

    def run_full_upload(self, image_dir, csv_path):
        """Run complete upload workflow"""
        print("="*60)
        print("🚀 Adobe Stock Upload Automation")
        print("="*60)

        # Get image files
        image_paths = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']:
            image_paths.extend(Path(image_dir).glob(ext))

        image_paths = [str(p) for p in sorted(image_paths)]

        if not image_paths:
            print("❌ No images found in directory")
            return False

        print(f"📁 Found {len(image_paths)} images")

        # Step 1: Navigate
        self.navigate_to_upload_page()

        # Step 2: Upload images
        if not self.upload_images(image_paths):
            return False

        # Step 3: Upload CSV
        if not self.upload_csv(csv_path):
            return False

        # Step 4: Mark AI-generated and fictional
        if not self.mark_ai_generated_and_fictional(len(image_paths)):
            return False

        print("="*60)
        print("✅ Upload complete! Ready for manual verification.")
        print("⚠️  DO NOT auto-submit - user should verify manually")
        print("="*60)

        return True

# Usage example
if __name__ == '__main__':
    with AdobeStockAutomation(headless=False) as automation:
        automation.run_full_upload(
            image_dir='/home/burak/drive/Gallery/AIGenerated/upscaled',
            csv_path='/home/burak/docker/n8n/python/test_metadata.csv'
        )
```

## Key Selectors Reference

| Element | Selector | Notes |
|---------|----------|-------|
| File Input (Images) | `input[type="file"][accept*="image"]` | Hidden element |
| Browse Button | `button:has-text("suchen")` | Triggers file chooser |
| CSV Upload Button | `button:has-text("CSV hochladen")` | Opens CSV file chooser |
| Image Thumbnails | `[role="option"]` | All uploaded images |
| AI-Generated Checkbox | `input[type="checkbox"][aria-label*="generativen KI-Tools"]` | Must check this |
| Fictional People Checkbox | `input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]` | Appears after AI checkbox |
| Submit Button | `button:has-text("Dateien einreichen")` | DO NOT AUTO-CLICK |

## Timing Recommendations

- **Image Upload:** Wait 3-5 seconds after `set_input_files()`
- **CSV Processing:** Can take 10 seconds to 15 minutes
- **Between Thumbnail Clicks:** 500ms
- **After Checkbox Click:** 300ms
- **Page Loads:** Use `wait_until='networkidle'`

## Error Handling

```python
# Retry decorator
def retry(max_attempts=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3)
def upload_with_retry(automation, image_paths):
    return automation.upload_images(image_paths)
```

## Testing Checklist

- [ ] Auth state persists across sessions
- [ ] Images upload successfully (verify count)
- [ ] CSV metadata applies (check titles/keywords)
- [ ] All AI-generated checkboxes are checked
- [ ] All fictional people checkboxes are checked
- [ ] No bot detection warnings
- [ ] Ready for manual submission (DO NOT auto-submit)

## Performance Notes

- **20 images:** ~2-3 minutes total (excluding CSV processing time)
- **CSV processing:** 10 seconds - 15 minutes (Adobe backend dependent)
- **Checkbox marking:** ~10-15 seconds for 20 images with JavaScript approach

## Security Considerations

1. **Never commit `adobe_auth_state.json`** - Add to `.gitignore`
2. **Use environment variables** for credentials if implementing login automation
3. **Rate limiting:** Add delays between operations
4. **Session persistence:** Reuse auth state to avoid repeated logins

## Next Steps

- [ ] Implement for other platforms (Freepik, Wirestock, Dreamstime)
- [ ] Add retry logic for network failures
- [ ] Add logging for debugging
- [ ] Create monitoring/alerting for failed uploads
- [ ] Add support for video uploads
