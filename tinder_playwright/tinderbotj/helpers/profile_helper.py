from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from tinderbotj.helpers.xpaths import content, modal_manager

import time, os

class ProfileHelper:

    delay = 5000  # milliseconds

    HOME_URL = "https://www.tinder.com/app/profile"

    def __init__(self, page):
        self.page = page

        # open profile
        try:
            xpath = '//*[@href="/app/profile"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)
            self.page.locator(xpath).click()
        except:
            pass

        self._edit_info()

    def _edit_info(self):
        xpath = '//a[@href="/app/profile/edit"]'

        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            self.page.locator(xpath).click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def _save(self):
        xpath = f"{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[1]/a"
        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            self.page.locator(xpath).click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def add_photo(self, filepath):
        # get the absolute filepath instead of the relative one
        filepath = os.path.abspath(filepath)

        # "add media" button
        xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[2]/span/button'
        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            btn = self.page.locator(xpath)
            btn.scroll_into_view_if_needed()
            btn.click()
        except Exception as e:
            print(e)

        xpath_input = f"{modal_manager}/div/div/div[1]/div[2]/div[2]/div/div/input"
        try:
            self.page.wait_for_selector(xpath_input, timeout=self.delay)
            self.page.locator(xpath_input).set_input_files(filepath)
        except Exception as e:
            print(e)

        xpath_choose = f"{modal_manager}/div/div/div[1]/div[1]/button[2]"
        try:
            self.page.wait_for_selector(xpath_choose, timeout=self.delay)
            self.page.locator(xpath_choose).click()
        except Exception as e:
            print(e)

        self._save()

    def set_bio(self, bio):
        xpath = f"{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[2]/div[2]/div/textarea"

        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            text_area = self.page.locator(xpath)

            for _ in range(500):
                text_area.press("Backspace")

            time.sleep(1)
            text_area.fill(bio)
            time.sleep(1)
        except Exception as e:
            print(e)

        self._save()
