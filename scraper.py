# Author: Colin Tiller

# Resources:
# https://selenium-python.readthedocs.io/waits.html
# https://selenium-python.readthedocs.io/locating-elements.html
# https://pypi.org/project/webdriver-manager/

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


def search_jobs(driver, job_keyword, location):
    """
    This function will search for jobs based on the job_keyword and location -- it will also click the internship button.
    """
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



def get_job_listing_links(driver, links):
    """
    This function will go through each job listing and get the href for each job.
    Specifically, it is specialized for ziprecruiter job listings.
    """
    # go through each <li> and add the href to a list
    try:
        job_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/ul[1]/li/strong/a"))
        )
        for job in job_listings:
            if "ziprecruiter" in job.get_attribute("href"):
                links.append(job.get_attribute("href"))
    except Exception as e:
        print(f"Error during job listing retrieval: {e}")
        
        
def paginate(driver):
    """
    This function will scroll to the bottom of the page and click the next button.
    """
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
        
 
def process_webpage(driver, link):
    """
    This function processes the webpage to retrieve:
    - Job Title
    - Job Company
    - Job Location
    - Benefits list
    - Job Description
    - How recently it was posted
    
    Returns a dictionary with the above information.
    """
    
    driver.get(link)
    job_info = {}
    
    # Title
    try:
        job_info["title"] = driver.find_element(By.CSS_SELECTOR, "h1").text
    except Exception as e:
        job_info["title"] = "Not available"
        print(f"Error during title retrieval: {e}")
    
    # Company
    try:
        job_info["company"] = driver.find_element(By.CLASS_NAME, "job_company").text
    except Exception as e:
        job_info["company"] = "Not available"
        print(f"Error during company retrieval: {e}")

    # Location
    try:
        job_info["location"] = driver.find_element(By.CLASS_NAME, "job_location").text
    except Exception as e:
        job_info["location"] = "Not available"
        print(f"Error during location retrieval: {e}")

    # Benefits list #ul class="job_benefits_list"
    try:
        job_info["benefits"] = [li.text for li in driver.find_elements(By.CLASS_NAME, "job_benefits_list")]
    except Exception as e:
        job_info["benefits"] = "Not available"
        print(f"Error during benefits retrieval: {e}")
        

    try:
        job_info["description"] = " ".join([p.text for p in driver.find_elements(By.CLASS_NAME, "job_description")])
    except Exception as e:
        job_info["description"] = "Not available"
        print(f"Error during description retrieval: {e}")
        
    try:
        job_info["posted_date"] = driver.find_element(By.CLASS_NAME, "job_posted").text
    except Exception as e:
        job_info["posted_date"] = "Not available"
        print(f"Error during posted date retrieval: {e}")
        
    job_info["link"] = link

    return job_info


def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    site = "https://www.collegegrad.com/"
    
    driver.get(site)
    
    search_terms = "Software, Data, Computer, Information, Technology"
    location = "North Carolina"
    
    search_jobs(driver, search_terms, location)
    
    # Init list to store listings
    links = []
    
    for _ in range(1):
        get_job_listing_links(driver, links)
        paginate(driver)
        time.sleep(2)  # be nice to the website :>
        
    
    # Get details from each listing
    details = []
    for link in links:
        job_info = process_webpage(driver, link)
        if job_info:
            details.append(job_info)
        else:
            details.append({"error": "No details found"})
        time.sleep(1) 
    
    # Write to file jsonlines .jl
    with open('jobs.jl', 'w') as f:
        for item in details:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    driver.quit()
    
    
if __name__ == "__main__":
    main()