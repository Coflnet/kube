import datetime
from tabelle.models import Saison, Spielwoche, Spiel, Mannschaft
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

    def __repr__(self):
        return str(self)


class Gameweek:
    # quasi eine spielwoche mit daten wie in db, aber spiele in array statt referenz aum spielwochen_id
    def __init__(self, wochen_name, saison_iid, start_datum, end_datum):
        self.wochen_name = wochen_name
        self.start_datum = start_datum
        self.end_datum = end_datum
        self.saion_iid = saison_iid
        self.games = []

    def __str__(self):
        return 'Ausgabe einer Kompletten Woche' + \
               '\nWeek name  : ' + str(self.wochen_name) + \
               '\nSaison name: ' + str(self.saion_iid) + \
               '\nstart date : ' + str(self.start_datum) + \
               '\nend date   : ' + str(self.end_datum) + str(self.games)


class Season:
    def __init__(self, name, startdate=None, enddate=None):
        self.name = name
        self.startdate = startdate
        self.enddate = enddate
        weeks = []


def scrape(url):
    # hier werden später alle gescrapten spiele gespeichert
    games = []
    driver = create_driver()
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
        g = create_game_objekt(articles[i].text.replace('\n', " "))
        if type(g) == Game:
            games.append(g)
    # webseite zumachen
    driver.quit()
    return games


def create_game_objekt(strip):
    # print(articles[i].text.replace('\n', " "))
    # schaut, ob gefundener Artikel im richtigen Format ist
    # beispiel '38 Seahawks (12-4) 25 Falcons (4-12)'
    regex = re.search('(\d+)\s([\D\d]+)\s[(\d-]+[)]\s(\d+)\s([\D\d]+)\s[(\d-]+[)]', strip)
    # wenn regex matched, Game objekt erstellen und in Array packen
    if regex:
        g = Game(regex.group(2), regex.group(4), regex.group(1), regex.group(3))
    else:
        # schaut, ob gefundener Artikel im richtigen Format ist
        # beispiel 'Seahawks (12-4) Falcons (4-12)'
        regex = re.search('([\D\d]+)\s[(\d-]+[)]\s([\D\d]+)\s[(\d-]+[)]', strip)
        # wenn regex matched, Game objekt erstellen und in Array packen
        if regex:
            g = Game(regex.group(1), regex.group(2))
        else:
            # schaut, ob gefundener Artikel im richtigen Format ist
            # beispiel 'Seahawks Falcons'
            regex = re.search('([\D\d]+)\s([\D\d]+)', strip)
            # wenn regex matched, Game objekt erstellen und in Array packen
            if regex:
                g = Game(regex.group(1), regex.group(2))
    if g:
        return g


def create_date(date_string, jahr):
    jahr = int(jahr)
    if date_string == 'GAMES NOT YET SCHEDULED':
        return
    regex = re.search('^[A-Z]+, ([A-Z]+) (\d+)[A-Z]+$', date_string)
    if regex:
        monat_start, tag_start = regex.group(1), int(regex.group(2))
        long_month_name = monat_start.lower()
        datetime_object = datetime.datetime.strptime(long_month_name, "%B")
        if datetime_object.month < 6:
            jahr += 1
        datum = datetime.datetime(int(jahr), datetime_object.month, tag_start)
        return datum
    else:
        print(date_string)
        raise Exception('Unable to convert start date' + str(date_string))


def create_driver():
    # definieren parameter
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=2000,2000")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # initialisieren des treibers, öffnen des browsers
    return webdriver.Chrome(PATH, options=chrome_options)


def scrape_wochen_daten(url):
    # scrapen von spieldaten plus daten ueber spezielle woche
    # hier werden später alle gescrapten spiele gespeichert
    games = []
    driver = create_driver()
    # öffnen der webseite
    driver.get(url)
    # warten, bis klasse mit spiel geladen ist
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nfl-c-matchup-strip__game"))
    )
    articles = driver.find_elements_by_class_name("nfl-c-matchup-strip__game")
    for i in range(int(len(articles))):
        g = create_game_objekt(articles[i].text.replace('\n', " "))
        if type(g) == Game:
            games.append(g)

    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nfl-c-content-header__roofline"))
    )
    header = driver.find_elements_by_class_name("nfl-c-content-header__roofline")
    name = header[0].text.split('—')[1].strip()
    jahr = header[0].text.split('—')[0].strip()
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "d3-o-section-title"))
    )
    articles = driver.find_elements_by_class_name("d3-o-section-title")
    datums_daten = []
    for a in articles:
        if a.text.lower() != 'teams on bye' and a.text.lower() != 'GAMES NOT YET SCHEDULED'.lower() and len(a.text) > 3:
            # print(a.text)
            datums_daten.append(a.text)
    datum_start = create_date(datums_daten[0].upper(), jahr)
    datum_end = create_date(datums_daten[len(datums_daten) - 1].upper(), jahr)
    week = Gameweek(name, int(jahr), datum_start, datum_end)
    week.games = games
    print(week)
    # webseite zumachen
    driver.quit()
    return week


