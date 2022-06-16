
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def forming_data(_url):
    url = _url
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return html_page