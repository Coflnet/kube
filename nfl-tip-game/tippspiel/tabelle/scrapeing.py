from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import re

# pfad zum programm chromedriver, in dem die webseite geöffnet wird windows
PATH = r"H:\Daten\nfl-tippspiel\tippspiel\tabelle\chromedriver.exe"


# pfad linux
# PATH = "/usr/bin/chromedriver"

# scrape games
def scrape(url):
    class Game:  # class, in der die daten der spiele gespeichert werden können
        def __init__(self, mannschaft_1, mannschaft_2, punkte_mannschaft_1=None, punkte_mannschaft_2=None):
            self.mannschaft_1 = mannschaft_1
            self.punkte_mannschaft_1 = punkte_mannschaft_1
            self.mannschaft_2 = mannschaft_2
            self.punkte_mannschaft_2 = punkte_mannschaft_2

        def __str__(self):
            # wenn punkte none ist, schmeisst anderes fehler, deswegen nur ausgabe von mannschaften
            if self.punkte_mannschaft_1 is None or self.punkte_mannschaft_2 is None:
                return self.mannschaft_1 + ' ' + self.mannschaft_2
            return self.mannschaft_1 + ' ' + self.punkte_mannschaft_1 + ' : ' + self.punkte_mannschaft_2 + ' ' + self.mannschaft_2

    # hier werden später alle gescrapten spiele gespeichert
    games = []
    # definieren parameter
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=2000,2000")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # initialisieren des treibers, öffnen des browsers
    driver = webdriver.Chrome(PATH, options=chrome_options)
    # driver = webdriver.Chrome()
    # öffnen der webseite
    driver.get(url)
    # warten, bis klasse mit spielingel
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nfl-c-matchup-strip__game"))
    )
    articles = driver.find_elements_by_class_name("nfl-c-matchup-strip__game")

    # print('Amount of articles:', len(articles), '\n--------------------------------')

    for i in range(int(len(articles))):
        # print(articles[i].text.replace('\n', " "))
        # schaut, ob gefundener Artikel im richtigen Format ist
        # beispiel '38 Seahawks (12-4) 25 Falcons (4-12)'
        regex = re.search('(\d+)\s([\D\d]+)\s[(\d-]+[)]\s(\d+)\s([\D\d]+)\s[(\d-]+[)]',
                          articles[i].text.replace('\n', " "))
        # wenn regex matched, Game objekt erstellen und in Array packen
        if regex:
            g = Game(regex.group(2), regex.group(4), regex.group(1), regex.group(3))
            games.append(g)
        else:
            # schaut, ob gefundener Artikel im richtigen Format ist
            # beispiel 'Seahawks (12-4) Falcons (4-12)'
            regex = re.search('([\D\d]+)\s[(\d-]+[)]\s([\D\d]+)\s[(\d-]+[)]', articles[i].text.replace('\n', " "))
            # wenn regex matched, Game objekt erstellen und in Array packen
            if regex:
                g = Game(regex.group(1), regex.group(2))
                games.append(g)
            else:
                # schaut, ob gefundener Artikel im richtigen Format ist
                # beispiel 'Seahawks Falcons'
                regex = re.search('([\D\d]+)\s([\D\d]+)', articles[i].text.replace('\n', " "))
                # wenn regex matched, Game objekt erstellen und in Array packen
                if regex:
                    g = Game(regex.group(1), regex.group(2))
                    games.append(g)
    # webseite zumachen
    driver.quit()
    return games


# scraped die dropdownfelder auf der webseite, wo man jahr und woche auswaehlen kann
def scrape_options(url="https://www.nfl.com/schedules/2021/REG1/"):
    # definiern parameter
    chrome_options = webdriver.ChromeOptions()
    # kein fenster oeffnen, wichtig fuer raspberry
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    # grosses virtuelles fenster, sodass volle mannschaftsnamen angezeigt werden
    chrome_options.add_argument("--window-size=2000,2000")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # initialisieren des treibers, öffnen des browsers
    driver = webdriver.Chrome(PATH, options=chrome_options)
    # driver = webdriver.Chrome()
    # öffnen der webseite
    driver.get(url)
    # warten, bis dropdownfeld mit werten gefuellt ist
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "d3-o-dropdown"))
    )

    dropdown_values = []
    dropdown = driver.find_elements_by_class_name("d3-o-dropdown")
    print('Amount of articles:', len(dropdown), '\n--------------------------------')
    for d in dropdown:
        # print(d.text)
        dropdown_values.append(d.text)

    # komischer code, das funktioniert
    # selector = Select(dropdown[0])

    # das nicht, sind aber 2 elemente drin
    # selector = Select(dropdown[1])

    # Waiting for the values to load
    # element = WebDriverWait(driver,
    #                        10).until(EC.element_to_be_selected(selector.options[0]))

    # options = selector.options
    # for o in options:
    #    print(o.text)

    # formatieren der dropdownvalues
    years = dropdown_values[0].split('\n')
    weeks = dropdown_values[1].split('\n')
    # print(len(dropdown_values))

    # webseite zumachen
    driver.quit()
    return years, weeks


if __name__ == '__main__':
    games = scrape("https://www.nfl.com/schedules/2021/REG2/")

    years, weeks = scrape_options()
    print('Amount of years: ', len(years))
    print('Amount of weeks: ', len(weeks))
    for y in years:
        print(y)

    for w in weeks:
        print(w)

    for g in games:
        print(g)
