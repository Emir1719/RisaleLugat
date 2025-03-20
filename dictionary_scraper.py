from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_dictionary_entries(url):
    try:
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Get the page
        driver.get(url)
        
        # Wait for the content to load
        time.sleep(5)  # Give some time for JavaScript to render
        
        # Get the page source after JavaScript has rendered
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all dictionary entries
        dictionary_entries = soup.find_all('span', class_='dictionary')
        
        # Process and format the entries
        formatted_entries = []
        for entry in dictionary_entries:
            # Get the text content
            text = entry.get_text()
            # Split by colon and clean up
            parts = text.split(':', 1)
            if len(parts) == 2:
                word = parts[0].strip()
                meaning = parts[1].strip()
                formatted_entries.append(f"{word}: {meaning}")
        
        # Close the browser
        driver.quit()
        return formatted_entries
    
    except Exception as e:
        print(f"Error: {e}")
        if 'driver' in locals():
            driver.quit()
        return []

def main():
    url = "http://www.erisale.com/#content.tr.11.17"
    entries = get_dictionary_entries(url)
    
    if not entries:
        print("Veri bulunamadı!")
    else:
        print(f"Toplam {len(entries)} kelime bulundu:")
        for entry in entries:
            print(entry)

if __name__ == "__main__":
    main() 