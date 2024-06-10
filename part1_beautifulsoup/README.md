# Web Scraping and Data Cleaning Script

This Python script performs web scraping on a given website, extracts information such as page title, links in the body, and headings, and then saves the data in JSON format. Additionally, the script cleans the data, standardizes link formats, and removes duplicates.

## Prerequisites

- Python 3.x
- Required Python libraries can be installed using:

  ```bash
  pip install requests beautifulsoup4 pandas

## Usage
Run this code:
'python main.py'

## Functionality

get_page_info(address):
Fetches information from the specified web page, including page title, links in the body, and headings.

save_json(data, path_output_file):
Saves the provided data in JSON format to the specified output file.

read_json(file_path):
Reads JSON data from the specified file.

format_links(links):
Standardizes the formats of links by ensuring they start with "http://" if not already.

clean_data(data_frame):
Cleans the DataFrame by converting 'Links in Body' to a list, exploding the DataFrame to separate links, removing duplicates, and standardizing link formats.

main():
The main function where the user provides input and the entire process is orchestrated.