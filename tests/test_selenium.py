import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()

        # Configuration pour environnement CI/CD
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Vérifier le titre
        assert "Calculatrice Simple" in driver.title

        # Vérifier la présence des éléments principaux
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Saisir les valeurs
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")

        # Sélectionner l'addition
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")

        # Cliquer sur calculer
        driver.find_element(By.ID, "calculate").click()

        # Vérifier le résultat
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 15" in result.text

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Saisir les valeurs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")

        # Sélectionner la division
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")

        driver.find_element(By.ID, "calculate").click()

        # Vérifier le message d'erreur
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Erreur: Division par zéro" in result.text

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]

        for op, num1, num2, expected in operations:
            # Nettoyer les champs
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num2").clear()

            # Saisir les valeurs
            driver.find_element(By.ID, "num1").send_keys(num1)
            driver.find_element(By.ID, "num2").send_keys(num2)

            # Sélectionner l'opération
            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)

            # Calculer
            driver.find_element(By.ID, "calculate").click()

            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert f"Résultat: {expected}" in result.text
            time.sleep(1)

    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement de la page"""
        import time
        start_time = time.time()

        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Attendre que la page soit complètement chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )

        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")

        # Vérifier que le chargement prend moins de 3 secondes
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_decimal_numbers(self, driver):
        file_path = os.path.abspath("../src/index.html")

        driver.get(f"file://{file_path}")
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("3.19")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2.81")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "Résultat: 6.00" in result.text

    def test_negative_numbers(self, driver):
        file_path = os.path.abspath("../src/index.html")

        driver.get(f"file://{file_path}")
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("-5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("-3")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("subtract")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "Résultat: -2" in result.text

    def test_ui_style(self, driver):
        file_path = os.path.abspath("../src/index.html")

        driver.get(f"file://{file_path}")

        container = driver.find_element(By.CLASS_NAME, "container")
        background = driver.find_element(By.ID, "result").value_of_css_property("background-color")

        assert container.value_of_css_property("max-width") in ("400px", "400")
        assert background in ("rgb(240, 240, 240)", "#f0f0f0")


if __name__ == "__main__":
    pytest.main([
        "-v",
        "--html=report.html",
        "--self-contained-html"
    ])
