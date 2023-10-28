import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')


table_data = soup.find('table', {'class': 'wikitable sortable'})

tr_first = table_data.find('tr')
header_tags = tr_first.find_all('th')[:-2]
headers = [title.text.strip() for title in header_tags]
headers.remove('Rank')
if headers[-1] != 'Headquarters':
    headers[-1] = 'Headquarters'

df = pd.DataFrame(columns=headers)

column_data = table_data.find_all('tr')[2:]
for row in column_data:
    row_data = row.find_all('td')[:-2]
    individual_data = [data.text.strip() for data in row_data]
    length = len(df)
    df.loc[length] = individual_data
df.to_excel('Largest_companies.xlsx', index=False)
print('Dataframe saved to excel file')
