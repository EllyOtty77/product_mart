import requests
from bs4 import BeautifulSoup

price = []
product_name = []
available = []
product_link = []
description = []

url = 'https://www.digitalstore.co.ke/collections/iphones-ipads'
r = requests.get(url)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find('div', {'class': 'product-list product-list--collection product-list--with-sidebar'})
    products = data.find_all('div', {'class': 'product-item__info'})

    for i in products:
        sale_price = i.find('span', {'class': 'price price--highlight'})
        if sale_price:
            # Remove the 'Sale price' text and any non-digit characters
            price_text = sale_price.text.strip().replace('Sale price', '').replace('KSh', '').replace(',', '')
            # Convert the price to an integer or float, depending on the format
            cost = float(price_text) if '.' in price_text else int(price_text)
            price.append(cost)

        name = i.find('a', {'class': 'product-item__title text--strong link'})
        product_name.append(name.text.strip())

        stock = i.find('span', {'class': 'product-item__inventory inventory inventory--high'})
        available.append(stock.text.strip())

        link = i.find('a', {'class': 'product-item__title text--strong link'})
        link_text = link.get('href')
        product_link.append(f'https://www.digitalstore.co.ke{link_text}')

else:
    print("Failed to retrieve the webpage. Status code:", r.status_code)

