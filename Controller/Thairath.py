from datetime import datetime
from Database.database import insert_database
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from service.forming_data_service import forming_data

# from Database.database import insert_database


def get_thairath_content():
    html_page = forming_data('https://www.thairath.co.th/business')
    invest_news = html_page.find('h2', text='การลงทุน').find_next('div').find_all('a')
    policy_news =  html_page.find('h2', text='เศรษฐกิจ-นโยบาย').find_next('div').find_all('a')
    marketing_news = html_page.find('h2', text='การตลาด-ธุรกิจ').find_next('div').find_all('a')
    finance_news = html_page.find('h2', text='การเงิน การธนาคาร').find_next('div').find_all('a')
    analysis_news = html_page.find('h2', text='บทวิเคราะห์เศรษฐกิจ').find_next('div').find_all('a')
    try:
        fetch_news(invest_news, 'การลงทุน')
        fetch_news(policy_news, 'นโยบาย')
        fetch_news(marketing_news, 'การตลาด')
        fetch_news(finance_news, 'การเงิน')
        fetch_news(analysis_news, 'วิเคราะห์เศรษฐกิจ')
    except Exception:
        return "something went woring"


def fetch_news(incoming_news, type):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for i, s in enumerate(incoming_news):
        try:
            news = {'source': 'ไทยรัฐออนไลน์', 'type': type, 'title': '', 'public_date': '', 'content': '',
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
            news['public_date'] = (t.strftime('%Y-%m-%d %H:%M:%S'))
            contents = soup.find('article', id='article-content').find_all('p')
            contents = ''.join([c.text for c in contents])
            news['content'] = contents

            # get images in content here
            picture = soup.find_all('picture')
            if picture is not None:
                for temp_pic in picture:
                    temp = {'url': temp_pic.find('img')['src'], 'ait': ''}
                    news['images'].append(temp)
            #add to database
            insert_database(news)

        except WebDriverException:
            continue
    driver.close()
    return news


if __name__ == "__main__":
    get_thairath_content()
