# immoware_selenium_api.py
import time
import pyperclip
import tempfile
import uuid
import os
import sys
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from APIs.immoware_selenium.config_selenium import SeleniumConfig


def ensure_logged_in(func):
    """Decorator to ensure login before running the method."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not getattr(self, "logged_in", False):
            self.login()
        return func(self, *args, **kwargs)
    return wrapper


class ImmowareSeleniumAPI:
    """Selenium-based API for Immoware24 operations."""

    def __init__(self, download_dir: str = None, chromedriver_path: str = None):
        self.config = SeleniumConfig()
        self.mandant = self.config.MANDANT
        self.username = self.config.USERNAME
        self.password = self.config.PASSWORD
        self.download_dir = download_dir or self.config.DOWNLOAD_DIR
        self.chromedriver_path = chromedriver_path or self.config.CHROMEDRIVER_PATH
        
        # ensure download dir exists
        os.makedirs(self.download_dir, exist_ok=True)
        
        self.service = Service(executable_path=self.chromedriver_path)
                
        # Set Chrome options with unique user data directory
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # improve download prefs for headless chrome
        chrome_prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        
        # wait a maximum of 10 seconds for elements to load
        self.wait = WebDriverWait(self.driver, 10)

    def wait_for_download(self, filename, timeout=60, directory: str = None):
        """Warte, bis Download abgeschlossen ist.

        If `directory` is provided, look for the file there; otherwise use `self.download_dir`.
        Returns the full path to the downloaded file.
        """
        search_dir = directory or self.download_dir
        end_time = time.time() + timeout
        # Wait until a file with exact name appears in the directory and is not a temporary .crdownload
        while time.time() < end_time:
            try:
                for fname in os.listdir(search_dir):
                    # exact filename match and not a temp download file
                    if fname == filename and not fname.endswith(".crdownload"):
                        full = os.path.join(search_dir, fname)
                        # double-check file exists and has non-zero size (optional safety)
                        if os.path.exists(full):
                            return full
            except FileNotFoundError:
                # directory might not exist yet
                pass
            time.sleep(1)
        raise TimeoutError(f"Download nicht abgeschlossen: {filename}")

    def login(self):
        """Log in to Immoware24."""
        try:
            self.driver.get("https://www.awi-rems.de/router/auth/login")
            # Wait for fields to appear
            mandant_field = self.wait.until(EC.presence_of_element_located((By.NAME, "mandator")))
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "user")))
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            
            # Fill login info
            mandant_field.clear()
            mandant_field.send_keys(self.mandant)
            username_field.clear()
            username_field.send_keys(self.username)
            password_field.clear()
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            # Accept notification if present
            try:
                weiter_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='weiter']"))
                )
                weiter_button.click()
                print("Notification akzeptiert, weiter zum Dashboard", file=sys.stderr)
            except:
                # Button not found → page might already be the dashboard
                pass

            # Wait until the dashboard is loaded
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/dashboard')] | //*[@id='dashboard']")))
            self.logged_in = True
            print("Successfully logged in to Immoware24", file=sys.stderr)
        except Exception as e:
            print(f"Login failed: {e}", file=sys.stderr)
            raise

    @ensure_logged_in
    def export_adressbuch(self, filename: str = None):
        """Export contacts from Adressbuch."""
        try:
            # Direkt zur Export-Seite gehen
            self.driver.get("https://athene.awi-rems.de/extdata/contact/export")

            # Kategorie-Auswahl öffnen
            category_picker = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.selectorSelection.categoryPicker"))
            )
            category_picker.click()

            # Popup Checkbox anklicken
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.catSelect[value='1000']"))
            )
            checkbox.click()

            # Auswahl bestätigen
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "selectorCloser"))
            )
            close_button.click()

            # Dateiname setzen
            if not filename:
                filename = f"n8n_Kontakt_Export_{time.strftime('%Y%m%d-%H%M%S')}"

            filename_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "My_Form_ExportForm-fileName"))
            )
            filename_input.clear()
            filename_input.send_keys(filename)

            # Speichern klicken
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "My_Form_ExportForm-save"))
            )
            save_button.click()
            
            # Auf das Popup mit dem direkten Link warten
            popup_link = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='msg-inner']//a[contains(@href, '/dms/document/show')]")
                )
            )

            # Direkt die URL aus dem Popup holen
            doc_url = popup_link.get_attribute("href")
            print(f"Dokument erstellt: {doc_url}", file=sys.stderr)

            # Zum Download-Link gehen (Seite aufrufen)
            self.driver.get(doc_url)

            # Den Download-Button "herunterladen" anklicken
            download_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btnFooter[title='herunterladen']"))
            )
            download_button.click()

            # Warte auf Download-Finish in the main download dir
            downloaded_full = self.wait_for_download(f"{filename}.csv")

            # ensure target subfolder under repo downloads exists and move the file there
            contacts_dir = os.path.join(self.download_dir, 'contacts')
            # create contacts dir if missing
            os.makedirs(contacts_dir, exist_ok=True)
            
            target_path = os.path.join(contacts_dir, os.path.basename(downloaded_full))
            try:
                if os.path.abspath(downloaded_full) != os.path.abspath(target_path):
                    try:
                        os.replace(downloaded_full, target_path)
                    except Exception:
                        # fallback to copy & remove
                        import shutil
                        shutil.copy2(downloaded_full, target_path)
                        try:
                            os.remove(downloaded_full)
                        except Exception:
                            pass
            except Exception:
                pass

            # remove any older files in contacts_dir except the current one
            try:
                for f in os.listdir(contacts_dir):
                    fp = os.path.join(contacts_dir, f)
                    if os.path.abspath(fp) != os.path.abspath(target_path):
                        try:
                            os.remove(fp)
                        except Exception:
                            pass
            except Exception:
                pass

            print(f"Document downloaded: {filename}", file=sys.stderr)
            # return path relative to repository root so callers running in repo can use
            # a stable path that begins with `n8n/...` (download_dir is under n8n/<area>/downloads)
            try:
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                rel = os.path.relpath(target_path, start=repo_root)
            except Exception:
                rel = os.path.relpath(target_path)
            return rel

        except Exception as e:
            print(f"Failed to download document: {e}")
            raise

    @ensure_logged_in
    def export_properties(self, filename: str = None):
        """Export properties (objektdaten) from a given export URL and download the file.

        This mirrors the flow used in `export_adressbuch` but accepts an `export_url`.
        Selectors are best-effort; adjust them to the real page DOM if needed.
        """
        try:
            # Go to the provided export URL
            self.driver.get("https://athene.awi-rems.de/objectdata/global-objectdata-overview/export/adminType_ids/2/adminType_ids/1/adminType_ids/3")

            # Try to open category picker (best-effort)
            try:
                category_picker = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.selectorSelection.categoryPicker"))
                )
                category_picker.click()
            except Exception:
                # If not present, continue — page may not require it
                pass

            # Try to click a category checkbox (best-effort)
            try:
                checkbox = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.catSelect"))
                )
                checkbox.click()
                # close picker if there's a closer
                try:
                    close_button = self.wait.until(
                        EC.element_to_be_clickable((By.ID, "selectorCloser"))
                    )
                    close_button.click()
                except Exception:
                    pass
            except Exception:
                # ignore if not found
                pass

            # Default filename
            if not filename:
                filename = f"n8n_Objekt_Export_{time.strftime('%Y%m%d-%H%M%S')}"

            # Try to set filename if input present
            try:
                filename_input = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "My_Form_ExportForm-fileName"))
                )
                filename_input.clear()
                filename_input.send_keys(filename)
            except Exception:
                # proceed without setting filename
                pass

            # Click save / export button
            try:
                save_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "My_Form_ExportForm-save"))
                )
                save_button.click()
            except Exception:
                # fallback: try to click any button/input with text 'speichern'
                try:
                    btns = self.driver.find_elements(By.XPATH, "//button|//input[@type='submit']")
                    for b in btns:
                        if 'speichern' in (getattr(b, 'text', '') or '').lower():
                            try:
                                b.click()
                                break
                            except Exception:
                                pass
                except Exception:
                    pass

            # Wait for popup with document link
            popup_link = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='msg-inner']//a[contains(@href, '/dms/document/show')]") )
            )
            # Some test stubs may return a plain object; ensure we have an element
            if not hasattr(popup_link, 'get_attribute'):
                try:
                    popup_elem = self.driver.find_element(By.XPATH, "//div[@class='msg-inner']//a[contains(@href, '/dms/document/show')]")
                    doc_url = popup_elem.get_attribute("href")
                except Exception:
                    raise
            else:
                doc_url = popup_link.get_attribute("href")
            print(f"Dokument erstellt: {doc_url}", file=sys.stderr)

            # Navigate to the document page and download
            self.driver.get(doc_url)

            # Try clicking the download control (CSS first, then LINK_TEXT). Treat either as success.
            clicked = False
            try:
                download_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btnFooter[title='herunterladen']"))
                )
                download_button.click()
                clicked = True
            except Exception:
                try:
                    download_button = self.wait.until(lambda drv: drv.find_element(By.LINK_TEXT, "herunterladen"))
                    download_button.click()
                    clicked = True
                except Exception:
                    clicked = False

            if not clicked:
                raise RuntimeError("Download-Button nicht gefunden oder nicht klickbar")

            # Wait for the file to appear in the download dir
            downloaded_full = self.wait_for_download(f"{filename}.csv")

            # ensure target subfolder under repo downloads exists and move the file there
            properties_dir = os.path.join(self.download_dir, 'properties')
            os.makedirs(properties_dir, exist_ok=True)

            target_path = os.path.join(properties_dir, os.path.basename(downloaded_full))
            try:
                if os.path.abspath(downloaded_full) != os.path.abspath(target_path):
                    try:
                        os.replace(downloaded_full, target_path)
                    except Exception:
                        import shutil
                        shutil.copy2(downloaded_full, target_path)
                        try:
                            os.remove(downloaded_full)
                        except Exception:
                            pass
            except Exception:
                pass

            # Normalize CSV headers using dedicated helper (semicolon-separated CSV)
            try:
                self._fix_properties_header(target_path)
            except Exception:
                # non-fatal: leave file as-is if post-processing fails
                pass

            # remove any older files in properties_dir except the current one
            try:
                for f in os.listdir(properties_dir):
                    fp = os.path.join(properties_dir, f)
                    if os.path.abspath(fp) != os.path.abspath(target_path):
                        try:
                            os.remove(fp)
                        except Exception:
                            pass
            except Exception:
                pass

            print(f"Document downloaded: {filename}", file=sys.stderr)
            try:
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                rel = os.path.relpath(target_path, start=repo_root)
            except Exception:
                rel = os.path.relpath(target_path)
            return rel

        except Exception as e:
            print(f"Failed to export properties document: {e}")
            raise

    @ensure_logged_in
    def download_dms_document(self, doc_name: str):
        """Download a specific document from DMS."""
        try:
            self.driver.get("https://www.immoware24.de/dms")  # DMS URL
            # Wait and click document link
            doc_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, doc_name)))
            doc_link.click()
            time.sleep(3)  # Wait for download to finish
            print(f"Document downloaded: {doc_name}", file=sys.stderr)
        except Exception as e:
            print(f"Document download failed: {e}", file=sys.stderr)
            raise

    def quit(self):
        """Close the browser and clean up."""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            self.logged_in = False
        except Exception as e:
            # ensure quit does not silently fail when called in cleanup; log to stderr
            print(f"Error during quit: {e}", file=sys.stderr)
            
            # Clean up temporary user data directory
            import shutil
            if hasattr(self, 'user_data_dir'):
                try:
                    shutil.rmtree(self.user_data_dir, ignore_errors=True)
                except:
                    pass
            print("Browser closed and cleaned up")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit()

    # Add new helper to normalize the properties CSV header
    def _fix_properties_header(self, target_path):
        import csv
        import re

        # Helper: transliterate common german characters to ASCII-friendly forms
        def translit(s: str) -> str:
            if not isinstance(s, str):
                return s
            # normalize common umlauts and special chars used here
            s = s.replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
            s = s.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
            s = s.replace('ß', 'ss')
            return s

        # Read entire CSV preserving rows; try several encodings to be tolerant
        from io import StringIO

        encodings_to_try = ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1']
        rows = None
        last_exception = None
        for enc in encodings_to_try:
            try:
                with open(target_path, 'rb') as fh:
                    raw = fh.read()
                text = raw.decode(enc)
                reader = csv.reader(StringIO(text), delimiter=';')
                rows = list(reader)
                used_encoding = enc
                break
            except Exception as e:
                last_exception = e
                rows = None

        if not rows:
            # give up if we couldn't decode the file
            raise UnicodeError(f"Unable to decode CSV file {target_path}: last error: {last_exception}")

        header = rows[0]
        new_header = []
        vz_count = 0

        for raw_f in header:
            # strip whitespace and surrounding quotes
            if raw_f is None:
                f = ''
            else:
                f = raw_f.strip()
            # remove wrapping double quotes if present
            if len(f) >= 2 and ((f[0] == '"' and f[-1] == '"') or (f[0] == "'" and f[-1] == "'")):
                f = f[1:-1].strip()

            # normalize common misspellings and variants
            # lowercase-copy for matching, but keep original case for later translit
            f_lower = f.lower()

            # fix obvious misspellings
            if 'akutell' in f_lower or 'akutelle' in f_lower:
                f = re.sub(r'(?i)akutell[ea]?\s+eigentu[mn]er', 'aktuelle Eigentuemer', f)
            # replace German sharp-s and diacritics in the token 'Eigentümer' and similar
            if 'eigent' in f_lower:
                # normalize any 'Eigentümer' occurrences to 'Eigentuemer'
                f = re.sub('(?i)eigentu[mn]er', 'Eigentuemer', f)
                f = re.sub('(?i)eigentÃ¼mer', 'Eigentuemer', f)  # handle common mojibake

            # normalize the exact token
            if f.lower() == 'eigentuemer' or f == 'Eigentuemer':
                f = 'Eigentuemer'

            # handle the 'vereinbarter Zahlbetrag' columns: there may be two; rename first/second
            if f_lower == 'vereinbarter zahlbetrag' or 'vereinbarter zahlbetrag' in f_lower:
                vz_count += 1
                if vz_count == 1:
                    f = 'Eigentuemer vereinbarter Zahlbetrag'
                elif vz_count == 2:
                    f = 'Mieter vereinbarter Zahlbetrag'

            # ensure 'aktuelle Eigentümer' -> 'aktuelle Eigentuemer'
            if 'aktuelle eigent' in f_lower or 'aktueller eigent' in f_lower:
                f = re.sub(r'(?i)aktuell(?:e|er)?\s+eigentu[mn]er', 'aktuelle Eigentuemer', f)

            # final transliteration to drop special chars like 'ö' etc. while keeping ASCII letters
            f = translit(f)

            new_header.append(f)

        rows[0] = new_header

        # --- New feature: add identifier column combining Objekt-Nummer + VE-Nummer ---
        # Find indices (case-insensitive match) for Objekt-Nummer and VE-Nummer using regex
        header_lc = [h.lower() for h in new_header]
        idx_obj = None
        idx_ve = None
        import re as _re
        for i, h in enumerate(header_lc):
            h_comp = _re.sub(r"[^a-z0-9]", "", h)
            # match objekt-nummer variants: objekt, objektnummer, objekt-nummer
            if idx_obj is None and _re.match(r'^(objekt|objektnummer|objektnummer|objektnummer)$', h_comp):
                idx_obj = i
            # match ve-nummer variants: ve-nummer, venummer, ve nummer
            if idx_ve is None and _re.match(r'^(venummer|ve|venr|ve-nummer|venummer)$', h_comp):
                idx_ve = i

        # Append new header column name
        id_col_name = 'Objekt-VE-Nummer'
        # Only append if not already present
        if id_col_name.lower() not in header_lc:
            rows[0].append(id_col_name)

            # For each data row, compute identifier using available fields; leave empty if missing
            for ri in range(1, len(rows)):
                row = rows[ri]
                # ensure row has at least as many columns as header (pad if necessary)
                if len(row) < len(rows[0]) - 1:
                    # pad row to length of header minus the new id column
                    row += [''] * ((len(rows[0]) - 1) - len(row))

                val_obj = ''
                val_ve = ''
                if idx_obj is not None and idx_obj < len(row):
                    val_obj = row[idx_obj].strip()
                if idx_ve is not None and idx_ve < len(row):
                    val_ve = row[idx_ve].strip()

                # Build identifier: prefer underscore-separated, skip empties
                if val_obj and val_ve:
                    new_id = f"{val_obj}_{val_ve}"
                elif val_obj:
                    new_id = val_obj
                elif val_ve:
                    new_id = val_ve
                else:
                    new_id = ''

                rows[ri].append(new_id)

        # write back with utf-8 and semicolon delimiter
        with open(target_path, 'w', encoding='utf-8', newline='') as fh:
            writer = csv.writer(fh, delimiter=';')
            writer.writerows(rows)
