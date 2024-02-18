from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class job_obj :
    def __init__(self, position):
        self.position_name = position
        self.dict_job = []
        self.jobs_db = []
        
    def playwright(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://www.wanted.co.kr/search?query={self.position_name}&tab=position")

        for x in range(5):
            page.keyboard.down("End")
            time.sleep(2)
            
        contents = page.content()
        p.stop()
        
        return contents
        
        
    def bs4(self, contents):
        soup = BeautifulSoup(contents, "html.parser")
        jobs = soup.find_all("div",class_="JobCard_container__FqChn")
        if jobs:
            for job in jobs:
                link = f"https://www.wanted.co.kr{job.find("a")["href"]}"
                title = job.find("strong", class_="JobCard_title__ddkwM").text
                company = job.find("span", class_="JobCard_companyName__vZMqJ").text
                location = job.find("span", class_="JobCard_location__2EOr5").text
                reward = job.find("span", class_="JobCard_reward__sdyHn").text

                self.dict_job = {
                "title" : title,
                "company" : company,
                "location" : location,
                "reward" : reward,
                "link" : link,
                }
                self.jobs_db.append(self.dict_job)
    
        else:
            return 0
        
        
    def write_csv(self):
        file = open(f"{self.position_name}_jobs.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Reward", "Link"])

        for job in self.jobs_db:
            writer.writerow(job.values())

keywords = ["flutter", "nextjs", "kotlin"]

obj_list = job_obj(keywords[0]), job_obj(keywords[1]), job_obj(keywords[2])

for keyword in obj_list:
    contents = keyword.playwright()
    return_value = keyword.bs4(contents)
    if return_value != 0:
        keyword.write_csv()




#page.screenshot(path="screenshot.png")