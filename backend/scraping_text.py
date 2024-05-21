import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import threading
import pyarrow.parquet as pq

class ScrapeText:
    def __init__(self):
        self.df_links = pq.read_table("list of company websites.snappy.parquet").to_pandas()
        self.start = 0
        self.end = len(self.df_links) - 1
        self.num_threads = 16
        for i in range(len(self.df_links)):
            if not self.df_links.loc[i, "domain"].startswith("http"):
                self.df_links.loc[i, "domain"] = "https://" + self.df_links.loc[i, "domain"] 
        self.directory = "./text_from_links"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        # self.scrape_links_multithreaded()
        self.scrape_links(self.start, self.end)
    def init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scraping_text(self, url):
        driver = self.init_driver() 
        url = url.strip("'")
        try:
            driver.get(url)
            text_element = driver.find_element(By.XPATH, "/html/body")
            text = text_element.text if text_element else "No text found"
            return text
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
        finally:
            driver.quit()  

    def scrape_links(self, start_index, end_index):
         for index, row in self.df_links.iloc[start_index:end_index].iterrows():
            
            if (not os.path.exists(f"{self.directory}/text_link_{index}")) and (not os.path.exists(f"{self.directory}/text_link_{index}.txt")):
                print(f"Scraping text from {row['domain']}, {index}")
                text = self.scraping_text(row['domain'])
                with open(f"{self.directory}/text_link_{index}.txt", "a") as text_file:
                    text_file.write(text)
                

    def scrape_links_multithreaded(self):
        threads = []
        step = (self.end - self.start) // self.num_threads
        for i in range(self.num_threads):
            start_index = self.start + i * step
            end_index = min(self.start + (i + 1) * step, self.end)
            thread = threading.Thread(target=self.scrape_links, args=(start_index, end_index))
            threads.append(thread)
            thread.start()

        

        # with open("timers.txt", "w") as f:
        #     for thread_id, times in self.timers.items():
        #         f.write(f"Thread {thread_id}: Total time taken: {sum(times)} seconds\n")
        # for thread_id, times in self.timers.items():
        #     print(f"Thread {thread_id}: Total time taken: {sum(times)} seconds")


if __name__ == "__main__":
    start_time = time.time()
    scraper = ScrapeText()

    # for file in os.listdir("./text_from_links"):
    #     if len(open(f"./text_from_links/{file}").readlines()) < 10:
    #         os.remove(f"./text_from_links/{file}")
    end_time = time.time()
    print(f"Scraping finished.")
    print(f"Time taken: {end_time - start_time}")
