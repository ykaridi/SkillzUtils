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

    main_handle = driver.current_window_handle

    def run_batch(grps):
        results = []

        print("Running games...")
        driver.switch_to.window(main_handle)
        for x in grps:
            print("\tRunning game vs " + str(x))
            run_game(x.id)
            time.sleep(1)

        handles = [wh for wh in driver.window_handles if wh != main_handle]
        print("Processing games...")
        for handle in reversed(handles):
            driver.switch_to.window(handle)
            play_link = WebDriverWait(driver, config.hard_timeout).until(
                EC.visibility_of(driver.element_by_css_selector("#play-link"))
            )
            time.sleep(1)
            driver.get(play_link.get_attribute("href"))
            g = Game(driver.element_by_css_selector("#replayData").get_attribute("innerHTML"), driver.current_url)
            results.append(g)
            print("\tProcessed game " + str(g))
            driver.close()

        driver.switch_to.window(main_handle)

        return results

    n = len(groups)/config.batch_size
    if n-int(n) > 0:
        n += 1
    n = int(n)

    games = []
    for i in range(n):
        print("Running batch [" + str(i*config.batch_size) + ":" + str((i+1)*config.batch_size))
        games.extend(run_batch(groups[i*config.batch_size:(i+1)*config.batch_size]))
        time.sleep(5)

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
