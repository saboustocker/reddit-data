# article class="w-full m-0"

# inside: <a> with slot="full-post-link" contains a href - i want that
# also inside article: span slot="credit-bar" -> I want the full HTML in there

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def create_driver(headless=False):
    """Create and return a Chrome WebDriver instance."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

    service = Service()  # Automatically finds your ChromeDriver (if Selenium ≥ 4.6)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_example():
    driver = create_driver(headless=False)

    try:
        url = "https://example.com"
        driver.get(url)

        # Wait for example element
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        print("Page Title:", driver.title)
        print("H1 text:", element.text)

        # Example scraping multiple elements
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for p in paragraphs:
            print("Paragraph:", p.text)

    except Exception as e:
        print("Error:", e)

    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    scrape_example()
