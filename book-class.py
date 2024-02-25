from selenium import webdriver   
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, calendar
from datetime import date, timedelta

from config import login, password, class_name

chrome_options = Options()  
chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

def nearest_saturday():
  """Finds the date of the nearest Saturday, excluding today if it's a Saturday."""
  today = date.today()
  
  # Check if today is Saturday
  if today.weekday() == calendar.SATURDAY:
    # If today is Saturday, skip to next week
    return today + timedelta(days=7)
  else:
    # Calculate days until next Saturday
    days_to_saturday = (calendar.SATURDAY - today.weekday()) % 7
    return today + timedelta(days=days_to_saturday)

# Get and print the date of the nearest Saturday
nearest_sat_date = nearest_saturday().strftime("%m/%d/%Y")

driver = webdriver.Chrome(options=chrome_options)  
driver.get("https://app.wodify.com/")

try:
    # Login to Wodify, uses email, password fields and the login button
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Input_UserName"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Input_Password"))
    )
    
    email_field.send_keys(login)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-primary:not(.invalid-fields)"))
    )

    login_button.click()

    # After clicking the 
    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".Menu_TopMenu"))
    )

    driver.get("https://app.wodify.com/Schedule/CalendarListViewEntry.aspx")

    date_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='mm/dd/yyyy']"))
    )
    date_filter.clear()
    date_filter.send_keys(nearest_sat_date)

    # click header to close the date picker
    header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".h1"))
    )
    header.click()

    # wait for the date to be loaded
    # nearest_saturday_loaded = WebDriverWait(driver, 15).until(
        # EC.presence_of_element_located((By.XPATH, "//table[@class='TableRecords']/tbody/tr[1]/td/span[contains(., '%s')]" % nearest_sat_date) )
    # )

    # Lazy me, but don't want to wait for the loading element to show and disappear
    time.sleep(5)

    reserve_class_button = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, "//span[contains(@title,'%s')]/ancestor::tr//a[contains(@title, 'Reserve')]" % class_name))
    )

    reserve_class_button.click()

    confirmation_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".Feedback_Message_Text"))
    )

    print("Confirmation message: ", confirmation_message.text)
finally:
    driver.quit()
