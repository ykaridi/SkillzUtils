import csv
from selenium import webdriver
import SkillzUtil.config as config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def new_chrome_driver(with_images=False, headless=False, no_sounds=True):
    def set_attribute(self, element, att, v):
        self.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                              element, att, v)

    def set_value(self, element, v):
        self.execute_script("arguments[0].value=arguments[1]", element, v)

    options = webdriver.ChromeOptions()
    prefs = {}
    if not with_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    if headless and (not config.headfull):
        options.add_argument('headless')
    if no_sounds:
        options.add_argument("--mute-audio")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_attribute = set_attribute.__get__(driver, driver.__class__)
    driver.set_value = set_value.__get__(driver, driver.__class__)
    return driver


def new_authenticated_tournament_driver(email, passwrd):
    driver = new_chrome_driver(with_images=False, headless=True)
    driver.get(config.baseURL)
    email_input = WebDriverWait(driver, config.soft_timeout).until(EC.presence_of_element_located((By.ID, 'id_email')))
    passwrd_input = WebDriverWait(driver, config.soft_timeout).until(EC.presence_of_element_located((By.ID, 'id_password')))
    driver.set_value(email_input, email)
    driver.set_value(passwrd_input, passwrd)
    passwrd_input.submit()
    driver.get("https://piratez.skillz-edu.org/home/")
    tournament_btn = WebDriverWait(driver, config.soft_timeout).until(EC.presence_of_element_located((By.ID, "tournament_button_" + str(config.tournament_number))))
    tournament_btn.submit()
    return driver


def new_tournament_driver():
    if len(config.email) > 0 and len(config.passwrd) > 0:
        return new_authenticated_tournament_driver(config.email, config.passwrd)

    driver = new_chrome_driver(False)
    driver.get(config.baseURL)
    try:
        WebDriverWait(driver, 60).until(
            EC.url_matches(".*/group_dashboard/.*")
        )
    except:
        return new_tournament_driver()

    return driver


def to_csv(path, arr, attributes):
    with open(path, "w") as f:
        wr = csv.writer(f, delimiter=",")
        wr.writerow(attributes.keys())
        for elem in arr:
            wr.writerow([getattr(elem, "get_" + x)() if attributes[x] is None else attributes[x](elem) for x in attributes])