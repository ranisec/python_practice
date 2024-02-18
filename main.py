from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

for x in range(5):
    page.keyboard.down("End")
    time.sleep(2)

content = page.content()
soup = BeautifulSoup(content, "html.parser")
jobs = soup.find_all("div",class_="JobCard_container__FqChn")

p.stop()

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find("a")["href"]}"
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company = job.find("span", class_="JobCard_companyName__vZMqJ").text
    location = job.find("span", class_="JobCard_location__2EOr5").text
    reward = job.find("span", class_="JobCard_reward__sdyHn").text

    dic_job = {
    "title" : title,
    "company" : company,
    "location" : location,
    "reward" : reward,
    "link" : link,
    }
    jobs_db.append(dic_job)

file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Location", "Reward", "Link"])

for job in jobs_db:
    writer.writerow(job.values())


#page.screenshot(path="screenshot.png")