def scrape_all():
    year = datetime.datetime.now().year
    years, weeks = scrape_options('https://www.nfl.com/schedules/' + str(year) + '/REG1/')
    print(years)
    urls = []
    spiel_wochen = []
    for w in weeks:
        urls.append('https://www.nfl.com' + str(w))
        if len(urls) == -2:
            break

    for u in urls:
        print('scraping games for ' + u)
        spiel_wochen.append(scrape_wochen_daten(u))
    s = Season(str(year))
    s.weeks = spiel_wochen
    startdate = datetime.datetime(int(s.weeks[0].start_datum.year), 9, 1)
    enddate = datetime.datetime(int(s.weeks[0].start_datum.year + 1), 2, 1)
    s.startdate = startdate
    s.enddate=enddate
    return s


def scrape_options(url="https://www.nfl.com/schedules/2021/REG1/"):
    # scraped die dropdownfelder auf der webseite, wo man jahr und woche auswaehlen kann
    driver = create_driver()
    # öffnen der webseite
    driver.get(url)
    # warten, bis dropdownfeld mit werten gefuellt ist
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "d3-o-dropdown"))
    )

    dropdown = driver.find_elements_by_class_name("d3-o-dropdown")
    print('Amount of articles:', len(dropdown), '\n--------------------------------')

    selector = Select(dropdown[1])
    weeks = []
    options = selector.options
    select_box = driver.find_elements_by_class_name("d3-o-dropdown")[1]
    options = [x for x in select_box.find_elements_by_tag_name("option")]
    for element in options:
        # print(element.get_attribute("value"))
        weeks.append(element.get_attribute("value"))
    # formatieren der dropdownvalues
    years = dropdown[0].text.split('\n')
    # webseite zumachen
    driver.quit()
    return years, weeks


def save_season_to_db(season):

    saison_from_db = Saison.objects.filter(dStart=season.startdate, dEnde=season.enddate)
    if saison_from_db:
        saison_obj = saison_from_db[0]
    else:
        saison_obj = Saison(dStart=season.startdate, dEnde=season.enddate)

    saison_obj.save()

    mannschaften = Mannschaft.objects.all()
    for m in mannschaften:
        print(m.name)

    for w in season.weeks:
        save_woche_to_db(saison_obj, w, mannschaften)


def save_woche_to_db(saison, w, mannschaften):
    if w.wochen_name == "HALL OF FAME" or "PRESEASON" in w.wochen_name:
        return


    spielwoche_from_db = Spielwoche.objects.filter(name=w.wochen_name, saison_fk=saison)
    if spielwoche_from_db:
        g = spielwoche_from_db[0]
        g.start = w.start_datum
        g.ende = w.end_datum
    else:
        g = Spielwoche(name=w.wochen_name,
                       start=w.start_datum,
                       ende=w.end_datum,
                       saison_fk=saison)
    g.save()
    spiele = []

    for s in w.games:
        save_spiel_to_db(mannschaften, s, g)


def save_spiel_to_db(mannschaften, s, g):
    mannschaft1 = Mannschaft.objects.get(name=s.mannschaft_1)
    mannschaft2 = Mannschaft.objects.get(name=s.mannschaft_2)
    spiel_from_db = Spiel.objects.filter(mannschaft1_fk=mannschaft1,
                                         mannschaft2_fk=mannschaft2,
                                         spielwoche_fk=g)
    if spiel_from_db:
        spiel = spiel_from_db[0]
        spiel.mannschaft1_punkte = s.punkte_mannschaft_1
        spiel.mannschaft2_punkte = s.punkte_mannschaft_2
    else:
        spiel = Spiel(mannschaft1_fk=mannschaft1,
                      mannschaft2_fk=mannschaft2,
                      mannschaft1_punkte=s.punkte_mannschaft_1,
                      mannschaft2_punkte=s.punkte_mannschaft_2,
                      spielwoche_fk=g)
    spiel.save()


if __name__ == '__main__':
    # games = scrape("https://www.nfl.com/schedules/2021/REG2/")
    scrape_wochen_daten("https://www.nfl.com/schedules/2021/REG2/")
    # years, weeks = scrape_options()
    # print('Amount of years: ', len(years))
    # print('Amount of weeks: ', len(weeks))
    # for y in years:
    #     print(y)
    scrape_all()
    # for w in weeks:
    #     print(w)

    # for g in games:
    #    print(g)
