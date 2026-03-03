import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class FlipkartScraper:
    def __init__(self, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.reviews_data = []
        self.seen_reviews = set() # Prevent duplicates

    def get_product_metadata(self, url):
        pid_match = re.search(r'pid=([^&]+)', url)
        product_id = pid_match.group(1) if pid_match else "Unknown_ID"
        title = self.driver.title
        product_name = title.split('Reviews')[0].strip() if 'Reviews' in title else title.split('-')[0].strip()
        return product_name, product_id


    def extract_visible_reviews(self, product_name, product_id):
        verified_badges = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Verified Purchase')]")
        
        for badge in verified_badges:
            try:
                # Traverse up 7 levels to capture the entire review block
                card = badge
                for _ in range(7):
                    card = card.find_element(By.XPATH, "..")
                    
                raw_text = card.text
                if not raw_text or raw_text in self.seen_reviews:
                    continue
                self.seen_reviews.add(raw_text)

                lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
                
                # 1. Extract Rating (Looking for a number 1-5, optionally with a decimal or star)
                rating = None
                for line in lines[:5]:
                    if re.match(r'^[1-5](\.[0-9])?\s*★?$', line):
                        rating = re.sub(r'[^\d.]', '', line)
                        break
                
                # 2. Extract Date
                review_date = None
                for line in reversed(lines):
                    if '·' in line or '202' in line or 'ago' in line:
                        review_date = line
                        break

                # 3. Extract Text
                try:
                    vp_idx = next(i for i, line in enumerate(lines) if "Verified Purchase" in line)
                    body_lines = lines[1:vp_idx] # Body is usually between the rating and the VP badge
                    
                    clean_body = []
                    for l in body_lines:
                        # Skip UI noise
                        if l.startswith('Review for:') or l.startswith('Helpful for') or l == 'READ MORE' or re.match(r'^\d+$', l):
                            continue
                        clean_body.append(l)
                        
                    # Remove trailing short lines (likely reviewer name/location)
                    while clean_body and len(clean_body[-1]) < 20 and not clean_body[-1].endswith('.'):
                        clean_body.pop()
                        
                    review_text = " ".join(clean_body).strip()
                except Exception:
                    review_text = " ".join(lines) # Fallback if structure is weird

                if review_text or rating:
                    self.reviews_data.append({
                        "Product Name": product_name,
                        "Product ID": product_id,
                        "Review Text": review_text,
                        "Review Rating": rating,
                        "Review Date": review_date,
                        "Reviewer Verified": True
                    })
            except Exception as e:
                continue

    def run(self, url, target_review_count=100):
        print(f"Starting scraper for: {url}\n")
        self.driver.get(url)
        time.sleep(3) 
        
        product_name, product_id = self.get_product_metadata(url)
        print(f"Product: {product_name} | PID: {product_id}\n")

        while len(self.reviews_data) < target_review_count:
            print(f"Extracting... Current count: {len(self.reviews_data)}")
            self.extract_visible_reviews(product_name, product_id)
            
            # Find the last Verified Purchase badge and trigger the Intersection Observer
            badges = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Verified Purchase')]")
            if not badges:
                break
                
            last_badge = badges[-1]
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", last_badge)
                self.driver.execute_script("window.scrollBy(0, 300);") # Nudge it slightly
            except:
                pass
                
            time.sleep(3) # Wait for network API to load new data
            
            # Check if we are stuck at the bottom
            new_badges = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Verified Purchase')]")
            if len(new_badges) == len(badges):
                print("Reached the end of the infinite scroll.")
                break

        self.driver.quit()
        print(f"\nScraping complete. Collected {len(self.reviews_data)} reviews.")

    def save_to_csv(self, filename):
        if not self.reviews_data:
            print("No data to save.")
            return
        df = pd.DataFrame(self.reviews_data)
        df.to_csv(f"data/raw/{filename}", index=False)
        print(f"Data successfully saved to data/raw/{filename}")

if __name__ == "__main__":
    TARGET_URL = input("Enter the Flipkart product reviews URL: ")
    target_review_count = int(input("Enter the number of reviews to scrape: "))
    scraper = FlipkartScraper(headless=True)
    scraper.run(TARGET_URL, target_review_count) 
    filename = input("Enter the filename to save the reviews (e.g., reviews.csv): ")
    scraper.save_to_csv(filename)