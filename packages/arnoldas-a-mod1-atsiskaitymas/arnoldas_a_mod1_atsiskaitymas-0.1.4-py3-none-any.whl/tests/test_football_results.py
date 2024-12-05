import unittest
from unittest.mock import patch, MagicMock
# importuojamas patch, kad būtų galima imituoti funkcijas ir klases
# taip pat MagicMock, kad būtų galima sukurti objekto imitacija
import os
# importuojamas os, kad būtų galima patikrinti ar sukurtas CSV failas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arnoldas_a_mod1_atsiskaitymas.football_results import football_results

class TestFootballResults(unittest.TestCase):
    # webdriver ir WebDriverWait pakeisti mock objektais
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.webdriver.Chrome')
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.WebDriverWait')
    # testuojama ar svetainę buvo atidaryta, mcok_chrome imituoja webdriver, mock_wait imituoja WebDriverWait
    def test_website_load(self, mock_wait, mock_chrome):
        #sukuriamas MagicMock, kuris imituoja naršyklės veikimą
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # imituojamas spaudžiamas elementas, kuris realaus veiksmo neatlieka
        mock_element = MagicMock()
        mock_element.click.return_value = None
        mock_wait.return_value.until.return_value = mock_element

        football_results()

        # patikrinama ar URL buvo iškviestas kartą ir ar su tinkamu URL
        mock_driver.get.assert_called_once_with('https://www.adamchoi.co.uk/overs/detailed')

    # prieš kiekvieną funkciją tenka naudoti tuos pačius patch, nes kitaip funkcija neveikia
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.webdriver.Chrome')
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.WebDriverWait')
    # patikrinama ar buvo paspaustas "All Matches" mygtukas
    def test_click_all_matches(self, mock_wait, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        mock_element = MagicMock()
        mock_element.click.return_value = None
        mock_wait.return_value.until.return_value = mock_element

        football_results()

        mock_element.click.assert_called_once()


    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.webdriver.Chrome')
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.WebDriverWait')
    # testuojama ar duomenų surinkimas yra teisingas
    def test_football_results(self, mock_wait, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        mock_element = MagicMock()
        mock_element.click.return_value = None

        mock_wait.return_value.until.return_value = mock_element

        # simuliuojamos lentelės eilės "tr"
        mock_row1 = MagicMock()
        # simuliuojami "td" elementai
        mock_row1.find_elements.return_value = [
            MagicMock(text="2024-11-01"),
            MagicMock(text="Team A"),
            MagicMock(text="1-0"),
            MagicMock(text="Team B"),
        ]
        mock_row2 = MagicMock()
        mock_row2.find_elements.return_value = [
            MagicMock(text="2024-11-02"),
            MagicMock(text="Team C"),
            MagicMock(text="2-2"),
            MagicMock(text="Team D"),
        ]
        mock_driver.find_elements.return_value = [mock_row1, mock_row2]

        # atidaromas URL, paspaudžiama "All Matches" ir gražinamos eilutės mock_row 1 ir 2
        football_results()

    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.webdriver.Chrome')
    @patch('arnoldas_a_mod1_atsiskaitymas.football_results.WebDriverWait')
    # testuojama ar buvo sukurtas CSV failas
    def test_football_csv(self, mock_wait, mock_chrome):

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver


        mock_element = MagicMock()
        mock_element.click.return_value = None
        mock_wait.return_value.until.return_value = mock_element


        football_results()

        # patikrinama ar CSV failas egzistuoja
        self.assertTrue(os.path.exists('football_results.csv'), "CSV failas nebuvo sukurtas")


if __name__ == '__main__':
    unittest.main()
