from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import random
from Constants import *
from Util import *
from Game import *
import csv
import time
from Group import *


def Run(out, selector):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)

    def run_game(gid):
        driver.execute_script("$('#vs').val('" + gid + "'); $('form').submit();")

    driver.get(baseURL)
    try:
        WebDriverWait(driver, 60).until(
            EC.url_matches(".*/scores")
        )
    except:
        return False

    gid = driver.find_element_by_css_selector("#group").get_attribute("value")

    btns = [x for x in driver.find_elements_by_css_selector('a.btn') if "try-to-win" in x.get_attribute("class")]
    groups = [Group(re.search(r'\d+', x.get_attribute("onclick"))[0], x.find_element_by_xpath("../..").find_element_by_css_selector(".name").text) for x in selector(btns)]

    # Prepare form
    setAttribute(driver, driver.find_element_by_css_selector('form'), "target", "_blank")

    for x in groups:
        run_game(x.id)
        time.sleep(1)

    driver.close()

    handles = driver.window_handles
    games = []
    for handle in reversed(handles):
        driver.switch_to.window(handle)
        WebDriverWait(driver, 180).until(
            EC.visibility_of(driver.find_element_by_css_selector("#play-link"))
        )
        driver.get(driver.find_element_by_css_selector("#play-link").get_attribute("href"))
        g = Game(driver.find_element_by_css_selector("#replayData").get_attribute("innerHTML"), driver.current_url)
        games.append(g)
        driver.close()
    driver.quit()

    def get_name(group_id):
        return next(g.name for g in groups if g.id == group_id)

    to_csv(out, games,
           {"opponent": lambda x: get_name(x.get_players()[0] if x.get_players()[0] != gid else x.get_players()[1]),
            "result": lambda x: "Win" if (x.get_winner() == gid) else ("Tie" if (x.get_winner() == "Tie") else "Lose"),
            "score": None,
            "length": None,
            "link": None}
           )

    return True


Run("log.csv", lambda groups: random.sample(groups, 10))
