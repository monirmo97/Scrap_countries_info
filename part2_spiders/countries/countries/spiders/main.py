import scrapy
import csv
import pandas as pd


class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = ["https://www.currencyremitapp.com/world-currency-symbols"]
    read_data_path = "countries.csv"
    clean_data_path = "clean_countries.csv"

    def get_countries(self):
        with open(self.clean_data_path, "r") as countries:
            header = next(countries)
            headers = header.strip().split(',')
            reader = csv.reader(countries)
            for row in reader:
                row_dict = {}
                for i, h in enumerate(headers):
                    row_dict[h] = row[i]
                yield row_dict

    def format_links(self, link):
        if not (link.startswith('http') or (link.startswith('https'))):
            return 'https://'+link
        else:
            return link

    def clean_data(self, data_frame):
        print(data_frame)

        # Drop rows with NaN missing value
        data_frame.dropna(inplace=True)

        # Remove duplicates rows
        data_frame.drop_duplicates(inplace=True)

        # Standardize formats of links
        data_frame['Flag Link'] = data_frame['Flag Link'].apply(
            self.format_links)

        # Remove unwanted characters in 'Page Title'
        for column in data_frame.columns:
            data_frame[f"{column}"] = data_frame[f"{column}"].str.strip()

        return data_frame

    def parse(self, response):
        # Extract information from the URL
        countries = response.xpath('//table/tbody/tr')

        # Open csv file
        with open(self.read_data_path, 'w', newline='', encoding='utf-8') as csvfile:
            column_names = ['Name', 'Code', 'Symbol',
                            'Flag Link', 'Currency']
            writer = csv.DictWriter(csvfile, fieldnames=column_names)

            # Write the headers of the CSV file
            writer.writeheader()

            # Write data to the CSV file
            for country in countries:
                data = {
                    'Name': country.xpath('.//td[2]/text()').get(),
                    'Code': country.xpath('.//td[4]/text()').get(),
                    'Symbol': country.xpath('.//td[5]/text()').get(),
                    'Flag Link': country.xpath('.//td[1]/img/@src').get(),
                    'Currency': country.xpath('.//td[3]/text()').get(),
                }

                writer.writerow(data)

        data_frame = pd.read_csv(f"{self.read_data_path}")
        data_frame = self.clean_data(data_frame)

        print(data_frame.to_string(index=False))

        data_frame.to_csv(f"{self.clean_data_path}", index=False)

        for item in self.get_countries():
            print(f"{item}")
        
