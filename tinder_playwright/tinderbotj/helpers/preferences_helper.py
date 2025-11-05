from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

from tinderbotj.helpers.constants_helper import Sexuality
import time

class PreferencesHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/profile"

    def __init__(self, page):
        self.page = page

        # open profile
        try:
            xpath = '//*[@href="/app/profile"]'
            self.page.wait_for_selector(xpath, timeout=self.delay*1000)
            self.page.locator(xpath).click()
        except:
            pass

    def set_distance_range(self, km):
        # correct out of bounds values
        if km > 160:
            final_percentage = 100
        elif km < 2:
            final_percentage = 0
        else:
            final_percentage = (km / 160) * 100

        possible_xpaths = ['//*[@aria-label="Maximum distance in kilometres"]',
                           '//*[@aria-label="Maximum distance in kilometers"]',
                           '//*[@aria-label="Maximum distance in miles"]']

        link = None
        for xpath in possible_xpaths:
            try:
                self.page.wait_for_selector(xpath, timeout=self.delay*1000)
                link = self.page.locator(xpath)
                break
            except PlaywrightTimeoutError:
                continue

        print("\nSlider of distance will be adjusted...")
        current_percentage = float(link.get_attribute('style').split(' ')[1].split('%')[0])
        print("from {}% = {}km".format(current_percentage, current_percentage*1.6))
        print("to {}% = {}km".format(final_percentage, final_percentage*1.6))
        print("with a fault margin of 1%\n")

        # start adjusting the distance slider
        while abs(final_percentage - current_percentage) > 1:
            # Get the bounding box of the element
            box = link.bounding_box()
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2

            if current_percentage < final_percentage:
                # Move to element, press mouse, move by offset, release
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x + 3, y)
                self.page.mouse.up()
            elif current_percentage > final_percentage:
                # Move to element, press mouse, move by offset, release
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x - 3, y)
                self.page.mouse.up()

            # update current percentage
            current_percentage = float(link.get_attribute('style').split(' ')[1].split('%')[0])

        print("Ended slider with {}% = {}km\n\n".format(current_percentage, current_percentage*1.6))
        time.sleep(5)

    def set_age_range(self, min, max):
        # locate elements
        xpath = '//*[@aria-label="Minimum age"]'
        self.page.wait_for_selector(xpath, timeout=self.delay*1000)
        btn_minage = self.page.locator(xpath)

        xpath = '//*[@aria-label="Maximum age"]'
        self.page.wait_for_selector(xpath, timeout=self.delay*1000)
        btn_maxage = self.page.locator(xpath)

        min_age_tinder = int(btn_maxage.get_attribute('aria-valuemin'))
        max_age_tinder = int(btn_maxage.get_attribute('aria-valuemax'))

        # correct out of bounds values
        if min < min_age_tinder:
            min = min_age_tinder

        if max > max_age_tinder:
            max = max_age_tinder

        while max-min < 5:
            max += 1
            min -= 1

            if min < min_age_tinder:
                min = min_age_tinder
            if max > max_age_tinder:
                max = max_age_tinder

        range_ages_tinder = max_age_tinder - min_age_tinder
        percentage_per_year = 100 / range_ages_tinder

        to_percentage_min = (min - min_age_tinder) * percentage_per_year
        to_percentage_max = (max - min_age_tinder) * percentage_per_year

        current_percentage_min = float(btn_minage.get_attribute('style').split(' ')[1].split('%')[0])
        current_percentage_max = float(btn_maxage.get_attribute('style').split(' ')[1].split('%')[0])

        print("\nSlider of ages will be adjusted...")
        print("Minimum age will go ...")
        print("from {}% = {} years old".format(current_percentage_min,
                                               (current_percentage_min/percentage_per_year)+min_age_tinder))
        print("to {}% = {} years old".format(to_percentage_min, min))
        print("Maximum age will go ...")
        print("from {}% = {} years old".format(current_percentage_max,
                                               (current_percentage_max / percentage_per_year) + min_age_tinder))
        print("to {}% = {} years old".format(to_percentage_max, max))
        print("with a fault margin of 1%\n")

        # start adjusting the distance slider
        while abs(to_percentage_min - current_percentage_min) > 1 or abs(to_percentage_max - current_percentage_max) > 1:
            if current_percentage_min < to_percentage_min:
                box = btn_minage.bounding_box()
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x + 5, y)
                self.page.mouse.up()
            elif current_percentage_min > to_percentage_min:
                box = btn_minage.bounding_box()
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x - 5, y)
                self.page.mouse.up()

            if current_percentage_max < to_percentage_max:
                box = btn_maxage.bounding_box()
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x + 5, y)
                self.page.mouse.up()
            elif current_percentage_max > to_percentage_max:
                box = btn_maxage.bounding_box()
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
                self.page.mouse.move(x, y)
                self.page.mouse.down()
                self.page.mouse.move(x - 5, y)
                self.page.mouse.up()

            # update current percentage
            current_percentage_min = float(btn_minage.get_attribute('style').split(' ')[1].split('%')[0])
            current_percentage_max = float(btn_maxage.get_attribute('style').split(' ')[1].split('%')[0])

        print("Ended slider with ages from {} years old  to {} years old\n\n".format((current_percentage_min/percentage_per_year)+min_age_tinder,
              (current_percentage_max / percentage_per_year) + min_age_tinder))
        time.sleep(5)

    def set_sexualitiy(self, type):
        if not isinstance(type, Sexuality):
            assert False

        xpath = '//*[@href="/app/settings/gender"]/div/div/div/div'
        self.page.wait_for_selector(xpath, timeout=self.delay*1000)
        element = self.page.locator(xpath)
        element.click()

        xpath = '//*[@aria-pressed="false"]'.format(type.value)
        self.page.wait_for_selector(xpath, timeout=self.delay*1000)
        elements = self.page.locator(xpath).all()

        for element in elements:
            label_element = element.locator('.//div/label')
            if label_element.text_content() == type.value:
                element.click()
                break

        print("clicked on " + type.value)
        time.sleep(5)

    def set_global(self, boolean, language=None):
        # check if global is already activated
        # Global is activated when the href to preferred languages is visible
        is_activated = False
        try:
            xpath = '//*[@href="/app/settings/global/languages"]/div'
            self.page.wait_for_selector(xpath, timeout=self.delay*1000)
            self.page.locator(xpath)
            is_activated = True

        except:
            pass

        if boolean != is_activated:
            xpath = '//*[@name="global"]'
            element = self.page.locator(xpath)
            element.click()

        if is_activated and language:
            print("\nUnfortunately, Languages setting feature does not yet exist")
            print("If needed anyways:\nfeel free to open an issue and ask for the feature")
            print("or contribute by making a pull request.\n")

            '''
            languages_element.click()
            xpath = "//*[contains(text(), {})]".format(language)
            self.page.wait_for_selector(xpath, timeout=self.delay*1000)
            self.page.locator(xpath).all().click()
            '''
            time.sleep(5)
