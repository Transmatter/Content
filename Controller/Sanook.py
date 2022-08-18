from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

from selenium.common.exceptions import WebDriverException
from service.forming_data_service import forming_data
from Database.database import insert_database
from webdriver_manager.chrome import ChromeDriverManager



def get_content():
    html_page = forming_data('https://www.sanook.com/news/entertain/')
    ent_news = html_page.find('h2', text='อัปเดตล่าสุด').find_next('div').find_all('a',{'class':'EntryListTitle'})

    # print(len(ent_news))
    for i, s in enumerate(ent_news):
        news = {'source': 'สนุกออนไลน์', 'category': 'เอ็นเตอร์เทน', 'title': s['title'], 'publicDate': '', 'content': '',
                'images': [], 'author': 'สนุกออนไลน์', 'url': s['href'], "approvedBy":None,"approveStatus":"NOT_APPROVE", 'approvedDate':'', 'type':'LOCAL_CONTENT'}

        # news['url'] = s['href']
        # get content from main news for each url
        soup = forming_data(news['url'])
        # print(soup.prettify())
        temp_time = soup.find('time')['datetime']+":00"
        t = datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
        news['publicDate'] = t.strftime('%Y-%m-%d %H:%M:%S')
        contents = soup.find('div', id='EntryReader_0').find_all('p')
        contents = ''.join([c.text for c in contents])
        news['content'] = contents
        content_image={}
        content_image['url'] = soup.find('img')['src']
        content_image['alt'] = ''
        content_image['verifyStatus'] = 'EMPTY'
        content_image['verifiedDate'] = ''
        content_image['verifiedBy'] = None
        news['images'].append(content_image)
        insert_database(news)



if __name__ == "__main__":
    get_content()
