# Import necessary libraries
import requests
from selenium import webdriver

from app.utils.functions import find_first_element, find_elements_by_regex, find_elements_by_tag, click_element_by_text, find_links_to_excel_files, download_excel_files_from_url

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

# General information services

class GeneralService:
    def __init__(self, driver=None):
        self.driver = driver