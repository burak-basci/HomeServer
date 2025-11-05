import os
import time
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError as PlaywrightTimeoutError


class AdobeStockPlaywrightAPI:
    """Playwright-based automation for Adobe Stock upload workflows.

    This helper automates the following Adobe Stock contributor operations:
    - login (if credentials provided via environment)
    - upload a batch of images
    - upload CSV metadata
    - mark items as AI generated and fictional human
    - release the assets

    NOTE: Adobe Stock web UI changes frequently. Selectors here are best-effort
    and may need adjustments.
    """

    def __init__(self, download_dir=None, headless=True, profile_dir=None, debugger_address=None, auth_state_file=None):
        """Initialize the Playwright browser instance.

        Args:
            download_dir: Directory for downloads
            headless: Run browser in headless mode
            profile_dir: Chrome user profile directory (not used with debugger_address or auth_state_file)
            debugger_address: Connect to existing Chrome DevTools endpoint (e.g., "localhost:9222")
            auth_state_file: Path to authentication state JSON file for session persistence
        """
        self.playwright = sync_playwright().start()
        self.download_dir = download_dir or os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        self.debugger_address = debugger_address
        self.auth_state_file = auth_state_file

        # Configure browser launch options
        if debugger_address:
            # Connect to existing Chrome instance
            self.browser = self.playwright.chromium.connect_over_cdp(f"http://{debugger_address}")
            self.context = self.browser.contexts[0] if self.browser.contexts else self.browser.new_context()
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        else:
            # Launch new browser with anti-detection settings
            launch_options = {
                "headless": headless,
                "args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",  # Remove webdriver flag
                    "--disable-infobars",
                    "--disable-features=IsolateOrigins,site-per-process",
                ],
            }

            # Use persistent context if profile_dir is specified
            if profile_dir:
                self.context = self.playwright.chromium.launch_persistent_context(
                    profile_dir,
                    **launch_options,
                    viewport={"width": 1920, "height": 1080},
                    accept_downloads=True,
                    downloads_path=self.download_dir,
                    user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    locale='de-DE',
                    timezone_id='Europe/Berlin',
                )
                self.browser = None
                self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
            else:
                # Load auth state if provided
                storage_state = None
                if auth_state_file and os.path.exists(auth_state_file):
                    storage_state = auth_state_file
                    print(f"Loading authentication state from {auth_state_file}")

                self.browser = self.playwright.chromium.launch(**launch_options)
                self.context = self.browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    accept_downloads=True,
                    storage_state=storage_state,
                    user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    locale='de-DE',
                    timezone_id='Europe/Berlin',
                )
                self.page = self.context.new_page()

        # Add anti-detection script
        self.context.add_init_script("""
            // Remove webdriver detection
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Override plugins
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

        # Set default timeout
        self.page.set_default_timeout(30000)

    def login(self, username=None, password=None):
        """Log in to Adobe Stock.

        If username/password are not provided, assumes already logged in via SSO or cookies.
        """
        if not username or not password:
            return

        self.page.goto("https://stock.adobe.com/")

        # Click sign in link
        try:
            sign_in = self.page.get_by_role("link", name="Sign in")
            if sign_in.is_visible():
                sign_in.click()
        except Exception:
            pass

        # Basic username/password flow
        try:
            # Enter email
            email_input = self.page.locator("input[name='email']").first
            email_input.wait_for(state="visible", timeout=10000)
            email_input.fill(username)
            email_input.press("Enter")

            # Enter password
            pwd_input = self.page.locator("input[name='password']").first
            pwd_input.wait_for(state="visible", timeout=10000)
            pwd_input.fill(password)
            pwd_input.press("Enter")

            # Wait for navigation to complete
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            # Some Adobe flows use federated login; leave to manual login
            time.sleep(5)

    def open_contributor_portal(self):
        """Navigate to the Adobe Stock contributor portal."""
        self.page.goto("https://contributor.stock.adobe.com/")
        self.page.wait_for_load_state("networkidle")

    def upload_images(self, images_dir):
        """Upload all images from images_dir via the contributor portal.

        Args:
            images_dir: Directory containing image files to upload

        Returns when the upload step completes and thumbnails are visible.
        """
        # Navigate directly to upload page (works in any language)
        print("   Navigating to upload page...")
        self.page.goto("https://contributor.stock.adobe.com/uploads?upload=1", timeout=60000, wait_until="domcontentloaded")
        time.sleep(3)  # Give page time to fully load

        # Prepare files list
        files = []
        for name in os.listdir(images_dir):
            path = os.path.join(images_dir, name)
            if os.path.isfile(path) and name.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
                files.append(os.path.abspath(path))

        if not files:
            raise RuntimeError(f"No image files found in {images_dir}")

        print(f"   Preparing to upload {len(files)} images...")

        # Find file input - should be present on upload page
        try:
            file_inputs = self.page.locator("input[type='file'][accept*='image']").all()
            if not file_inputs:
                raise RuntimeError("No file input found on upload page")

            # Use first file input
            print("   Uploading files...")
            file_inputs[0].set_input_files(files)
            print(f"   ✓ {len(files)} files sent to browser")

        except Exception as e:
            raise RuntimeError(f"Failed to upload files: {str(e)}")

        # Wait for upload to start processing
        print("   Waiting for uploads to process...")
        time.sleep(5)

        # Verify upload succeeded by checking for the file type indicator
        # This shows "Dateitypen: Alle (X)" where X is the number of uploaded files
        try:
            # Wait for the indicator that shows uploaded files
            # German: "Dateitypen: Alle (20)" or similar
            self.page.wait_for_selector(f"text=/Dateitypen.*{len(files)}/", timeout=60000)
            print(f"   ✓ Upload verified: {len(files)} files uploaded successfully")
        except Exception as e:
            print(f"   ⚠ WARNING: Could not verify upload completion: {e}")
            print("   Waiting additional 30 seconds...")
            time.sleep(30)

    def upload_csv(self, csv_path):
        """Upload CSV metadata file.

        Args:
            csv_path: Path to the CSV file containing metadata
        """
        csv_path = os.path.abspath(csv_path)
        print("   Looking for CSV upload button...")

        try:
            # Click CSV upload button (works in any language)
            # Look for button with text containing "CSV"
            csv_buttons = self.page.get_by_role("button").all()
            csv_button = None

            for btn in csv_buttons:
                text = btn.inner_text().lower()
                if 'csv' in text:
                    csv_button = btn
                    print(f"   Found CSV button: {btn.inner_text()}")
                    break

            if csv_button:
                csv_button.click()
                time.sleep(1)

            # Look for CSV file input (might appear after clicking button)
            csv_inputs = self.page.locator("input[type='file']").all()
            if csv_inputs:
                print(f"   Uploading CSV file...")
                # Try each input until one accepts the CSV
                for inp in csv_inputs:
                    try:
                        inp.set_input_files(csv_path)
                        print(f"   ✓ CSV uploaded")
                        break
                    except Exception:
                        continue
            else:
                print("   WARNING: No file input found for CSV, skipping...")

        except Exception as e:
            print(f"   WARNING: CSV upload failed: {e}")
            print("   You may need to upload CSV manually")

        # Wait for CSV processing
        time.sleep(5)

    def mark_ai_and_fictional(self):
        """Mark all uploaded assets as AI-generated and all people as fictional.

        This uses JavaScript to iterate through all thumbnails and check the appropriate
        checkboxes. Based on verified MCP testing workflow.
        """
        print("   Marking all images as AI-generated with fictional people...")

        # Use JavaScript to efficiently process all images
        result = self.page.evaluate("""
        async () => {
            const thumbnails = document.querySelectorAll('[role="option"]');
            let processed = 0;
            let errors = [];

            for (let i = 0; i < thumbnails.length; i++) {
                try {
                    // Click thumbnail to load its form
                    thumbnails[i].click();
                    await new Promise(resolve => setTimeout(resolve, 500));

                    // Find and check AI-generated checkbox
                    const aiCheckbox = document.querySelector('input[type="checkbox"][aria-label*="generativen KI-Tools"]') ||
                                      document.querySelector('input[type="checkbox"][aria-label*="AI generated"]') ||
                                      document.querySelector('input[type="checkbox"][aria-label*="generative AI"]');

                    if (aiCheckbox && !aiCheckbox.checked) {
                        aiCheckbox.click();
                        await new Promise(resolve => setTimeout(resolve, 300));
                    }

                    // Find and check fictional people checkbox (appears after AI checkbox)
                    const fictionalCheckbox = document.querySelector('input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]') ||
                                             document.querySelector('input[type="checkbox"][aria-label*="fictional"]') ||
                                             document.querySelector('input[type="checkbox"][aria-label*="ficticio"]');

                    if (fictionalCheckbox && !fictionalCheckbox.checked) {
                        fictionalCheckbox.click();
                        await new Promise(resolve => setTimeout(resolve, 300));
                    }

                    processed++;
                } catch (err) {
                    errors.push(`Image ${i}: ${err.message}`);
                }
            }

            return {
                processed: processed,
                total: thumbnails.length,
                errors: errors
            };
        }
        """)

        print(f"   ✓ Processed {result['processed']}/{result['total']} images")

        if result.get('errors'):
            print(f"   ⚠ Encountered {len(result['errors'])} errors:")
            for error in result['errors'][:5]:  # Show first 5 errors
                print(f"     - {error}")

        return result['processed'] == result['total']

    def _ensure_checked(self, checkbox_locator):
        """Ensure a checkbox is checked.

        Args:
            checkbox_locator: Playwright locator for the checkbox element
        """
        try:
            if not checkbox_locator.is_checked():
                checkbox_locator.check()
        except Exception:
            # Try clicking if check() doesn't work
            try:
                checkbox_locator.click()
            except Exception:
                pass

    def release_all(self):
        """Submit all assets for review by clicking the release/submit button."""
        try:
            # Try multiple button text variations
            button_texts = ["Submit", "Release", "Send for review", "Submit for review"]

            submit_button = None
            for text in button_texts:
                try:
                    submit_button = self.page.get_by_role("button", name=text, exact=False)
                    if submit_button.is_visible():
                        break
                except Exception:
                    continue

            if not submit_button or not submit_button.is_visible():
                raise RuntimeError("Could not find submit/release button")

            submit_button.click()
            time.sleep(2)
        except Exception as e:
            raise RuntimeError(f"Could not find or click submit/release button: {str(e)}")

    def save_auth_state(self, auth_state_file=None):
        """Save the current authentication state (cookies, localStorage, etc.) to a file.

        This allows you to reuse the login session in future runs without logging in again.

        Args:
            auth_state_file: Path to save the auth state JSON file (defaults to self.auth_state_file)
        """
        save_path = auth_state_file or self.auth_state_file
        if not save_path:
            raise ValueError("auth_state_file must be provided either in __init__ or save_auth_state()")

        try:
            self.context.storage_state(path=save_path)
            print(f"✓ Authentication state saved to {save_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to save authentication state: {str(e)}")

    def close(self):
        """Close the browser and cleanup resources."""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            self.playwright.stop()
        except Exception:
            pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
