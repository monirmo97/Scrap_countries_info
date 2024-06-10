import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get information of page
def get_page_info(address):
    response = requests.get(address)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get page title
    page_title = soup.title.text

    # Get links of the page
    body_links = []
    for link in soup.find_all('a', href=True):
        body_links.append(link['href'])

    # Get value of tags 1h to 6h (without attribute)
    headings = {}
    for i in range(1, 7):
        heading = soup.find('h' + str(i))
        if heading:
            headings['h' + str(i)] = heading.text

    # Create a dictionary
    page_info = {
        'Page Title': page_title,
        'Links in Body': body_links,
        'Headings': headings
    }

    return page_info


# Save function
def save_json(data, path_output_file):
    with open(path_output_file, 'w') as json_file:
        json.dump(data, json_file)


# Load function
def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return pd.DataFrame([data])

# Standardize formats of links
def format_links(link):
    if not (link.startswith('http') or (link.startswith('https'))):
        return 'https://'+link
    else:
        return link


def clean_data(data_frame):
    # Convert 'Links in Body' to list if not already
    data_frame['Links in Body'] = data_frame['Links in Body'].apply(
        lambda x: x if isinstance(x, list) else [x]
    )

    # explode method to separate links
    explode_data_frame = data_frame.explode('Links in Body')

    # Drop rows with NaN missing value
    explode_data_frame.dropna(inplace=True)

    explode_data_frame['Links in Body'] = explode_data_frame['Links in Body'].astype(
        str)
    explode_data_frame['Headings'] = explode_data_frame['Headings'].astype(str)

    # Remove duplicates rows
    explode_data_frame.drop_duplicates(inplace=True)

    # Standardize formats of links
    explode_data_frame['Links in Body'] = explode_data_frame['Links in Body'].apply(
        format_links)

    # Remove unwanted characters in 'Page Title'
    explode_data_frame['Page Title'] = explode_data_frame['Page Title'].str.strip()

    return explode_data_frame

# Main function
def main():

    try:
        # Get input address from the user
        address = input('Enter the address: ')

        # Get save address from the user
        output_path = input('Enter the address to save json file: ')

        # check inputs
        if not address or not output_path:
            raise ValueError('The inputs are not valid')

        # Call the get_page_info function
        page_info = get_page_info(address)

        # Save in json file
        save_json(page_info, output_path)

        # Load from json file
        data_loaded = read_json(output_path)

        # Clean Data
        data_loaded = clean_data(data_loaded)

        # Save clean data
        output_path_clean_data = input('Enter the cleaned output file path: ')
        data_loaded.to_json(output_path_clean_data,
                            orient='records', lines=True)

        print('Data saved successfully!')

    except Exception as e:
        print('An error occurred:', str(e))


if __name__ == '__main__':
    main()
