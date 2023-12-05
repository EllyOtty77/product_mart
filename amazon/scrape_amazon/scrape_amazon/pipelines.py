
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import pyodbc as odbc
from scrapy.exceptions import DropItem
from scrapy import signals

class PricePipeline:
    def process_item(self, item, spider):
        # Extract the 'price' field from the item
        price = item.get('price')

        # Check if the price is not None and is a string
        if price is not None and isinstance(price, str):
            # Remove the dollar sign ($) and any additional formatting
            cleaned_price = re.sub('[^\d.]', '', price)

            # Convert the cleaned price to an integer
            item['price'] = int(float(cleaned_price))

        return item

class SaveToMSSQLPipeline(object):
    def __init__(self, mssql_settings):
        self.mssql_settings = mssql_settings
        self.connection = odbc.connect(DSN=mssql_settings['DSN'], UID=mssql_settings['USERNAME'], PWD=mssql_settings['PASSWORD'])
        self.cursor = self.connection.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(
            mssql_settings=crawler.settings.get('MSSQL_SETTINGS')
        )
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def ensure_table(self, table_name):
        # Check if the table exists, create it if it doesn't
        try:
            self.cursor.execute(f"""
                IF OBJECT_ID('{table_name}', 'U') IS NULL
                CREATE TABLE {table_name} (
                    title NVARCHAR(MAX),
                    price INTEGER,
                    brand NVARCHAR(20),
                    image_url NVARCHAR(MAX),
                    description NVARCHAR(MAX),
                )
            """)
            self.connection.commit()
        except odbc.Error as e:
            self.connection.rollback()
            raise DropItem(f"Failed to ensure table exists: {e}")

    def process_item(self, item, spider):
        table_name = item.get('table_name', 'ProductTable')  # Default table if 'table_name' not provided in the item
        self.ensure_table(table_name)

        try:
            self.cursor.execute(f"""
                INSERT INTO {table_name} (title, price, brand, image_url, description)
                VALUES (?, ?, ?, ?, ?)
            """, item['title'], item['price'], item['brand'], item['image'], item['description'])
            self.connection.commit()
        except odbc.Error as e:
            self.connection.rollback()
            raise DropItem(f"Failed to insert item into MSSQL database: {e}")
        return item

    def spider_closed(self, spider):
        self.connection.close()