from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Database.database import insert_database


def forming_data():
    url = 'https://www.thairath.co.th/business'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return html_page


def get_content():
    html_page = forming_data()
    invest_news = html_page.find('h2', text='การลงทุน').find_next('div').find_all('a')
    # news = {'source': 'ไทยรัฐออนไลน์', 'type': 'เศรฐกิจ', 'title': '', 'public_date': '', 'content': '',
    #         'images': [],
    #         'author': 'ไทยรัฐออนไลน์', 'url': '', }
    # print(invest_news)
    # print(invest_news[0])
    # print(invest_news[6])
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for i, s in enumerate(invest_news):
        news = {'source': 'ไทยรัฐออนไลน์', 'type': 'เศรฐกิจ', 'title': '', 'public_date': '', 'content': '',
                'images': [],
                'author': 'ไทยรัฐออนไลน์', 'url': '', }
        images = {}
        if i % 2 == 1:
            continue
        news['url'] = 'https://www.thairath.co.th' + s['href']
        images['url'] = s.find('img')['src']
        images['alt'] = s.find('img')['alt']
        news['title'] = s.find('img')['alt']
        news['images'].append(images)
    # get content from main news for each url
        driver.get(news['url'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup.prettify())
        t = datetime.strptime(soup.find('meta', property='article:published_time')['content'][:-6], '%Y-%m-%dT%H:%M:%S')
        news['public_date'] = (t.strftime('%Y-%m-%d'))
        contents = soup.find('article', id='article-content').find_all('p')
        contents = ''.join([c.text for c in contents])
        news['content'] = contents
        insert_database(news)
    driver.close()


if __name__ == "__main__":
        get_content()
