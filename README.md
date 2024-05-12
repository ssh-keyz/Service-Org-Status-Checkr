# Status Checkr for Service Organizations

Welcome to the Status Checkr for Service Organizations! This Python-based program is designed to quickly gain oversight on remaining information to be vetted from the San Francisco Service Guide website, specifically focusing on service organizations.

## Features

- Retrieve information such as active status and last vetted date
- Normalize date formats for consistent data representation
- Handle retries and error scenarios gracefully
- Customize the range of pages and filter results based on active status
- Export the data to a CSV file for further analysis and use

## Getting Started

To get started with the Status Checkr for Service Organizations, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Rename the `.env.example` to `.env` provide the following environment variables:
   ```
   BASE_URL=
   END_URL=
   ```
4. Make sure you have the appropriate webdriver installed for your browser (e.g., ChromeDriver for Google Chrome).
5. Run the script using `python update_deactivated_list.py` and follow the prompts.
6. Sit back while the data is saved to a CSV file specified during the setup (organizations.csv is defailt).

## Requirements

- Python 3.x
- Selenium
- python-dotenv

These dependencies are listed in the ```requirements.txt``` file and can be easily installed using ``` pip install -r requirements.txt ```.

## Customization

The Status Checkr for Service Organizations provides flexibility for customization. You can modify the script to adapt to different website structures, add additional data fields, or integrate with other tools and services.

Feel free to explore the codebase and make any necessary adjustments to suit your specific requirements. The script is designed to be modular and easy to understand..

## Contributing

We welcome contributions from the community! If you have any ideas, suggestions, or bug reports, please open an issue on the GitHub repository. If you'd like to contribute code, please fork the repository and submit a pull request with your changes.

## License

The Service Org Status Checkr is open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute the code as per the terms of the license.

