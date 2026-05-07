from scraper.course_scraper import CourseScraper
from recommender.course_recommender import CourseRecommender
import os
import pandas as pd
import time

def main():

    DRIVER_PATH = "C:/chromedriver/chromedriver-win64/chromedriver.exe"
    
    OUTPUT_FILE = "./output/{}.xlsx"


    courses = pd.read_excel('courses.xlsx')
    print(courses)
    categories = dict(
        zip(
            courses['name'],
            (courses['alias'])
        )
    )

    for c in categories:

        BASE_URL = f"https://git.ir/courses/?c={c}&sort=newest&pg=96&page=1"
        BASE_URL += '&page={}'


        #1. scrape
        scraper = CourseScraper(DRIVER_PATH, BASE_URL)
        df = scraper.run()

        print(f"[INFO] scraped {len(df)} {c}")

        # 2. recommend
        recommender = CourseRecommender(df)
        df_ranked = recommender.feature_engineering().rank()
        df_final = recommender.top_unique()

        # 3. save
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        OUTPUT_DIR = os.path.join(BASE_DIR, "output")

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        OUTPUT_FILE = os.path.join(OUTPUT_DIR, "{}.xlsx")
        
        df_final.to_excel(OUTPUT_FILE.format(categories[c]), index=False)

        print(f"[DONE] saved to {OUTPUT_FILE}")
        print(df_final[["title", "score"]].head(10))

        time.sleep(5)

if __name__ == "__main__":
    main()