from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from Database.database import insert_database
from webdriver_manager.chrome import ChromeDriverManager



def forming_data():
    url = 'https://www.sanook.com/news/entertain/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return html_page


def get_content():
    html_page = forming_data()
    ent_news = html_page.find('h2', text='อัปเดตล่าสุด').find_next('div').find_all('a')

    # print(len(ent_news))
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for i, s in enumerate(ent_news):
        news = {'source': 'สนุกออนไลน์', 'type': 'เอ็นเตอร์เทน', 'title': '', 'public_date': '', 'content': '',
                'images': [],
                'author': 'สนุกออนไลน์', 'url': '', }
        images = {}
        if i % 3 == 0:
            news['url'] = s['href']
            print(s['href'])
            images['url']  = s.find('img')['src']
            images['alt'] = s.find('img')['alt']
            news['title'] = s['title']
            news['images'].append(images)
    # get content from main news for each url
        driver.get(news['url'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup.prettify())
        t = datetime.strptime(soup.find('time')['datetime'], "%Y-%m-%d %H:%M")
        news['public_date'] = t.strftime('%Y-%m-%d')
        contents = soup.find('div', id='EntryReader_0').find_all('p')
        contents = ''.join([c.text for c in contents])
        news['content'] = contents
        insert_database(news)
    driver.close()



if __name__ == "__main__":
    get_content()
