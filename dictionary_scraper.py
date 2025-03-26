from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        # time.sleep(5)  # Give some time for JavaScript to render
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

def scrape_pages(start_page, end_page):
    # Create output file
    with open('sozler.txt', 'w', encoding='utf-8') as f:
        for page in range(start_page, end_page + 1):
            url = f"http://www.erisale.com/#content.tr.1.{page}"
            print(f"Sayfa {page} taranıyor...")
            entries = get_dictionary_entries(url)
            # Write page number as header
            f.write(f"\n# {page}\n")
            if entries:
                # Write entries
                for entry in entries:
                    f.write(f"{entry}\n")
            else:
                f.write("Bu sayfada veri bulunamadı.\n")
            # Add a separator between pages
            f.write("\n" + "-"*50 + "\n")
            # time.sleep(2)

def main():
    try:
        start_page = 27
        end_page = 1041
        
        if start_page > end_page:
            print("Hata: Başlangıç sayfası bitiş sayfasından büyük olamaz!")
            return
        print(f"\nSayfa {start_page} ile {end_page} arasındaki kelimeler taranıyor...")
        scrape_pages(start_page, end_page)
        print("\nİşlem tamamlandı! Sonuçlar dosyaya kaydedildi.")
    except ValueError:
        print("Hata: Lütfen geçerli sayılar girin!")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main() 