import unittest
from unittest.mock import patch, MagicMock
# importuojamas patch, kad būtų galima imituoti funkcijas ir klases
# taip pat MagicMock, kad būtų galima sukurti objekto imitacija
# importuojamas os, kad būtų galima patikrinti ar sukurtas CSV failas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arnoldas_a_mod1_atsiskaitymas.book_info import book_info

class TestBookInfo(unittest.TestCase):
    # webdriver pakeistas mock objektu
    @patch('arnoldas_a_mod1_atsiskaitymas.book_info.webdriver.Chrome')
    # tikrinama ar teisingai surenkami duomenys apie knygas
    def test_book_info(self, mock_chrome):
        # sukuriamas MagicMock, kuris imituoja naršyklės veikimą
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # sukuriami mock elementai, kurie simuliuoja kygų informaciją
        # side_effect leidžia simuliuoti kelis elementus
        mock_element1 = MagicMock()
        mock_element1.find_element.side_effect = [
            MagicMock(text="A Light in the Attic"),
            MagicMock(text="£51.77"),
            # testuojant rodoma klaida dėl reitingo, book_rating grazina MagicMoc objeką
            # vietoje tikrosios reiksmes
            MagicMock(get_dom_attribute=lambda name: "star-rating Three"),
        ]
        mock_element2 = MagicMock()
        mock_element2.find_element.side_effect = [
            MagicMock(text="Tipping the Velvet"),
            MagicMock(text="£53.74"),
            MagicMock(get_dom_attribute=lambda name: "star-rating One"),
        ]
        mock_element3 = MagicMock()
        mock_element3.find_element.side_effect = [
            MagicMock(text="Soumission"),
            MagicMock(text="£50.10"),
            MagicMock(get_dom_attribute=lambda name: "star-rating One"),
        ]
        mock_element4 = MagicMock()
        mock_element4.find_element.side_effect = [
            MagicMock(text="Sharp Objects"),
            MagicMock(text="£47.82"),
            MagicMock(get_dom_attribute=lambda name: "star-rating Four"),
        ]
        mock_element5 = MagicMock()
        mock_element5.find_element.side_effect = [
            MagicMock(text="Sapiens: A Brief History of Humankind"),
            MagicMock(text="£54.23"),
            MagicMock(get_dom_attribute=lambda name: "star-rating Five"),
        ]

        mock_driver.find_elements.return_value = [mock_element1, mock_element2, mock_element3, mock_element4, mock_element5]

        # nurodoma kokio rezultato tikimasi
        expected = [
            {"book_title": "A Light in the Attic", "book_price": "£51.77", "book_rating": "Three"},
            {"book_title": "Tipping the Velvet", "book_price": "£53.74", "book_rating": "One"},
            {"book_title": "Soumission", "book_price": "£50.10", "book_rating": "One"},
            {"book_title": "Sharp Objects", "book_price": "£47.82", "book_rating": "Four"},
            {"book_title": "Sapiens: A Brief History of Humankind", "book_price": "£54.23", "book_rating": "Five"},
        ]
        # grąžinamas rezultatas ir tikrinamas ar sutampa su tuo, ko tikimės
        result = book_info()
        self.assertEqual(result, expected)


    @patch('arnoldas_a_mod1_atsiskaitymas.book_info.webdriver.Chrome')
    @patch('arnoldas_a_mod1_atsiskaitymas.book_info.WebDriverWait')
    # tikrinama kaip funckija veiks, jei nėra knygų
    def test_no_books(self, mock_wait, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # simuliuojama, kad nerandama jokių elementų ir grąžinamas tuščias sarašas
        mock_wait.return_value.until.return_value = True
        mock_driver.find_elements.return_value = []

        # tikrinama, kai nėra duomenų ar grąžinamas tuščias sąrašas
        result = book_info()
        self.assertEqual(result, [])

    @patch('arnoldas_a_mod1_atsiskaitymas.book_info.webdriver.Chrome')
    # testuojama ar buvo sukurtas CSV failas
    def test_book_csv(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        mock_element = MagicMock()
        mock_element.find_element.side_effect = [
            MagicMock(text="A Light in the Attic"),
            MagicMock(text="£51.77"),
            MagicMock(get_attribute=lambda name: "star-rating Three"),
        ]
        mock_driver.find_elements.return_value = [mock_element]

        csv_file = 'test_book_info.csv'
        book_info(csv_file)

        # patikrinama ar CSV failas egzistuoja
        self.assertTrue(os.path.exists(csv_file), "CSV failas nebuvo sukurtas")

if __name__ == '__main__':
        unittest.main()
