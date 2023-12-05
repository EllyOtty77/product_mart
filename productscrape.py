# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# Configuring Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.get('https://glantix.co.ke/')

# Navigating to the laptops section
time.sleep(3)
hoverable_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/ul/li[1]')
ActionChains(driver).move_to_element(hoverable_element).perform()
time.sleep(2)
laptops = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/ul/li[1]/ul/li[3]')
time.sleep(2)
laptops.click()
time.sleep(5)

# Selecting the number of items to display
dropdown_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[3]/select')
dropdown = Select(dropdown_element)
dropdown.select_by_visible_text("28")
time.sleep(5)

# Storage variables
Title = []
Price = []
Link = []

# Scrolling to load additional elements
prev_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    prev_height = new_height

time.sleep(7)

# Extracting data
titles = driver.find_elements(By.XPATH, '//div[5]/div/div[2]/div[1]/a')
for title in titles:
    Title.append(title.get_attribute('title'))

prices = driver.find_elements(By.XPATH, '//div[5]/div/div/2/div[2]/span[1]')
for price in prices:
    Price.append(price.text)

links = driver.find_elements(By.XPATH, '//div[5]/div/div[2]/div[1]/a')
for link in links:
    Link.append(link.get_attribute('href'))



# Creating a DataFrame and saving it to a CSV file
data = {'Title': Title, 'Price': Price, 'Link': Link}
df = pd.DataFrame(data)
df.to_csv('allproduct_data.csv', index=False)

# Closing the WebDriver
driver.quit()
