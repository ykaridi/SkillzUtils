import csv
from selenium import webdriver
import SkillzUtil.config as config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pandas import DataFrame
from pandas import ExcelWriter


def new_chrome_driver(with_images=False, headless=False, no_sounds=True):
    def set_attribute(self, element, att, v):
        self.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                              element, att, v)

    def set_value(self, element, v):
        self.execute_script("arguments[0].value=arguments[1]", element, v)

    def element_by_css_selector(self, selector):
        return WebDriverWait(self, config.soft_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def element_by_id(self, element_id):
        return WebDriverWait(self, config.soft_timeout).until(EC.presence_of_element_located((By.ID, element_id)))

    options = webdriver.ChromeOptions()
    prefs = {}
    if not with_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    if headless and config.headless:
        options.add_argument('headless')
    if no_sounds:
        options.add_argument("--mute-audio")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_attribute = set_attribute.__get__(driver, driver.__class__)
    driver.set_value = set_value.__get__(driver, driver.__class__)
    driver.element_by_css_selector = element_by_css_selector.__get__(driver, driver.__class__)
    driver.element_by_id = element_by_id.__get__(driver, driver.__class__)
    return driver


def new_authenticated_tournament_driver(user, password, connection_type):
    driver = new_chrome_driver(with_images=False, headless=True)
    if connection_type == "idm":
        driver.get(config.baseURL)
        driver.get(driver.element_by_id("ministry_of_education_login").get_attribute("href"))
        usr_input = driver.element_by_id("HIN_USERID")
        passwrd_input = driver.element_by_id("Ecom_Password")
        driver.set_value(usr_input, user)
        driver.set_value(passwrd_input, password)
        usr_input.submit()
        driver.get("https://piratez.skillz-edu.org/home/")
        tournament_btn = driver.element_by_id("tournament_button_" + str(config.tournament_number))
        tournament_btn.submit()
        return driver
    elif connection_type == "local":
        driver.get(config.baseURL)
        email_input = driver.element_by_id("id_email")
        passwrd_input = driver.element_by_id("id_password")
        driver.set_value(email_input, user)
        driver.set_value(passwrd_input, password)
        passwrd_input.submit()
        driver.get("https://piratez.skillz-edu.org/home/")
        tournament_btn = driver.element_by_id("tournament_button_" + str(config.tournament_number))
        tournament_btn.submit()
        return driver

    raise Exception("Invalid connection type!")


def new_tournament_driver():
    if config.authenticate > 0:
        return new_authenticated_tournament_driver(config.user, config.password, config.connection_type)

    driver = new_chrome_driver(False)
    driver.get(config.baseURL)
    try:
        WebDriverWait(driver, 60).until(
            EC.url_matches(".*/group_dashboard/.*")
        )
    except:
        return new_tournament_driver()

    return driver


def to_dataframe(arr, attributes):
    df = DataFrame(
        {x: [getattr(row, "get_" + x)() if attributes[x] is None else attributes[x](row) for row in arr] for x in
         attributes})
    df = df[list(attributes.keys())]
    return df


def to_csv(path, arr, attributes):
    df = to_dataframe(arr, attributes)
    df.to_csv(path)


def to_excel(path, arr, attributes):
    df = to_dataframe(arr, attributes)
    write_excel(path, {"Score Sheet": df})


def write_excel(path, dfs):
    writer = ExcelWriter(path, engine='xlsxwriter')
    for sheetname, df in dfs.items():  # loop through `dict` of dataframes
        df.to_excel(writer, sheet_name=sheetname)  # send df to writer
        worksheet = writer.sheets[sheetname]  # pull worksheet object
        for idx, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
            worksheet.set_column(idx+1, idx+1, max_len)  # set column width
    writer.save()
