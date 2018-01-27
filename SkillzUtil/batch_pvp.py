import re
import time
import os

from SkillzUtil.game import *
from SkillzUtil.util import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from SkillzUtil.group import *


def run(out, selector):
    print("Starting batch pvp run...")
    driver = new_tournament_driver()
    driver.get(driver.element_by_css_selector("a#menu_button_scores").get_attribute("href"))

    def run_game(gid):
        driver.execute_script("$('#vs').val('" + gid + "'); $('form').submit();")

    gid = driver.element_by_css_selector("#group").get_attribute("value")

    btns = [x for x in driver.find_elements_by_css_selector('a.btn') if "try-to-win" in x.get_attribute("class")]
    groups = \
        [Group(re.search(r'\d+', x.get_attribute("onclick"))[0],
         x.find_element_by_xpath("../..").find_element_by_css_selector(".name").text)
         for x in selector(btns)]
    print("Groups selected!")

    # Prepare form
    driver.set_attribute(driver.element_by_css_selector('form'), "target", "_blank")

    for x in groups:
        print("\tRunning game #" + str(x.id))
        run_game(x.id)
        time.sleep(1)

    driver.close()

    handles = driver.window_handles
    games = []
    print("Processing games...")
    for handle in reversed(handles):
        driver.switch_to.window(handle)
        play_link = WebDriverWait(driver, config.hard_timeout).until(
            EC.visibility_of(driver.element_by_css_selector("#play-link"))
        )
        driver.get(play_link.get_attribute("href"))
        g = Game(driver.element_by_css_selector("#replayData").get_attribute("innerHTML"), driver.current_url)
        games.append(g)
        print("\tProcessed game " + str(g))
        driver.close()
    driver.quit()

    def get_name(group_id):
        return next(g.name for g in groups if g.id == group_id)

    print("Printing to csv @ " + os.path.abspath(out))

    to_csv(out, games,
           {"opponent": lambda x: get_name(x.get_players()[0] if x.get_players()[0] != gid else x.get_players()[1]),
            "result": lambda x: "Win" if (x.get_winner() == gid) else ("Tie" if (x.get_winner() == "Tie") else "Lose"),
            "score": None,
            "length": None,
            "link": None}
           )

    return True
