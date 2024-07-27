# File for common functions and variables used in the project

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import re
import time

def click_element_by_text(driver, text, sleep_time=3, partial_match=False):
    """
    Clicks an element in the page by its text
    :param driver: Selenium driver
    :param text: text of the element to click
    :param sleep_time: time to wait after clicking
    :param partial_match: if True, will match the text partially
    :return: None
    """
    if partial_match:
        search_criteria = f"//*[contains(text(),'{text}')]"
    else:
        search_criteria = f"//*[text()='{text}']"
    date_elements = driver.find_elements(By.XPATH, search_criteria)
    # filter empty elements
    date_elements = [el for el in date_elements if el.text]
    date_elements[0].click()
    time.sleep(sleep_time)

def find_links_to_excel_files(content, domain=None):
    """
    Finds all links to Excel files in the content of a page
    :param content: HTML content of the page
    :param domain: domain of the page
    :return: list of links to Excel files
    """
    ans = []
    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.find_all('a')
    for a in a_tags:
        # If the <a> tag has a href attribute
        if 'href' in a.attrs:
            link_url = a['href']

            # If the link is to an Excel file
            if (link_url.endswith('.xls') or link_url.endswith('.xlsx')) and (link_url not in ans):
                # Add the link to the list of Excel file links
                print('Found Excel file:', link_url)
                ans.append(domain+link_url if domain else link_url)
    return list(set(ans))

def find_links_matching_all(response, items, without_domain=False):
    """
    Finds all links in the response that contain all the items in the list
    :param response: Selenium driver or requests response
    :param without_domain: it will return all the found links without concact the domain
    :param items: list of strings to match
    :return: list of links
    """
    if isinstance(response, webdriver.firefox.webdriver.WebDriver):
        # For Selenium driver
        soup = BeautifulSoup(response.page_source, 'html.parser')
        current_url = response.current_url
    else:
        # For requests response
        soup = BeautifulSoup(response.content, 'html.parser')
        current_url = response.url
    domain = re.findall(r'^(https?://[^/]+)', current_url)[0]
    a_tags = soup.find_all('a')
    available_links = [a['href'] for a in a_tags if 'href' in a.attrs]
    matching_links = []
    for link in available_links:
        if all(item in link for item in items):
            matching_links.append(domain+link if without_domain is False else link)
    return list(set(matching_links))

def download_excel_files_from_url(excel_links, folder_name, filename_from_headers=None, headers=None, allow_redirects=True, split_arg = None):
    """
    Downloads all Excel files from a list of links
    :param excel_links: list of links to Excel files
    :param folder_name: folder to save the files
    :param filename_from_headers: if True, will get the filename from the headers instead of the URL
    :return: None
    Note: It only works if the link ends with .xls or .xlsx. For pages where a download button is clicked, 
    """
    for link in excel_links:
        print('Downloading Excel file:', link)
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Download the file
        r = requests.get(link, allow_redirects=allow_redirects, headers=headers)
        # Get the filename from the URL

        if filename_from_headers is None:
            filename = re.findall(r'/([^/]+)$', link)[0]
        else:
            if 'content-disposition' in r.headers:
                filename = r.headers.get('content-disposition').split('filename=')[1].replace('"','')
            elif not allow_redirects:
                filename = r.headers.get('location').split(split_arg)[1]

        if not filename.endswith('.xls') and not filename.endswith('.xlsx'):
            filename += '.xlsx'
        open(folder_name + '/' + filename, 'wb').write(r.content)

def find_first_element(response, tag = 'p'):
     # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

     # Extract the content of the first <tag> element
    first_element = soup.find(tag)

     # Check if a <tag> element was found
    if first_element:
        return first_element.get_text(strip=True)  # strip=True removes leading/trailing whitespaces       
    else:
        print("No " + "<"+tag+">" + " element found on the page.")  
        return None

def find_elements_by_regex(regex, container_tag = None, container_class = None, response=None, content=None):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text if response else content, 'html.parser')

        if container_tag:
            # Find a specific container, for example, a <div> with a specific class
            container = soup.find(container_tag, class_=container_class)
            # Use regex to find content in the container tag
            all_text = container.get_text()
        else: 
            # Use regex to find content in the HTML content
            all_text = soup.get_text()
        return re.findall(regex, all_text)

