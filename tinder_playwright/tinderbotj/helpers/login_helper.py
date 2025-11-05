from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from tinderbotj.helpers.xpaths import content
import time

class LoginHelper:

    delay = 7000  # milliseconds for Playwright

    def __init__(self, page, context):
        self.page = page
        self.context = context
        self._accept_cookies()

    def _click_login_button(self):
        try:
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
            self.page.wait_for_selector(xpath, timeout=self.delay)
            button = self.page.locator(xpath)
            button.click()
            time.sleep(3)
        except PlaywrightTimeoutError:
            self._exit_by_time_out()
        except Exception:
            pass

    def login_by_google(self, email, password):
        self._click_login_button()

        # wait for google button to appear
        xpath = '//*[@aria-label="Log in with Google"]'
        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            self.page.locator(xpath).click()
        except PlaywrightTimeoutError:
            self._exit_by_time_out()
        except Exception:
            # page was still loading when attempting to click google login
            time.sleep(4)
            self.page.locator(xpath).click()

        if not self._change_focus_to_pop_up():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.login_by_google(email, password)

        try:
            xpath = "//input[@type='email']"
            self.page.wait_for_selector(xpath, timeout=self.delay)

            emailfield = self.page.locator(xpath)
            emailfield.fill(email)
            emailfield.press("Enter")
            # sleeping 3 seconds for passwordfield to come through
            time.sleep(3)
        except PlaywrightTimeoutError:
            self._exit_by_time_out()

        try:
            xpath = "//input[@type='password']"
            self.page.wait_for_selector(xpath, timeout=self.delay)

            pwdfield = self.page.locator(xpath)
            pwdfield.fill(password)
            pwdfield.press("Enter")

        except PlaywrightTimeoutError:
            self._exit_by_time_out()

        self._change_focus_to_main_window()
        self._handle_popups()

    def login_by_facebook(self, email, password):
        self._click_login_button()

        # wait for facebook button to appear
        xpath = '//*[@aria-label="Log in with Facebook"]'
        try:
            self.page.wait_for_selector(xpath, timeout=self.delay)
            self.page.locator(xpath).click()
        except PlaywrightTimeoutError:
            self._exit_by_time_out()
        except Exception:
            # page was still loading when attempting to click facebook login
            time.sleep(4)
            self.page.locator(xpath).click()

        if not self._change_focus_to_pop_up():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.login_by_facebook(email, password)

        try:
            xpath_cookies = '//*[@data-cookiebanner="accept_button"]'
            self.page.wait_for_selector(xpath_cookies, timeout=self.delay)
            self.page.locator(xpath_cookies).click()
        except PlaywrightTimeoutError:
            # Not everyone might have the cookie banner so let's just continue then
            pass

        try:
            xpath_email = '//*[@id="email"]'
            xpath_password = '//*[@id="pass"]'
            xpath_button = '//*[@id="loginbutton"]'

            self.page.wait_for_selector(xpath_email, timeout=self.delay)

            emailfield = self.page.locator(xpath_email)
            emailfield.fill(email)

            pwdfield = self.page.locator(xpath_password)
            pwdfield.fill(password)

            loginbutton = self.page.locator(xpath_button)
            loginbutton.click()

        except PlaywrightTimeoutError:
            self._exit_by_time_out()

        self._change_focus_to_main_window()
        self._handle_popups()

    def login_by_sms(self, country, phone_number):
        self._click_login_button()

        # wait for sms button to appear
        try:
            xpath = '//*[@aria-label="Log in with phone number"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)

            btn = self.page.locator(xpath)
            btn.click()
        except PlaywrightTimeoutError:
            self._exit_by_time_out()

        self._handle_prefix(country)

        # Fill in sms
        try:
            xpath = '//*[@name="phone_number"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)

            field = self.page.locator(xpath)
            field.fill(phone_number)
            field.press("Enter")

        except PlaywrightTimeoutError:
            self._exit_by_time_out()

        print("\n\nPROCEED MANUALLY BY ENTERING SMS CODE\n")
        # check every second if user has bypassed sms-code barrier
        while not self._is_logged_in():
            time.sleep(1)

        self._handle_popups()

    def _handle_prefix(self, country):
        self._accept_cookies()

        xpath = '//div[@aria-describedby="phoneErrorMessage"]/div/div'
        self.page.wait_for_selector(xpath, timeout=self.delay)
        btn = self.page.locator(xpath)
        btn.click()

        els = self.page.locator('//div').all()
        for el in els:
            try:
                span = el.locator('.//span')
                if span.text_content().lower() == country.lower():
                    print("clicked")
                    el.click()
                    break
                else:
                    print(span.text_content())
            except:
                continue

    # checks if user is logged in by checking the url
    def _is_logged_in(self):
        return 'app' in self.page.url

    def _handle_popups(self):
        for _ in range(20):
            if not self._is_logged_in():
                time.sleep(1.2)
            else:
                break

        if not self._is_logged_in():
            print('Still not logged in ... ?')
            input('Proceed manually and press ENTER to continue\n')

        time.sleep(2)
        self._accept_cookies()
        self._accept_location_notification()
        self._deny_overlayed_notifications()

        time.sleep(5)

    def _accept_location_notification(self):
        try:
            xpath = '//*[@data-testid="allow"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)

            locationBtn = self.page.locator(xpath)
            locationBtn.click()
            print("ACCEPTED LOCATION.")
        except PlaywrightTimeoutError:
            print(
                "ACCEPTING LOCATION: Loading took too much time! Element probably not presented, so we continue.")
        except:
            pass

    def _deny_overlayed_notifications(self):
        try:
            xpath = '//*[@data-testid="decline"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)

            self.page.locator(xpath).click()
            print("DENIED NOTIFICATIONS.")
        except PlaywrightTimeoutError:
            print(
                "DENYING NOTIFICATIONS: Loading took too much time! Element probably not presented, so we continue.")
        except:
            pass

    def _accept_cookies(self):
        try:
            xpath = '//*[@type="button"]'
            self.page.wait_for_selector(xpath, timeout=self.delay)
            buttons = self.page.locator(xpath).all()

            for button in buttons:
                try:
                    text_span = button.locator('.//span').text_content()
                    if text_span and 'accept' in text_span.lower():
                        button.click()
                        print("COOKIES ACCEPTED.")
                        break
                except:
                    pass

        except PlaywrightTimeoutError:
            print(
                "ACCEPTING COOKIES: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("Error cookies", e)
            pass

    def _change_focus_to_pop_up(self):
        max_tries = 50
        current_tries = 0

        # Wait for popup to appear
        while current_tries < max_tries:
            current_tries += 1
            time.sleep(0.30)

            pages = self.context.pages
            if len(pages) > 1:
                # Switch to the new page (popup)
                self.page = pages[-1]
                return True

        print("tries exceeded")
        return False

    def _change_focus_to_main_window(self):
        pages = self.context.pages
        if len(pages) >= 1:
            self.page = pages[0]

    def _exit_by_time_out(self):
        print("Loading an element took too much time!. Please check your internet connection.")
        print("Alternatively, you can add a sleep or higher the delay class variable.")
        exit(1)
