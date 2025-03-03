from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import calendar
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')

# Create a new instance of the Chrome driver

driver = webdriver.Chrome(options=options)
# Open the Python website

driver.get("https://loinc.org/wp-login.php")

# Print the page title
print(driver.current_url)
login = driver.find_element(By.ID, 'user_login')
login.clear()
login.send_keys('user')

pwd = driver.find_element(By.ID, 'user_pass')
pwd.clear()
pwd.send_keys('pwd')
pwd.submit()

wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.current_url != "https://loinc.org/wp-login.php")
print(driver.current_url)

downloads = driver.find_element(By.XPATH, '/html/body/div/div[2]/footer/div[1]/div/div[1]/div/div/a')
downloads.click()

# Print the current URL
print(driver.current_url)
currentDownload = driver.find_element(By.XPATH, '//*[@id="post-467010"]/div/div/div/div/div[2]/div[1]/div/div/h2/a')
currentDownload.click()
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.current_url != "https://loinc.org/downloads/")

print(driver.current_url)
tc = driver.find_element(By.ID, 'tc_accepted_')
tc.click()
tc.submit()

driver_cookies = driver.get_cookies()
cookies_copy = {}
for driver_cookie in driver_cookies:
    cookies_copy[driver_cookie["name"]] = driver_cookie["value"]
epoch = int(calendar.timegm(time.gmtime()))    
r = requests.get('https://loinc.org/download/loinc-complete/?tmstv={0}&tc_accepted=1'.format(str(epoch)),cookies = cookies_copy)
r.raise_for_status() # ensure we notice bad responses
file = open("loinc.zip", "wb")
file.write(r.content)
file.close()


# Close the browser window

driver.close()