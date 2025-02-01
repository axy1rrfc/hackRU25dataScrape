import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import string

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Prepare CSV file
csv_file = "data/recipes.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Dish Name", "Ingredients"])  # CSV Headers

    # Loop through each letter (A-Z)
    for letter in string.ascii_lowercase:
        url = f"https://www.themealdb.com/browse/letter/{letter}"
        driver.get(url)
        time.sleep(2)  # Allow time for page to load

        # Find all recipe divs (class="col-sm-3")
        recipes = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-3 a")

        for recipe in recipes:
            try:
                # Click on each recipe link
                recipe.click()
                time.sleep(2)

                # Extract dish name (<h2>)
                dish_name = driver.find_element(By.XPATH, '//td[@style="width:35%"]/h2').text
                
                # Extract ingredients (<figcaption>)
                ingredients = [elem.text for elem in driver.find_elements(By.CSS_SELECTOR, "figcaption")]

                # Store in CSV
                writer.writerow([dish_name, ", ".join(ingredients)])

                # Go back to the letter page
                driver.back()
                time.sleep(2)

            except Exception as e:
                print(f"Error scraping recipe: {e}")

# Close the browser
driver.quit()
print(f"Scraping completed. Data saved in {csv_file}")