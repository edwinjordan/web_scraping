"""
Tokopedia Product Scraper
Scrapes product information (name, price, rating) from Tokopedia search results
using Selenium WebDriver in headless mode.
"""

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    """
    Initialize Chrome WebDriver in headless mode.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    print("Initializing Chrome WebDriver...")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Initialize WebDriver with automatic driver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    print("WebDriver initialized successfully")
    return driver


def scrape_data(driver, url, min_products=30):
    """
    Scrape product data from Tokopedia search results.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance
        url (str): URL to scrape
        min_products (int): Minimum number of products to scrape
    
    Returns:
        list: List of dictionaries containing product information
    """
    print(f"Navigating to {url}...")
    driver.get(url)
    
    # Wait for initial page load
    time.sleep(3)
    
    products_data = []
    scroll_pause_time = 2  # Pause between scrolls to avoid bot detection
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    print(f"Starting to scrape products (target: {min_products})...")
    
    while len(products_data) < min_products:
        # Find all product cards on the current page
        try:
            # Common Tokopedia product card selectors
            product_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="master-product-card"], [data-testid="divProductWrapper"]')
            
            if not product_cards:
                # Try alternative selector
                product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[class*="css-"][class*="product"]')
            
            print(f"Found {len(product_cards)} product cards on page")
            
            # Extract data from each product card
            for card in product_cards:
                try:
                    # Extract product name
                    try:
                        name_element = card.find_element(By.CSS_SELECTOR, '[data-testid="spnSRProdName"], [data-testid="linkProductName"]')
                        product_name = name_element.text.strip()
                    except:
                        try:
                            name_element = card.find_element(By.CSS_SELECTOR, 'span[class*="name"], div[class*="name"]')
                            product_name = name_element.text.strip()
                        except:
                            product_name = "N/A"
                    
                    # Extract price
                    try:
                        price_element = card.find_element(By.CSS_SELECTOR, '[data-testid="spnSRProdPrice"], [data-testid="linkProductPrice"]')
                        price = price_element.text.strip()
                    except:
                        try:
                            price_element = card.find_element(By.CSS_SELECTOR, 'span[class*="price"], div[class*="price"]')
                            price = price_element.text.strip()
                        except:
                            price = "N/A"
                    
                    # Extract rating
                    try:
                        rating_element = card.find_element(By.CSS_SELECTOR, '[data-testid="spnSRProdRating"], span[class*="rating"]')
                        rating = rating_element.text.strip()
                    except:
                        rating = "N/A"
                    
                    # Only add if we have at least name and price
                    if product_name != "N/A" and price != "N/A":
                        product_info = {
                            'name': product_name,
                            'price': price,
                            'rating': rating
                        }
                        
                        # Avoid duplicates
                        if product_info not in products_data:
                            products_data.append(product_info)
                            print(f"Scraped product {len(products_data)}: {product_name[:50]}...")
                
                except Exception as e:
                    # Skip problematic cards
                    continue
            
            # Check if we have enough products
            if len(products_data) >= min_products:
                print(f"Target reached: {len(products_data)} products scraped")
                break
            
            # Scroll down to load more products
            print("Scrolling down to load more products...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Break if no more content loads
            if new_height == last_height:
                print("No more content to load")
                break
                
            last_height = new_height
        
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            break
    
    print(f"Scraping completed. Total products: {len(products_data)}")
    return products_data


def save_to_csv(data, filename='tokopedia_products.csv'):
    """
    Save scraped data to a CSV file.
    
    Args:
        data (list): List of dictionaries containing product information
        filename (str): Output CSV filename
    """
    if not data:
        print("No data to save")
        return
    
    print(f"Saving {len(data)} products to {filename}...")
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'price', 'rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Data successfully saved to {filename}")
    
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")


def main():
    """
    Main function to orchestrate the scraping process.
    """
    print("=" * 60)
    print("Tokopedia Product Scraper")
    print("=" * 60)
    
    # Configuration
    url = "https://www.tokopedia.com/search?q=laptop"
    min_products = 30
    output_file = "tokopedia_products.csv"
    
    driver = None
    
    try:
        # Initialize WebDriver
        driver = init_driver()
        
        # Scrape data
        products = scrape_data(driver, url, min_products)
        
        # Save to CSV
        save_to_csv(products, output_file)
        
        print("\n" + "=" * 60)
        print("Scraping completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
    
    finally:
        # Close the browser
        if driver:
            driver.quit()
            print("Browser closed")


if __name__ == "__main__":
    main()
