from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# importuojame webdriver ir Service, kad būtų galima paleisti Chrome naršyklę
from selenium.webdriver.common.by import By
# importuojame by, kad būtų galima ieškoti HTML elementų su xpath
from selenium.webdriver.support.ui import WebDriverWait
# importuotas WebDriverWait, naudojamas laukiant, kol bus įvykdoma tam tikra sąlyga
from selenium.webdriver.support import expected_conditions as EC
# importuotas expected_condition, kuriame aprašytos dažniausiai naudojamos sąlygos
import pandas as pd
# importuojamos pandas, kad būtų gaunamas "švaresnis" rezultatas ir išsaugomas CSV failas

def football_results():
    website = 'https://www.adamchoi.co.uk/overs/detailed'
    # testuojant funkciją, reikia nurodyti tikslią chromedriver vietą
    path = 'C:\\Tools\\chromedriver\\chromedriver.exe'

    # nurodytu URL sukuriamas webdriver objektas, atidarantis naršyklę ir svetainę
    service = Service(path)
    driver = webdriver.Chrome(service=service)

    driver.get(website)

    # laukiama iki 10 s, kol bus atidarytas xpath ir paspaudžiamas "All Matches" mygtukas
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//label[@analytics-event="All matches"]'))
    ).click()

    # tušti sąrašai naudojami surinkti informaciją apie rungtynes
    date = []
    home_team = []
    score = []
    away_team = []

    # surenkama rungtynių informacija esanti eilutėse ("tr" elementai)
    matches = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )

    # pereinama per visas eilutes ir surenkama informacija apie td[0] - td[3] elementus
    # surinka informacija pridedama prie sąrašų. Pridėtas exception, nes neradus informacijos
    # vienoje eilutėje kodas neveikia
    for match in matches:
        try:

            tds = match.find_elements(By.TAG_NAME, 'td')
            if len(tds) >= 4:
                date.append(tds[0].text)
                home_team.append(tds[1].text)
                score.append(tds[2].text)
                away_team.append(tds[3].text)
        except Exception as e:
            print(f"Skipping a row due to an error: {e}")

    # pereinama ir atspausdinama surinkti duomenys
    for i in range(len(date)):
        print(f"Date: {date[i]}, Home Team: {home_team[i]}, Score: {score[i]}, Away Team: {away_team[i]}")

    driver.quit()

    # sukuriama lentelė su sirinktais duomenimis, kuri yra išsaugoma kaip CSV ir atspausdinama
    data_frame = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
    data_frame.to_csv('football_results.csv', index=False)
    print(data_frame)

