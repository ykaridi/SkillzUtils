import csv
from selenium import webdriver


def new_chrome_driver(with_images = False):
    def set_attribute(self, element, att, v):
        self.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                              element, att, v)

    options = webdriver.ChromeOptions()
    if not with_images:
        prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_attribute = set_attribute.__get__(driver, driver.__class__)
    return driver


def to_csv(path, arr, attributes):
    with open(path, "w") as f:
        wr = csv.writer(f, delimiter=",")
        wr.writerow(attributes.keys())
        for elem in arr:
            wr.writerow([getattr(elem, "get_" + x)() if attributes[x] is None else attributes[x](elem) for x in attributes])