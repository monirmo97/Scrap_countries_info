This code allows users to retrieve information about countries, save user inputs, and generate reports.

Usage:

-Get Country Information

    To get information about a specific country, run the script with the -n option followed by the name of the country.
    'python main.py -n [country_name]'

-Save User Input
    To save a user's input (country name), run the script with the python 
    'main.py -n [country_name]'

-Show User Input Report
    To generate a report of user inputs, run the script with the -r or --report option.
    'python main.py -r'

Additional Information:

-The script uses the file clean_countries.csv as the source for country information.
-User inputs are saved in a log file named log.csv.
-The code provides case-insensitive matching for country names.
-If the specified CSV file or log file does not exist, appropriate messages will be displayed.

Requirements

-Python 3.x
-Pandas