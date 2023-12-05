# Finding no. of pages
page_countall = driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div/div')
count_pages = page_countall.find_elements(By.TAG_NAME, 'a')
page_count = int(count_pages[-1].text)
print(page_count)