def find_elements_by_tag(tag, container_tag = None, container_class = None, response=None, content=None, exceptions=['']):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text if response else content, 'html.parser')

        if container_tag:
            # Find a specific container, for example, a <div> with a specific class
            container = soup.find(container_tag, class_=container_class)
            elements = container.find_all(tag)
        else:
            elements = soup.find_all(tag)
     
        # Use tag to find content in the HTML content or container tag
        return [p.get_text(strip=True) for p in elements if p.get_text(strip=True) not in exceptions]

def delete_unnamed_columns(df):
    # Find the first valid raw
    first_raw = df.apply(lambda x: x.notnull().sum(), axis=1).idxmax()
    # Return the DataFrame with the raws based in the first raw
    df = df.iloc[first_raw:]
    # Establish the first raw like headers
    df.columns = df.iloc[0]
    # Delete the first raw (now headers)
    df = df.iloc[1:]
    # Restart the index
    df.reset_index(drop=True, inplace=True)
    return df

def find_links_to_zip_rar_files(content, domain=None):
    """
    Finds all links to Excel files in the content of a page
    :param content: HTML content of the page
    :param domain: domain of the page
    :return: list of links to Excel files
    """
    ans = []
    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.find_all('a')
    for a in a_tags:
        # If the <a> tag has a href attribute
        if 'href' in a.attrs:
            link_url = a['href']

            # If the link is to an Zip or Rar file
            if (link_url.endswith('.zip') or link_url.endswith('.rar')) and (link_url not in ans):
                # Add the link to the list of Zip or Rar file links
                print('Found Zip Rar file:', link_url)
                ans.append(domain+link_url if domain else link_url)
    return list(set(ans))

# def parse_url(url):
#     # Split the URL by '..' to remove relative path components
#     parts = url.split('..')
    
#     # Rejoin the parts without the '..' to get the base URL
#     base_url = parts[0]
    
#     # Remove any backslashes and replace with forward slashes
#     cleaned_path = '/'.join(parts[1:]).replace('\\', '/')
    
#     # Ensure the base URL ends with a slash before concatenating
#     if not base_url.endswith('/'):
#         base_url += '/'
    
#     # Concatenate the base URL with the cleaned path
#     full_url = base_url + cleaned_path
    
#     # Correct the path to include 'app/WebApps' if missing
#     if 'app/WebApps' not in full_url:
#         path_parts = full_url.split('/')
#         # Insert 'app/WebApps' after the domain
#         path_parts.insert(3, 'app/WebApps')
#         full_url = '/'.join(path_parts)
    
#     return full_url


def parse_url(url):
    # Split the URL by '..' to identify relative path components
    parts = url.split('..')
    
    # Filter out empty strings to remove the effect of consecutive slashes
    parts = [part for part in parts if part]
    
    # Reconstruct the URL without the '..' and replace backslashes with forward slashes
    cleaned_path = '/'.join(parts).replace('\\', '/')
    
    # Split the cleaned path to insert 'app/WebApps' if missing
    path_parts = cleaned_path.split('/')
    
    # Ensure the base URL ends with a slash
    if not path_parts[0].endswith('/'):
        path_parts[0] += '/'
    
    # Insert 'app/WebApps' after the domain if missing
    if 'app/WebApps' not in path_parts:
        path_parts.insert(3, 'app/WebApps')
    
    # Rejoin the parts into the full URL
    full_url = '/'.join(path_parts)
    
    return full_url

def download_zip_rar_files_from_url(links, folder_name, filename_from_headers=None, headers=None, allow_redirects=True, split_arg = None):
    """
    Downloads all ZIP or RAR files from a list of links
    :param links: list of links to zip/rar files
    :param folder_name: folder to save the files
    :param filename_from_headers: if True, will get the filename from the headers instead of the URL
    :return: None
    Note: It only works if the link ends with .zip or .rar. For pages where a download button is clicked, 
    """
    for link in links:
        print('Downloading Zip/Rar file:', link)
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Download the file
        r = requests.get(link, allow_redirects=allow_redirects, headers=headers)
        # Get the filename from the URL

        if filename_from_headers is None:
            filename = re.findall(r'/([^/]+)$', link)[0]
        else:
            if 'content-disposition' in r.headers:
                filename = r.headers.get('content-disposition').split('filename=')[1].replace('"','')
            elif not allow_redirects:
                filename = r.headers.get('location').split(split_arg)[1]

        # if not filename.endswith('.zip') and not filename.endswith('.xlsx'):
        #     filename += '.xlsx'
        open(folder_name + '/' + filename, 'wb').write(r.content)
