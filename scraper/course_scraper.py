import time
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.text_utils import TextUtils


class CourseScraper:

    def __init__(self, driver_path, base_url):
        self.base_url = base_url
        self.data = []

        options = Options()
        options.add_argument("--start-maximized")

        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)


    def get_max_pages(self, per_page=96):

        self.driver.get(self.base_url.format(1))

        try:
            element = self.wait.until(
                EC.presence_of_element_located((By.ID, "course-count-msg"))
            )

            text = element.text 
            
            text = TextUtils.fa_to_en(text)

            number = int(re.findall(r"\d+", text)[0])

            max_pages = int(number / per_page)+1

            print(f"[INFO] total courses: {number}")
            print(f"[INFO] max pages: {max_pages}")

            return max_pages

        except Exception as e:
            print("[ERROR] fallback to loop:", e)
            return self._get_max_pages_by_loop()
        
    def scrape_page(self, page):

        url = self.base_url.format(page)
        print(f"[SCRAPING] Page {page}")

        self.driver.get(url)

        courses = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.col-12.mb-3")
            )
        )

        for c in courses:

            try:
                title = c.find_element(By.CSS_SELECTOR, "h3.card-title").text
            except:
                title = None

            try:
                link = c.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = None

            try:
                rating = float(TextUtils.fa_to_en(
                    c.find_element(By.CSS_SELECTOR, ".text-warning.mx-1").text
                ))
            except:
                rating = 0

            try:
                students = TextUtils.extract_number(
                    c.find_element(By.CSS_SELECTOR, ".ms-2").text
                )
            except:
                students = 0

            hours, lessons = TextUtils.parse_hours_lessons(c)

            try:
                level = TextUtils.parse_level(c)
            
            except :
                level = ""

            self.data.append({
                "title": title,
                "link": link,
                "rating": rating,
                "students": students,
                "hours": hours,
                "lessons": lessons,
                "level":level
            })

        time.sleep(1)

    def run(self):
        max_pages = self.get_max_pages()
        print(f"[INFO] max pages: {max_pages}")

        for page in range(1, max_pages + 1):
            self.scrape_page(page)

        self.driver.quit()

        return pd.DataFrame(self.data)