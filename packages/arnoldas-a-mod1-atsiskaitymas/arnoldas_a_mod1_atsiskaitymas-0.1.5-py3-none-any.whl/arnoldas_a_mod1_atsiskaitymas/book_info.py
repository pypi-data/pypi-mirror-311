from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# importuojame webdriver ir Service, kad būtų galima paleisti Chrome naršyklę
from selenium.webdriver.common.by import By
# importuojame by, kad būtų galima ieškoti HTML elementų su xpath
from selenium.webdriver.support.ui import WebDriverWait
# importuotas WebDriverWait, naudojamas laukiant, kol bus įvykdoma tam tikra sąlyga
from selenium.webdriver.support import expected_conditions as EC
# importuotas expected_condition, kuriame aprašytos dažniausiai naudojamos sąlygos
from selenium.common.exceptions import TimeoutException
# importuotas TimeoutException, kad būtų galima patikrinti kas vyksta, jei neužkrautų tinklalapio
import pandas as pd
# importuojamos pandas, kad būtų gaunamas "švaresnis" rezultatas ir išsaugomas CSV failas

def book_info(book_info_csv = 'book_info.csv'):
    website = 'https://books.toscrape.com/'
    # testuojant funkciją, reikia nurodyti tikslią chromedriver vietą
    path = 'C:\\Tools\\chromedriver\\chromedriver.exe'

    # nurodytu URL sukuriamas webdriver objektas, atidarantis naršyklę ir svetainę
    service = Service(path)
    driver = webdriver.Chrome(service=service)

    driver.get(website)

    # laukiama iki 10 s, kol bus atidarytas xpath ir atsiras visi knygų elementai
    #TimeoutException grąžina tuščią sąrašą, jei knygų elementai neatsiranda per 10 s
    try:

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article[@class="product_pod"]'))
        )
    except TimeoutException:
        return[]

    all_books = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')

    # tušti sąrašai naudojami surinkti informaciją apie knygų pavadinimus, kainas ir reitingus
    book_title = []
    book_price = []
    book_rating = []

    # pereinama per kiekvieną elementą ir pridedama informacija į tuščius sarašus
    # reitingo klasėje panaudojamas paskutinis elementas, įvardijantis kiek žvaigdžių duodama knygai
    for book in all_books:
        title = book.find_element(By.TAG_NAME, 'h3').text
        price = book.find_element(By.CLASS_NAME, 'price_color').text
        rating_element = book.find_element(By.XPATH, './p[contains(@class, "star-rating")]')
        rating_class = rating_element.get_dom_attribute('class')
        rating = rating_class.split()[-1]
        book_title.append(title)
        book_price.append(price)
        book_rating.append(rating)

    # gražinamas rezultatas, naudojant zip, kuris sujungia pavadinimus, kainas ir reitingus
    # į vieną sąraša. Naudojamas tam, kad vėliau būtų galima patikrinti rezultatus su unittest
    results = [{"book_title": t, "book_price": p, "book_rating": r}
               for t, p, r in zip(book_title, book_price, book_rating)]

    driver.quit()

    # sukuriama lentelė ir išsaugoma CSV formatu
    data_frame = pd.DataFrame(results)
    data_frame.to_csv(book_info_csv, index=False)

    return results
