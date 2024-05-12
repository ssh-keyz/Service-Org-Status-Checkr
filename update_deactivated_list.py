from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time
import re
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("BASE_URL")
end_url = os.getenv("END_URL")

def normalize_date(date_string):
    date_formats = [
        "%m/%d/%Y",  # MM/DD/YYYY
        "%m/%d/%y",  # MM/DD/YY
        "%m-%d-%Y",  # MM-DD-YYYY
        "%m-%d-%y",  # MM-DD-YY
        "%Y/%m/%d",  # YYYY/MM/DD
        "%Y-%m-%d",  # YYYY-MM-DD
        "%b %d, %Y",  # MMM DD, YYYY (e.g., Jan 01, 2023)
        "%B %d, %Y",  # MMMM DD, YYYY (e.g., January 01, 2023)
        "%b %d %Y",  # MMM DD YYYY (e.g., Jan 01 2023)
        "%B %d %Y",  # MMMM DD YYYY (e.g., January 01 2023)
    ]

    for format in date_formats:
        try:
            date = datetime.strptime(date_string, format)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return date_string

def normalize_dates(dates):
    normalized_dates = []
    for date in dates:
        normalized_date = normalize_date(date)
        normalized_dates.append(normalized_date)
    return normalized_dates

def prompt_user():
    output_file = input("Enter the name of the CSV file (default: organizations.csv): ") or "organizations.csv"
    print_active_only = input("Do you want to print only active pages? (y/n, default: n): ").lower() == "y"
    start_num = int(input("Enter the starting number: "))
    end_num = int(input("Enter the ending number: "))
    pages_to_check = range(start_num, end_num + 1)
    return output_file, print_active_only, pages_to_check

def read_existing_data(output_file):
    existing_data = {}
    try:
        with open(output_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                existing_data[int(row[0])] = [row[1], row[2]]
    except FileNotFoundError:
        pass
    return existing_data

def process_page(driver, page_num, existing_data, writer):
    url = f"{base_url}{page_num}{end_url}"
    driver.get(url)

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            time.sleep(0.2)
            input_element = driver.find_element(By.ID, "edit-name-input")
            content = input_element.get_attribute("value")

            active = "False" if any(word in content for word in ["DEACTIVATED", "Deactivate", "deactivate", "DEACTIVATE", "deactivated"]) else "True"

            textarea_element = driver.find_element(By.ID, "edit-internal-note-input")
            internal_note = textarea_element.get_attribute("value")

            date_pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
            dates = re.findall(date_pattern, internal_note)
            dates = normalize_dates(dates)
            last_vetted = max(dates) if dates else "Missing"
            
            if page_num in existing_data:
                existing_data[page_num] = [active, last_vetted]
            else:
                existing_data[page_num] = [active, last_vetted]
                writer.writerow([page_num, active, last_vetted])

            if not print_active_only or active == "True":
                print(f"Page {page_num}: Active = {active}, Last Vetted = {last_vetted}")
            break  # Exit the retry loop if successful
        except:
            retry_count += 1
            if retry_count < max_retries:
                print(f"Error accessing page {page_num}. Retrying... (Attempt {retry_count})")
                driver.refresh()  # Reload the page
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print(f"Error accessing page {page_num}. Skipping after {max_retries} attempts.")

    # Handle popup/alert dialogues
    try:
        WebDriverWait(driver, 0.2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()  # Select the "Leave" option
        print("Popup/alert dialogue handled")
    except TimeoutException:
        pass

def write_csv(output_file, existing_data):
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Page Number", "Active", "Last Vetted"])  # Write the header row
        for page_num, data in existing_data.items():
            if not print_active_only or data[0] == "True":
                writer.writerow([page_num, data[0], data[1]])

output_file, print_active_only, pages_to_check = prompt_user()
driver = webdriver.Chrome()  # Make sure you have the appropriate webdriver installed
existing_data = read_existing_data(output_file)

# Open the CSV file in write mode
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Page Number", "Active", "Last Vetted"])  # Write the header row

    for page_num in pages_to_check:
        process_page(driver, page_num, existing_data, writer)

write_csv(output_file, existing_data)

driver.quit()  # Close the webdriver
print("Script completed. Results saved to", output_file)
