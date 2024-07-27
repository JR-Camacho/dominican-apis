# Import necessary libraries
import requests
from selenium import webdriver

from app.utils.functions import find_links_to_zip_rar_files, parse_url, download_zip_rar_files_from_url

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

# General information services

general_url = "https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx"

class GeneralService:
    def __init__(self, driver=None):
        self.driver = driver

class RNC:
     # Get the rnc list from the DGII website      
    def get_rnc_list(url = general_url): 
        # # Open in headless browser
        # driver = webdriver.Firefox(options=options)
        # driver.get(url)

        # content = driver.page_source
        # zip_links = find_links_to_zip_rar_files(content, domain="https://www.dgii.gov.do")
        # url_parsed = parse_url(zip_links[0])
        url_parsed = "https://www.dgii.gov.do/app/WebApps/Consultas/RNC/DGII_RNC.zip"

        # Download the ZIP file
        folder_name = f"downloads/dgii/rnc/all"
        download_zip_rar_files_from_url([url_parsed], folder_name)

        # print("Links", url_parsed)

        # driver.close()
        