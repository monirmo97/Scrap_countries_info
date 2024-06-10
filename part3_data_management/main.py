import pandas as pd
import argparse
import os


# Save user input
def save_user_input(csv_file, country_name, dataset):
    # Convert the 'Name' column in the dataset to lowercase for case-insensitive comparison
    dataset_lower = dataset['Name'].str.lower()

    # Check if the user's input is in the dataset
    if country_name.lower() in dataset_lower.values:
        # Save the user's input to the CSV file
        if not os.path.exists(csv_file):
            user_input_df = pd.DataFrame({'Name': [country_name.lower()]})
            user_input_df.to_csv(csv_file, mode='a', index=False)
            return
        user_input_df = pd.DataFrame({'Name': [country_name.lower()]})
        # Append user input to the CSV file
        user_input_df.to_csv(csv_file, mode='a', index=False, header=False)


# Counter user input
def count_user_input(csv_file):
    if not os.path.exists(csv_file):
        print("Report file not exist")
        return
    # Read the user input CSV file
    user_input_df = pd.read_csv(csv_file)

    # Count occurrences of each country in the user input file
    user_input_counts = user_input_df['Name'].value_counts()

    # Print the user input report
    for country, count in user_input_counts.items():
        print(f"{country}:{count}")


# Print country information
def print_country_info(country_data, country_name):
    # Convert country names to lowercase for case-insensitive comparison
    country_data['Name'] = country_data['Name'].str.lower()

    # Check there is country or not
    country_info = country_data[country_data['Name'] == country_name]

    if not country_info.empty:
        # Print country information
        print(country_info.to_dict(orient='records')[0])
        return True
    else:
        # Print error message if country not found
        print(f"Error: Country '{country_name}' not found.")
        return False


def main():

    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description='Get country information')
        parser.add_argument(
            '-r', '--report', action='store_true', help='Show user input report')
        parser.add_argument('-n', '--country_name',
                            help='Name of the country (case-insensitive)')

        args = parser.parse_args()

        file_path = 'clean_countries.csv'
        log_path = "log.csv"

        if args.country_name:
            if not os.path.exists(file_path):
                print("file not exist")
                return
            # Read csv file
            country_data = pd.read_csv(file_path)

            # Get the country name from command-line arguments
            country_name = args.country_name.lower()

            # Print country information
            if print_country_info(country_data, country_name):
                save_user_input(log_path, country_name, country_data)

        if (args.report):
            # Count user input
            count_user_input(log_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()

