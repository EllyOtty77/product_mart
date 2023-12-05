# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re
import locale

# Configuring Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.get('https://www.digitalstore.co.ke/collections/laptops')
time.sleep(5)

# Extracting and storing data to variable objects
Title = []
Brand = []
Price = []
Link = []

locale.setlocale(locale.LC_ALL, 'en_KE.UTF-8')

# Data extraction
titles = driver.find_elements(By.XPATH, '/html/body/main/div[1]/section/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/a[1]')
for title in titles:
    Title.append(title.text)

brands = driver.find_elements(By.XPATH, '/html/body/main/div[1]/section/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/a[2]')
for brand in brands:
    Brand.append(brand.text)

prices = driver.find_elements(By.XPATH, '/html/body/main/div[1]/section/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/span[1]')
for price in prices:
    # Use regular expression to extract only digits
    numeric_price = float(re.sub(r'[^\d.]', '', price.text))
    formatted_price = locale.currency(numeric_price, grouping=True)
    Price.append(formatted_price)

links = driver.find_elements(By.XPATH, '/html/body/main/div[1]/section/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/a[1]')
for link in links:
    Link.append(link.get_attribute('href'))


# Creating a DataFrame and saving it to a CSV file
data = {'Title': Title, 'Brand': Brand, 'Price': Price, 'Link': Link}
df = pd.DataFrame(data)
df.to_csv('smart_data.csv', index=True)

# Closing the WebDriver
driver.quit()
