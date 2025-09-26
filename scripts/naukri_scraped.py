#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium pandas openpyxl webdriver-manager')


# In[1]:


#imports
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


#Initialize Selenium Chrome Driver
def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1200, 900)
    return driver

driver = get_driver()
print("✅ Chrome driver ready!")


# In[4]:


#Define job scraping function
roles = [
    "data-analyst",
    "data-scientist",
    "business-analyst",
    "machine-learning-engineer",
    "python-developer",
    "data-engineer"
]

def scrape_jobs(role, num_pages=3):  # you can increase num_pages later
    all_jobs = []

    for page in range(1, num_pages + 1):
        url = f"https://www.naukri.com/{role}-jobs-in-india-{page}"
        driver.get(url)
        time.sleep(5)

        try:
            job_cards = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cust-job-tuple"))
            )
        except:
            print(f"⚠️ No jobs found for {role} page {page}")
            continue

        for job in job_cards:
            try: title = job.find_element(By.CSS_SELECTOR, "a.title").text
            except: title = "N/A"
            try: company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text
            except: company = "N/A"
            try: location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text
            except: location = "N/A"
            try: experience = job.find_element(By.CSS_SELECTOR, "span.expwdth").text
            except: experience = "N/A"
            try: salary = job.find_element(By.CSS_SELECTOR, "span.salary, span.sal-wrap").text
            except: salary = "N/A"
            try: skills = ", ".join([s.text for s in job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")])
            except: skills = "N/A"
            try: posted_date = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text
            except: posted_date = "N/A"

            all_jobs.append({
                "Role": role.replace("-", " ").title(),
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Experience": experience,
                "Salary": salary,
                "Skills": skills,
                "Posted Date": posted_date
            })

        print(f"✅ {role} - Page {page} scraped")

    return all_jobs


# In[5]:


#Scrape Jobs for All Roles and Create DataFrame
all_jobs_data = []

for role in roles:
    jobs = scrape_jobs(role, num_pages=10)  # 🔧 increase num_pages for more data
    all_jobs_data.extend(jobs)

df = pd.DataFrame(all_jobs_data)
print("✅ Scraping finished. Total records:", len(df))


# In[6]:


df.head(20)


# In[7]:


#Save Scraped Jobs to CSV
df.to_csv(r"D:\PROJECTS\Naukri_Job_Trends\data\raw\naukri_jobs_raw.csv", index=False)
print("📁 Data saved to data/raw/naukri_jobs.csv")

