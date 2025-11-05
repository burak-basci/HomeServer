import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class AdobeStockSeleniumAPI:
    """Minimal Selenium helper for automating Adobe Stock upload flows.

    This helper is intentionally small and focused on the operations you requested:
    - login (if credentials provided via environment)
    - upload a batch of images
    - upload CSV metadata
    - mark items as AI generated and fictional human
    - release the assets

    NOTE: Adobe Stock web UI changes frequently. Selectors here are best-effort
    and may need adjustments.
    """

    def __init__(self, download_dir=None, chromedriver_path=None, headless=True, profile_dir=None, debugger_address=None):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1400,1000")
        # If a profile dir is provided, reuse it so existing cookies/sessions are used
        # but prefer attaching to an existing browser via debugger_address to avoid
        # user-data-dir locking issues.
        self.debugger_address = debugger_address
        if profile_dir and not debugger_address:
            try:
                chrome_options.add_argument(f"--user-data-dir={profile_dir}")
            except Exception:
                pass

        # Use webdriver-manager to install a matching chromedriver when possible
        try:
            # If debugger_address is provided, attach to that running browser instead of
            # launching a new one. We still need a matching chromedriver binary.
            driver_path = None
            if chromedriver_path and os.path.exists(chromedriver_path):
                driver_path = chromedriver_path

            if self.debugger_address:
                # try to detect browser version from devtools endpoint
                try:
                    import urllib.request, json
                    host, port = self.debugger_address.split(":") if ":" in self.debugger_address else (self.debugger_address, '9222')
                    url = f"http://{host}:{port}/json/version"
                    data = urllib.request.urlopen(url, timeout=2).read()
                    info = json.loads(data)
                    browser = info.get('Browser', '')
                    if browser.startswith('Chrome/'):
                        browser_ver = browser.split('/', 1)[1]
                    else:
                        browser_ver = browser
                    # try to install matching chromedriver if we don't have one
                    if not driver_path:
                        driver_path = ChromeDriverManager(browser_ver).install()
                except Exception:
                    # fallback to default manager install
                    if not driver_path:
                        driver_path = ChromeDriverManager().install()

                service = Service(driver_path) if driver_path else None
                chrome_options.debugger_address = self.debugger_address
                if service:
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    self.driver = webdriver.Chrome(options=chrome_options)
            else:
                if not driver_path:
                    driver_path = ChromeDriverManager().install()
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            # fallback: try to create Chrome without service
            self.driver = webdriver.Chrome(options=chrome_options)

        self.wait = WebDriverWait(self.driver, 30)

    def login(self, username=None, password=None):
        # If username/password are not provided, assume already logged in (SSO / cookie mount)
        if not username or not password:
            return

        self.driver.get("https://stock.adobe.com/")
        # click sign in
        try:
            sign_in = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
            sign_in.click()
        except Exception:
            pass

        # Basic username/password flow
        try:
            email = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email.clear()
            email.send_keys(username)
            email.submit()
            pwd = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            pwd.clear()
            pwd.send_keys(password)
            pwd.submit()
        except Exception:
            # Some Adobe flows use federated login; leave to manual login.
            time.sleep(5)

    def open_contributor_portal(self):
        self.driver.get("https://contributor.stock.adobe.com/")
        # wait for upload button to be present
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def upload_images(self, images_dir):
        """Upload all images from images_dir via the contributor portal.

        Returns when the upload step completes and thumbnails are visible.
        """
        self.open_contributor_portal()

        # Try to find upload input
        try:
            upload_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        except Exception:
            # If there is a specific upload button that opens a dialog, click it then find input
            try:
                upload_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Upload')]")))
                upload_button.click()
                upload_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            except Exception as e:
                raise RuntimeError("Upload input not found: " + str(e))

        # prepare files list
        files = []
        for name in os.listdir(images_dir):
            path = os.path.join(images_dir, name)
            if os.path.isfile(path) and name.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
                files.append(path)

        if not files:
            raise RuntimeError("No image files found in " + images_dir)

        # send files
        upload_input.send_keys('\n'.join(files))

        # Wait until thumbnails or file rows appear
        time.sleep(3)
        # Best-effort wait for progress to finish
        for _ in range(60):
            try:
                # look for any element that indicates upload complete, e.g., thumbnail img
                thumbs = self.driver.find_elements(By.CSS_SELECTOR, "img[class*='thumbnail'], .uploaded-file")
                if thumbs and len(thumbs) >= len(files):
                    break
            except Exception:
                pass
            time.sleep(1)

    def upload_csv(self, csv_path):
        """Upload CSV metadata. Expects a CSV upload input on the page."""
        # try to find CSV upload field
        try:
            csv_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept='.csv']")))
            csv_input.send_keys(csv_path)
        except Exception:
            # try generic file input and send
            try:
                generic = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                generic.send_keys(csv_path)
            except Exception as e:
                raise RuntimeError("CSV upload input not found: " + str(e))

        # wait briefly for processing
        time.sleep(3)

    def mark_ai_and_fictional(self):
        """Click the 'is AI generated' and 'all humans fictional' checkboxes for each asset.

        This is best-effort and uses selector heuristics. Adjust as needed.
        """
        # find rows representing uploaded items
        rows = self.driver.find_elements(By.CSS_SELECTOR, ".asset-row, .upload-row, [data-test='asset-row']")
        if not rows:
            # fallback: find checkboxes on page
            rows = [self.driver]

        for row in rows:
            try:
                # AI generated checkbox
                ai_checkbox = row.find_element(By.XPATH, ".//label[contains(translate(., 'AI', 'ai'), 'ai') or contains(., 'AI generated')]/preceding-sibling::input[1]")
                self._ensure_checked(ai_checkbox)
            except Exception:
                # try by id or aria-label
                try:
                    ai_checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox'][aria-label*='AI']")
                    self._ensure_checked(ai_checkbox)
                except Exception:
                    pass

            try:
                fictional_checkbox = row.find_element(By.XPATH, ".//label[contains(., 'All people depicted are fictional')]/preceding-sibling::input[1]")
                self._ensure_checked(fictional_checkbox)
            except Exception:
                try:
                    fictional_checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox'][aria-label*='fictional']")
                    self._ensure_checked(fictional_checkbox)
                except Exception:
                    pass

    def _ensure_checked(self, checkbox_element):
        try:
            is_selected = checkbox_element.is_selected()
            if not is_selected:
                checkbox_element.click()
        except Exception:
            # try click via JS
            try:
                self.driver.execute_script("arguments[0].click();", checkbox_element)
            except Exception:
                pass

    def release_all(self):
        """Click the release/submit button to submit the assets for review."""
        try:
            submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit') or contains(., 'Release') or contains(., 'Send for review')]") ))
            submit.click()
        except Exception as e:
            raise RuntimeError("Could not find submit/release button: " + str(e))

    def quit(self):
        try:
            self.driver.quit()
        except Exception:
            pass
