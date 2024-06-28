"""
RPA Challenge Automation Script

This script automates the RPA Challenge from the website https://rpachallenge.com/.
It downloads an XLSX file, reads its data, fills out the dynamic form on the website,
and captures a screenshot of the final result along with the execution time.

Author: Victor Vinci Fantucci
Date: 06/28/2024

Dependencies:
- pandas
- openpyxl
- selenium
- pillow
- googletrans

Usage:
- Ensure you have the required dependencies installed.
- Download the appropriate WebDriver for your browser and ensure it's in your system PATH.
- Run the script using `python rpa_challenge.py`.

"""

# Import dependencies
import os
import sys
import logging
import warnings
import requests
import time
import pandas as pd
from r4ven_utils.log4me import function_logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Suppress all warnings
warnings.filterwarnings('ignore')

# Get the name of the directory where this file is present.
current_directory = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory name where the current directory is present.
parent_directory = os.path.dirname(current_directory)

# Adding the current directory to the sys.path.
sys.path.append(parent_directory)

# Get the base name of the current script file without the '.py' suffix
script_name = os.path.basename(__file__).removesuffix('.py')

# Create a logger for the script with the specified name and console logging level set to INFO
log4me = function_logger(script_name=script_name, console_level=logging.INFO)

class Challenge:
    """This class contains all the functionalities to execute the bot on the RPA Challenge website."""

    def __init__(self):
        try:
            """Initialize the class and open the RPA Challenge website."""
            self.options = webdriver.ChromeOptions()  # Changed to ChromeOptions
            self.options.add_argument("--disable-notifications")  # Example of Chrome option
            # self.options.add_argument("--headless")  # Optional: run in headless mode
            self.options.add_argument("--window-size=1920,1080")  # Optional: set window size

            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)  # Changed to Chrome
            self.wdw = WebDriverWait(self.driver, 40)
            self.driver.maximize_window()
        except Exception as error:
            log4me.error(f"Error initializing Challenge class: {error}")
            raise

    def access_site(self, url: str):
        """Start the RPA Challenge website."""
        try:
            self.driver.get(url)
            self.wdw.until(ec.visibility_of_element_located((By.CLASS_NAME, 'btn-large')))
        except Exception as error:
            log4me.error(f'Error starting the site: {error}')
            raise Exception('Error starting the site')

    def start_challenge(self):
        """Press the start button to begin data entry."""
        try:
            self.driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button').click()
        except Exception as error:
            log4me.error(f'Error starting the challenge: {error}')
            raise Exception('Error starting the challenge')

    def download_file(self):
        """Request, download, and save the file into the data folder."""
        try:
            url = 'https://rpachallenge.com/assets/downloadFiles/challenge.xlsx'
            file = requests.get(url, allow_redirects=True)
            data_folder = os.path.join(parent_directory, "data")
            os.makedirs(data_folder, exist_ok=True)  # Ensure data folder exists
            file_path = os.path.join(data_folder, 'input_forms_challenge.xlsx')
            with open(file_path, 'wb') as f:
                f.write(file.content)
            data = pd.read_excel(file_path)
            return data
        except Exception as error:
            log4me.error(f'Error downloading or saving the file: {error}')
            raise Exception('Error downloading or saving the file')

    def insert_data(self, data):
        """Insert the data into the form."""
        try:
            for index, row in data.iterrows():
                try:
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelFirstName"]').send_keys(row['First Name'])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelLastName"]').send_keys(row['Last Name '])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelCompanyName"]').send_keys(row['Company Name'])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelRole"]').send_keys(row['Role in Company'])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelAddress"]').send_keys(row['Address'])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelEmail"]').send_keys(row['Email'])
                    self.driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelPhone"]').send_keys(row['Phone Number'])
                    self.driver.find_element(By.XPATH, '//input[@value="Submit"]').click()
                except KeyError as e:
                    log4me.error(f"KeyError accessing DataFrame column: {e}")
                    raise Exception(f"Error inserting data for line {index + 1}")
                except Exception as error:
                    log4me.error(f'Error inserting data for line {index + 1}. Details: {error}')
                    raise Exception(f'Error inserting data for line {index + 1}')
        except Exception as e:
            log4me.error(f"Error inserting data: {e}")
            raise Exception("Error inserting data")

    def capture_time(self):
        """Capture the time taken by the robot to execute the process."""
        try:
            success_message = self.wdw.until(ec.visibility_of_element_located((By.CLASS_NAME, 'message2')))
            log4me.info(f"Success message found: {success_message.text}")

            # Introduce a 1-second delay to ensure stability
            time.sleep(1)

            # Confirm success message again before proceeding to take screenshot
            if '100%' in success_message.text:
                log4me.info("Success message confirms completion, taking screenshot.")

                # Directly save screenshot here after success message is confirmed
                screenshot_path = os.path.join(parent_directory, "screenshots", "input_forms_challenge.png")
                self.driver.save_screenshot(screenshot_path)

                log4me.info(f"Screenshot saved successfully at: {screenshot_path}")

                return True
            else:
                log4me.error("Success message did not confirm completion.")
                raise Exception("Success message did not confirm completion.")
        except Exception as error:
            log4me.error(f'Error capturing time or saving screenshot: {str(error)}')
            raise Exception('Error capturing time or saving screenshot.')

    def close_browser(self):
        """Close the driver."""
        self.driver.close()

    def __del__(self):
        """Delete the class instance."""
        log4me.info('Execution ended')

def main():
    """Main function to execute the RPA Challenge bot."""
    status_loop = 'ON'
    state = 'INITIALIZATION'
    bot = Challenge()

    while status_loop == 'ON':
        if state == 'INITIALIZATION':
            bot.access_site('https://rpachallenge.com/')
            state = 'GET TRANSACTION'
            continue

        if state == 'GET TRANSACTION':
            data = bot.download_file()
            state = 'PROCESS'
            continue

        if state == 'PROCESS':
            bot.start_challenge()
            bot.insert_data(data)
            bot.capture_time()
            state = 'END'
            continue

        if state == 'END':
            bot.close_browser()
            del bot
            status_loop = 'OFF'
            continue

if __name__ == "__main__":
    main()
