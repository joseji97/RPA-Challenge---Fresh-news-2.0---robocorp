import os
import re
import json
import uuid
import glob
import requests
import logging, logging.config
from time import sleep
from datetime import datetime, date, timedelta
from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import By
from RPA.Excel.Files import Files
from robocorp.tasks import task

class WebScraper:
    CURRENT_DIRECTORY = os.getcwd()
    OUTPUT_FOLDER = f"{CURRENT_DIRECTORY}/output"
    PARAMETERS_FILENAME = f"{CURRENT_DIRECTORY}/properties.json"
    LOG_FOLDER = f"{OUTPUT_FOLDER}/Log"
    IMAGES_FOLDER = f"{OUTPUT_FOLDER}/Images"
    TODAY = datetime.now()
    TODAY_STR = TODAY.strftime("%m%d%Y")
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.config.dictConfig({
                                "version": 1,
                                "disable_existing_loggers": True,
                                })


    def __init__(self):
        self._check_folder_exists(self.LOG_FOLDER)   
        self._check_folder_exists(self.IMAGES_FOLDER)  
        self.LOG_NAME = f"{self.LOG_FOLDER}/LATIMES_{self.TODAY_STR}.log"
        logging.basicConfig(filename=self.LOG_NAME,
                        level = logging.DEBUG,
                        format = self.LOG_FORMAT,
                        filemode = "a+")
        self.logger = logging.getLogger(__name__)

        self.print_and_log("info", message="###"*30)
        self.print_and_log("info", message="BOT started")

        try:
            self.properties = self.import_data()
            self.URL = self.properties.get("URL")
            self.SEARCH_PHRASE = self.properties.get("SEARCH_PHRASE")
            self.TOPIC = self.properties.get("TOPIC")
            self.NUMBER_OF_MONTHS = self.properties.get("NUMBER_OF_MONTHS")
            self.DELAY = self.properties.get("DELAY")
        
        except:
            self.print_and_log("error","Choosen Key not found in properties.json file")
        

    def print_and_log(self, log_type="debug", message=""):
        print(f"{log_type.upper()}: {message}")
        if log_type == "info":
            self.logger.info(message)
        elif log_type == "warning":
            self.logger.warning(message)
        elif log_type == "error":
            self.logger.error(message)
        else: 
            self.logger.debug(message)


    def _check_folder_exists(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)


    def import_data(self,file_name=PARAMETERS_FILENAME):
        try:
            self.print_and_log("info","Importing data from JSON file")
            with open(file_name, encoding="utf-8") as f:
                data = json.load(f)
            self.print_and_log("info","Data sucessfully imported")
            return data
        except Exception as e:
            self.print_and_log("error",str(e))
            self.print_and_log("error","Can't fetch data from json")
            return {}


    def close_browser(self):
        self.browser_lib.close_browser()


    def open_website(self):
        try:
            self.print_and_log("info", message="Opening browser")
            self.browser_lib = Selenium(auto_close=False)
            self.browser_lib.open_available_browser(self.URL)
            self.browser_lib.maximize_browser_window()
            self.print_and_log("info", message="Browser opened")
        except Exception as e:
            self.print_and_log("error",str(e))
            self.print_and_log("error","Error opening browser")


    def begin_search(self):
        try:
            SEARCH_XPATH = "//button[@data-element='search-button']"
            self.print_and_log("info", message="Clicking search button")
            self.browser_lib.wait_until_page_contains_element(locator=SEARCH_XPATH,timeout=self.DELAY)
            self.browser_lib.click_button_when_visible(locator=SEARCH_XPATH)
            self.print_and_log("info", message="Writing search phrase")
            FIELD_XPATH = "//input[@placeholder='Search']"
            self.browser_lib.wait_until_page_contains_element(locator=FIELD_XPATH,timeout=self.DELAY)
            self.browser_lib.input_text(locator=FIELD_XPATH, text=self.SEARCH_PHRASE)
            self.print_and_log("info", message="Searching content")
            GO_BUTTON_XPATH = "//button[@data-element='search-submit-button']"
            self.browser_lib.wait_until_page_contains_element(locator=GO_BUTTON_XPATH,timeout=self.DELAY)
            self.browser_lib.click_button_when_visible(locator=GO_BUTTON_XPATH)
        
        except Exception as e:
            self.print_and_log("error",str(e))
            self.print_and_log("error","Error on execution of begin_search")


    def select_topic(self):

        if len(self.TOPIC) == 0:
            return
        for value in self.TOPIC:
            try:
                see_all_xpath = "//div[1]/ps-toggler/ps-toggler/button[@class='button see-all-button']"
                self.browser_lib.click_element(locator=see_all_xpath)
                self.print_and_log("info", message=f"Clicking on topic '{value}'")
                TOPIC_XPATH = f"//span[./text()='{value}']/../input"
                self.browser_lib.wait_until_page_contains_element(locator=TOPIC_XPATH)
                self.browser_lib.click_element(locator=TOPIC_XPATH)
                sleep(self.DELAY)
            except Exception as e:
                self.print_and_log("error",str(e))
                self.print_and_log("error","Topic not found")


    def sort_newest_news(self):
        try:
            SORT_DROPDOWN_BUTTON = "//select[@class='select-input']"
            LIST_OPTION = "Newest"
            self.print_and_log("info", message=f"Sorting news by '{LIST_OPTION}'")
            self.browser_lib.wait_until_page_contains_element(locator=SORT_DROPDOWN_BUTTON)
            LIST_OPTION_XPATH = f"{SORT_DROPDOWN_BUTTON}/option[text()='{LIST_OPTION}']"
            LIST_VALUE=self.browser_lib.get_element_attribute(LIST_OPTION_XPATH,"value")
            self.browser_lib.select_from_list_by_value(SORT_DROPDOWN_BUTTON, LIST_VALUE)
            sleep(self.DELAY)
        except Exception as e:
            self.print_and_log("error",str(e))
            self.print_and_log("error","Error sorting news")


    def go_to_next_page(self):
        try:
            self.print_and_log("info","Going to next page")
            NEXT_PAGE_BUTTON = "//div[@class='search-results-module-next-page']/a"
            self.browser_lib.wait_until_page_contains_element(locator=NEXT_PAGE_BUTTON)
            NEXT_PAGE_LINK = self.browser_lib.get_element_attribute(NEXT_PAGE_BUTTON,"href")
            self.browser_lib.click_link(NEXT_PAGE_LINK)
            sleep(self.DELAY)
        except Exception as e:
            self.print_and_log("error",str(e))
            self.print_and_log("error","Error going to next page")


    def extract_website_data(self):
        self.print_and_log("info",message="Extracting data from website")
        flag = True
        self.set_month_range()
        extracted_data = [['DATE','TITLE','DESCRIPTION','IMAGE NAME','COUNT OF SEARCH PHRASES','TITLE CONTAINS AMOUNT OF MONEY','DESCRIPTION CONTAINS AMOUNT OF MONEY']]

        while(flag==True):
            element_list = "//ul[@class='search-results-module-results-menu']/li"
            news_list_elements = self.browser_lib.get_webelements(element_list)

            for value in range(0, len(news_list_elements)):
                timestamp_str = news_list_elements[value].find_element(By.CLASS_NAME, "promo-timestamp").get_attribute("data-timestamp")
                date = self.convert_timestamp_to_datetime(timestamp_str)
                title = news_list_elements[value].find_element(By.CLASS_NAME, "promo-title").text
                description = news_list_elements[value].find_element(By.CLASS_NAME, "promo-description").text
                image_link = news_list_elements[value].find_element(By.CLASS_NAME, "image").get_attribute("src")
                image = self.download_image_from_url(image_link)

                is_title_dolar = self.check_for_dolar_sign(title)
                is_description_dolar = self.check_for_dolar_sign(description)
                phrases_count = self.check_phrases(text_pattern=self.SEARCH_PHRASE, text=title)

                flag = self.date_comparison(date)
                if flag == True:
                    extracted_data.append(
                        [
                            date,
                            title,
                            description,
                            image,
                            self.check_phrases(
                                text_pattern=self.SEARCH_PHRASE,
                                text=description,
                                count=phrases_count,
                            ),
                            is_title_dolar,
                            is_description_dolar,
                        ]
                    )
                else:
                    break
            if flag == True:
                self.go_to_next_page()

        #self.print_and_log("info",extracted_data)
        self.write_excel_file(extracted_data)


    def set_month_range(self):
        self.end = self.TODAY.strftime("%m/%d/%Y")

        if self.NUMBER_OF_MONTHS < 2:
            self.start = self.TODAY.replace(day=1).strftime("%m/%d/%Y")
        else:
            self.start = (
                (self.TODAY - datetime.timedelta(days=30 * (self.NUMBER_OF_MONTHS - 1)))
                .replace(day=1)
                .strftime("%m/%d/%Y")
            )

    def date_comparison(self,current_date):
        format = "%m/%d/%Y"
        start_datetime = datetime.strptime(self.start, format)
        current_date_datetime = datetime.strptime(current_date, format)

        if current_date_datetime >= start_datetime:
            return True
        else:
            return False

    def convert_timestamp_to_datetime(self, timestamp_str):
        timestamp_float_in_miliseconds = float(timestamp_str)
        timestamp_float_in_seconds = timestamp_float_in_miliseconds / 1000
        date_str = datetime.fromtimestamp(timestamp_float_in_seconds).strftime("%m/%d/%Y")
        return date_str


    def write_excel_file(self, data):
        lib = Files()
        lib.create_workbook()
        lib.append_rows_to_worksheet(data)
        lib.save_workbook(f"{self.OUTPUT_FOLDER}/result.xlsx")


    def download_image_from_url(self, image_url):
        image_name = str(uuid.uuid4())
        if image_url == "":
            return ""
        img_data = requests.get(image_url).content
        with open(f"{self.IMAGES_FOLDER}/{image_name}.jpg", "wb") as handler:
            handler.write(img_data)
        return image_name


    def check_phrases(self, text_pattern, text, count=0):
        c = count
        words = text.split()
        for word in words:
            if word.strip(",.;:-?!") == text_pattern:
                c += 1
        return c


    def check_for_dolar_sign(self, text):
        pattern = re.compile(
            "((\$\s*\d{1,}.\d{0,}.\d{0,})|(\d{1,}\s*(dollars|usd|dollar)))", re.IGNORECASE
        )

        if re.search(pattern, text):
            return True
        return False


@task
def main():
    WebScraperBot = WebScraper()
    WebScraperBot.open_website()
    WebScraperBot.begin_search()
    WebScraperBot.select_topic()
    WebScraperBot.sort_newest_news()
    WebScraperBot.set_month_range()
    WebScraperBot.extract_website_data()
    WebScraperBot.close_browser()
    WebScraperBot.print_and_log("info","Bot execution finished")
        