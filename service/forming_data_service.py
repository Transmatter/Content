import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def forming_data(_url):
    url = _url
    res = requests.get(url)
    res.encoding = "utf-8"
    html_page = BeautifulSoup(res.text, 'html.parser')
    return html_page