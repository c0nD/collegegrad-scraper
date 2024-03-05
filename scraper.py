from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


"""
Setup the driver
"""
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
site = "https://www.collegegrad.com/"
driver.get(site)

search_terms = "Software, Data, Computer, Information, Technology"
location = "North Carolina"

def search_jobs(job_keyword, location):
    try:
        job_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "keywords"))
        )
        job_search.clear()
        job_search.send_keys(job_keyword)

        location_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "location"))
        )
        location_search.clear()
        location_search.send_keys(location)
        
        # click internship button
        internship_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ei"))
        )
        internship_button.click()
        
        search_button = driver.find_element(By.ID, "searchJobsBtn")
        search_button.click()
        
        job_search.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error during search: {e}")

search_terms = "Software, Data, Computer, Information, Technology"


# Follow through to different <a> tags to get job listings

def get_job_listing_links():
    # go through each <li> and add the href to a list
    try:
        job_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/ul[1]/li/strong/a"))
        )
        for job in job_listings:
            print(job.get_attribute("href"))
    except Exception as e:
        print(f"Error during job listing retrieval: {e}")
        
        
def paginate():
    # scroll to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        # click the next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Next"))
        )
        next_button.click()
    except Exception as e:
        print(f"Error during pagination -- ran out of pages?: {e}")

# Search through all pages:
while True:
    search_jobs(search_terms, location)
    get_job_listing_links()
    paginate()
    time.sleep(3)
    if driver.find_element(By.LINK_TEXT, "Next").get_attribute("href") == None:
        break
    

# Remember to uncomment the line below when you're ready to close the browser
# driver.quit()