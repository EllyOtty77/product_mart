from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML file
with open('Amazon.com_laptops.html', 'r', encoding='utf-8') as file:
    html = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all divs with the specified class
product_divs = soup.find_all('div', {'class': 'puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v1k579acibq3g12dxe3xrr3x1qq s-latency-cf-section puis-card-border'})

# Initialize empty lists for data
product_name = []
product_price = []
delivery_date = []
product_link = []

# Extract data from each div
for div in product_divs:
    # Product name
    name_span = div.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
    if name_span:
        product_name.append(name_span.text.strip())
    else:
        product_name.append(' ')

    # Product price
    price_span = div.find('span', {'class': 'a-price-whole'})
    if price_span:
        product_price.append(price_span.text.strip())
    else:
        product_price.append(' ')

    # Delivery date
    date_span = div.find('span', {'class': 'a-color-base a-text-bold'})
    if date_span:
        delivery_date.append(date_span.text.strip())
    else:
        delivery_date.append(' ')

    # Product link
    link_a = div.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
    if link_a:
        product_link.append(link_a)
    else:
        product_link.append(' ')

# Create a dictionary with the extracted data
data = {
    'Product Name': product_name,
    'Product Price': product_price,
    'Delivery Date': delivery_date,
    'Product Link': product_link
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
# print(df)

df.to_excel('Amzlaptops1.xlsx', index=False)