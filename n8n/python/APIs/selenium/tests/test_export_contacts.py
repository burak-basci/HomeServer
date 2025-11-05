from APIs.immoware_selenium.immoware_selenium_api import ImmowareSeleniumAPI

selenium = ImmowareSeleniumAPI()

contacts = selenium.export_adressbuch()
