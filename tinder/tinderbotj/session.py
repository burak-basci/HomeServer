# Selenium: automation of browser
from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.by import By

# some other imports :-)
import os
import platform
import time
import random
import requests
import atexit
from pathlib import Path
import subprocess
import socket

# tinderbotj: helper classes
from tinderbotj.helpers.geomatch import Geomatch
from tinderbotj.helpers.match import Match
from tinderbotj.helpers.profile_helper import ProfileHelper
from tinderbotj.helpers.preferences_helper import PreferencesHelper
from tinderbotj.helpers.geomatch_helper import GeomatchHelper
from tinderbotj.helpers.match_helper import MatchHelper
from tinderbotj.helpers.login_helper import LoginHelper
from tinderbotj.helpers.storage_helper import StorageHelper
from tinderbotj.helpers.email_helper import EmailHelper
from tinderbotj.helpers.constants_helper import Printouts
from tinderbotj.helpers.xpaths import *
from tinderbotj.addproxy import get_proxy_extension


class Session:
    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, headless=False, driver_path=None, store_session=True, proxy=None, user_data=False):
        self.email = None
        self.may_send_email = False
        self.session_data = {
            "duration": 0,
            "like": 0,
            "dislike": 0,
            "superlike": 0
        }
        
        # Initialize these early to avoid AttributeError in cleanup
        self.started = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.browser = None

        start_session = time.time()

        # this function will run when the session ends
        @atexit.register
        def cleanup():
            # End session duration
            seconds = int(time.time() - start_session)
            self.session_data["duration"] = seconds

            # add session data into a list of messages
            lines = []
            for key in self.session_data:
                message = "{}: {}".format(key, self.session_data[key])
                lines.append(message)

            # print out the statistics of the session
            try:
                box = self._get_msg_box(lines=lines, title="tinderbotj")
                print(box)
            finally:
                if hasattr(self, 'started'):
                    print("Started session: {}".format(self.started))
                y = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print("Ended session: {}".format(y))
            
                # Close browser properly if it exists
                if self.browser:
                    try:
                        self.browser.quit()
                    except:
                        pass

        # Check network connectivity before attempting to download
        if not self._check_network_connectivity():
            print("WARNING: Network connectivity issues detected. Trying to proceed...")
            # Try to fix DNS
            self._try_fix_dns()

        # Go further with the initialisation
        # Setting some options of the browser here below
        options = uc.ChromeOptions()
        
        # Add necessary arguments for headless and Docker/CI environments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--no-first-run')
        options.add_argument('--no-service-autorun')
        options.add_argument('--password-store=basic')
        options.add_argument("--lang=en-US")
        options.add_argument("--window-size=1920,1080")
        
        if headless:
            options.add_argument("--headless=new")
            
        # Create empty profile to avoid annoying Mac Popup
        if store_session:
            if not user_data:
                user_data = f"{Path().absolute()}/chrome_profile/"
            if not os.path.isdir(user_data):
                os.mkdir(user_data)

            Path(f'{user_data}First Run').touch()
            options.add_argument(f"--user-data-dir={user_data}")

        if proxy:
            if '@' in proxy:
                parts = proxy.split('@')

                user = parts[0].split(':')[0]
                pwd = parts[0].split(':')[1]

                host = parts[1].split(':')[0]
                port = parts[1].split(':')[1]

                extension = get_proxy_extension(PROXY_HOST=host, PROXY_PORT=port, PROXY_USER=user, PROXY_PASS=pwd)
                options.add_extension(extension)
            else:
                options.add_argument(f'--proxy-server=http://{proxy}')

        # Getting the chromedriver from cache or download it from internet
        print("Getting ChromeDriver ...")
        
        self.browser = uc.Chrome(options=options, driver_executable_path=driver_path)

        # Cool banner
        print(Printouts.BANNER.value)
        time.sleep(1)

        print("Started session: {}\n\n".format(self.started))

    def _check_network_connectivity(self):
        """Check if we can resolve DNS and connect to the internet"""
        try:
            # Try to resolve a common domain
            socket.gethostbyname('google.com')
            return True
        except socket.gaierror:
            return False

    def _try_fix_dns(self):
        """Try to fix DNS issues on Linux systems"""
        try:
            # Check if we're on Linux
            if platform.system() == 'Linux':
                # Try to restart systemd-resolved if available
                subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-resolved'], 
                             capture_output=True, timeout=5)
                time.sleep(2)
                
                # Alternative: try to use Google's DNS
                if not self._check_network_connectivity():
                    print("Attempting to use Google DNS (8.8.8.8)...")
                    # This would require root access to modify /etc/resolv.conf
                    # For now, just inform the user
                    print("If DNS issues persist, try:")
                    print("1. sudo systemctl restart systemd-resolved")
                    print("2. sudo echo 'nameserver 8.8.8.8' > /etc/resolv.conf")
                    print("3. Check your network connection")
        except:
            pass

    def _find_local_chromedriver(self):
        """Try to find a local ChromeDriver installation"""
        possible_paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
            os.path.expanduser('~/.local/bin/chromedriver'),
            os.path.join(os.getcwd(), 'chromedriver'),
            '/opt/chromedriver/chromedriver',
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        
        # Try to find chromedriver in PATH
        try:
            result = subprocess.run(['which', 'chromedriver'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None

    # Setting a custom location
    def set_custom_location(self, latitude, longitude, accuracy="100%"):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": int(accuracy.split('%')[0])
        }

        self.browser.execute_cdp_cmd("Page.setGeolocationOverride", params)

    # This will send notification when you get a match to your email used to logged in.
    def set_email_notifications(self, boolean):
        self.may_send_email = boolean

    # NOTE: Need to be logged in for this
    def set_distance_range(self, km):
        helper = PreferencesHelper(browser=self.browser)
        helper.set_distance_range(km)

    def set_age_range(self, min, max):
        helper = PreferencesHelper(browser=self.browser)
        helper.set_age_range(min, max)

    def set_sexuality(self, type):
        helper = PreferencesHelper(browser=self.browser)
        helper.set_sexualitiy(type)

    def set_global(self, boolean):
        helper = PreferencesHelper(browser=self.browser)
        helper.set_global(boolean)

    def set_bio(self, bio):
        helper = ProfileHelper(browser=self.browser)
        helper.set_bio(bio)

    def add_photo(self, filepath):
        helper = ProfileHelper(browser=self.browser)
        helper.add_photo(filepath)

    # Actions of the session
    def login_using_google(self, email, password):
        self.email = email
        if not self._is_logged_in():
            helper = LoginHelper(browser=self.browser)
            helper.login_by_google(email, password)
            time.sleep(5)
        if not self._is_logged_in():
            print('Manual interference is required.')
            input('press ENTER to continue')

    def login_using_facebook(self, email, password):
        self.email = email
        if not self._is_logged_in():
            helper = LoginHelper(browser=self.browser)
            helper.login_by_facebook(email, password)
            time.sleep(5)
        if not self._is_logged_in():
            print('Manual interference is required.')
            input('press ENTER to continue')

    def login_using_sms(self, country, phone_number):
        if not self._is_logged_in():
            helper = LoginHelper(browser=self.browser)
            helper.login_by_sms(country, phone_number)
            time.sleep(5)
        if not self._is_logged_in():
            print('Manual interference is required.')
            input('press ENTER to continue')

    def store_local(self, match):
        if isinstance(match, Match):
            filename = 'matches'
        elif isinstance(match, Geomatch):
            filename = 'geomatches'
        else:
            print("type of match is unknown, storing local impossible")
            print("Crashing in 3.2.1... :)")
            assert False

        # store its images
        for url in match.image_urls:
            hashed_image = StorageHelper.store_image_as(url=url, directory='data/{}/images'.format(filename))
            match.images_by_hashes.append(hashed_image)

        # store its userdata
        StorageHelper.store_match(match=match, directory='data/{}'.format(filename), filename=filename)

    def like(self, amount=1, ratio='100%', sleep=1, randomize_sleep = True):
        
        initial_sleep = sleep
        ratio = float(ratio.split('%')[0]) / 100

        if self._is_logged_in():
            helper = GeomatchHelper(browser=self.browser)
            amount_liked = 0
            # handle one time up front, from then on check after every action instead of before
            self._handle_potential_popups()
            print("\nLiking profiles started.")
            while amount_liked < amount:
                # randomize sleep
                if randomize_sleep:
                    sleep = random.uniform(0.5, 2.3) * initial_sleep
                if random.random() <= ratio:
                    if helper.like():
                        amount_liked += 1
                        # update for stats after session ended
                        self.session_data['like'] += 1
                        print(f"{amount_liked}/{amount} liked, sleep: {sleep}")
                else:
                    helper.dislike()
                    # update for stats after session ended
                    self.session_data['dislike'] += 1

                #self._handle_potential_popups()
                time.sleep(sleep)

            self._print_liked_stats()

    def dislike(self, amount=1):
        if self._is_logged_in():
            helper = GeomatchHelper(browser=self.browser)
            for _ in range(amount):
                self._handle_potential_popups()
                helper.dislike()

                # update for stats after session ended
                self.session_data['dislike'] += 1
                #time.sleep(1)
            self._print_liked_stats()

    def superlike(self, amount=1):
        if self._is_logged_in():
            helper = GeomatchHelper(browser=self.browser)
            for _ in range(amount):
                self._handle_potential_popups()
                helper.superlike()
                # update for stats after session ended
                self.session_data['superlike'] += 1
                time.sleep(1)
            self._print_liked_stats()

    def get_geomatch(self, quickload=True):
        if self._is_logged_in():
            helper = GeomatchHelper(browser=self.browser)
            self._handle_potential_popups()

            name = None
            attempts = 0
            max_attempts = 3
            while not name and attempts < max_attempts:
                attempts += 1
                name = helper.get_name()
                self._handle_potential_popups() # Popup handling on first geomatch
                time.sleep(1)

            age = helper.get_age()

            bio, passions, lifestyle, basics, anthem, looking_for = helper.get_bio_and_passions()
            image_urls = helper.get_image_urls(quickload)
            instagram = helper.get_insta(bio)
            rowdata = helper.get_row_data()
            work = rowdata.get('work')
            study = rowdata.get('study')
            home = rowdata.get('home')
            distance = rowdata.get('distance')
            gender = rowdata.get('gender')

            return Geomatch(name=name, age=age, work=work, gender=gender, study=study, home=home, distance=distance,
                            bio=bio, passions=passions, lifestyle=lifestyle, basics=basics, anthem=anthem, looking_for=looking_for, image_urls=image_urls, instagram=instagram)

    def get_chat_ids(self, new=True, messaged=True):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            return helper.get_chat_ids(new, messaged)

    def get_new_matches(self, amount=100000, quickload=True):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            return helper.get_new_matches(amount, quickload)

    def get_messaged_matches(self, amount=100000, quickload=True):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            return helper.get_messaged_matches(amount, quickload)

    def send_message(self, chatid, message):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            helper.send_message(chatid, message)

    def send_gif(self, chatid, gifname):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            helper.send_gif(chatid, gifname)

    def send_song(self, chatid, songname):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            helper.send_song(chatid, songname)

    def send_socials(self, chatid, media):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            helper.send_socials(chatid, media)

    def unmatch(self, chatid):
        if self._is_logged_in():
            helper = MatchHelper(browser=self.browser)
            self._handle_potential_popups()
            helper.unmatch(chatid)

    # Utilities
    def _handle_potential_popups(self):
        delay = 0.25

        # last possible id based div
        base_element = self.browser.find_element(By.XPATH, modal_manager)

        # try to deny see who liked you
        try:
            xpath = './/main/div/div/div[3]/button[2]'
            WebDriverWait(base_element, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            deny_btn = base_element.find_element(By.XPATH, xpath)
            deny_btn.click()
            return "POPUP: Denied see who liked you"

        except NoSuchElementException:
            pass
        except TimeoutException:
            pass

        # Try to dismiss a potential 'upgrade like' popup
        try:
            # locate "no thanks"-button
            xpath = './/main/div/button[2]'
            base_element.find_element(By.XPATH, xpath).click()
            return "POPUP: Denied upgrade to superlike"
        except NoSuchElementException:
            pass

        # try to deny 'add tinder to homescreen'
        try:
            xpath = './/main/div/div[2]/button[2]'

            add_to_home_popup = base_element.find_element(By.XPATH, xpath)
            add_to_home_popup.click()
            return "POPUP: Denied Tinder to homescreen"

        except NoSuchElementException:
            pass

        # deny buying more superlikes
        try:
            xpath = './/main/div/div[3]/button[2]'
            deny = base_element.find_element(By.XPATH, xpath)
            deny.click()
            return "POPUP: Denied buying more superlikes"
        except NoSuchElementException:
            pass

        # try to dismiss match
        matched = False
        try:
            xpath = '//button[@title="Back to Tinder"]'

            match_popup = base_element.find_element(By.XPATH, xpath)
            match_popup.click()
            matched = True

        except NoSuchElementException:
            pass
        except:
            matched = True
            self.browser.refresh()

        if matched and self.may_send_email:
            try:
                EmailHelper.send_mail_match_found(self.email)
            except:
                print("Some error occurred when trying to send mail.")
                print("Consider opening an Issue on Github.")
                pass
            return "POPUP: Dismissed NEW MATCH"

        # try to say 'no thanks' to buy more (super)likes
        try:
            xpath = './/main/div/div[3]/button[2]'
            deny_btn = base_element.find_element(By.XPATH, xpath)
            deny_btn.click()
            return "POPUP: Denied buying more superlikes"

        except ElementNotVisibleException:
            # element is not clickable, probably cuz it's out of view but still there
            self.browser.refresh()
        except NoSuchElementException:
            pass
        except:
            # TBD add stale element exception for now just refresh page
            self.browser.refresh()
            pass

        # Deny confirmation of email
        try:
            xpath = './/main/div/div[1]/div[2]/button[2]'
            remindmelater = base_element.find_element(By.XPATH, xpath)
            remindmelater.click()

            time.sleep(3)
            # handle other potential popups
            self._handle_potential_popups()
            return "POPUP: Deny confirmation of email"
        except:
            pass

        # Deny add location popup
        try:
            xpath = ".//*[contains(text(), 'No Thanks')]"
            nothanks = base_element.find_element(By.XPATH, xpath)
            nothanks.click()
            time.sleep(3)
            # handle other potential popups
            self._handle_potential_popups()
            return "POPUP: Deny confirmation of email"
        except:
            pass

        return None

    def _is_logged_in(self):
        try:
            self.browser.get("https://tinder.com/app/recs")
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="content"]'))
            )
            return True
        except TimeoutException:
            return False

    def _get_msg_box(self, lines, indent=1, width=None, title=None):
        """Print message-box with optional title."""
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'/{"=" * (width + indent * 2)}\\\n'  # upper_border
        if title:
            box += f'|{space}{title:<{width}}{space}|\n'  # title
            box += f'|{space}{"-" * len(title):<{width}}{space}|\n'  # underscore
        box += ''.join([f'|{space}{line:<{width}}{space}|\n' for line in lines])
        box += f'\\{"=" * (width + indent * 2)}/'  # lower_border
        return box

    def _print_liked_stats(self):
        likes = self.session_data['like']
        dislikes = self.session_data['dislike']
        superlikes = self.session_data['superlike']

        if superlikes > 0:
            print(f"You've superliked {self.session_data['superlike']} profiles during this session.")
        if likes > 0:
            print(f"You've liked {self.session_data['like']} profiles during this session.")
        if dislikes > 0:
            print(f"You've disliked {self.session_data['dislike']} profiles during this session.")