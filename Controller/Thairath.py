from datetime import datetime
from Database.database import insert_database
from bs4 import BeautifulSoup

from service.forming_data_service import forming_data



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
    for i, s in enumerate(incoming_news):
        news = {'source': 'ไทยรัฐออนไลน์', 'type': type, 'title': '', 'public_date': '', 'content': '',
                'images': [],
                'author': 'ไทยรัฐออนไลน์', 'url': '', }
        images = {}
        if i % 2 == 1:
            continue
        news['url'] = 'https://www.thairath.co.th' + s['href']
        print(news['url'])
        images['url'] = s.find('img')['src']
        images['alt'] = s.find('img')['alt']
        images['status'] = "INCOMPLETE" if len(images['alt']) >0 else "EMPTY"
        news['title'] = s.find('img')['alt']
        news['images'].append(images)
        # get content from main news for each url
        soup = forming_data(news['url'])
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
                status = "EMPTY"
                if len(temp_pic.find('img')['alt']) >0:
                    status = "INCOMPLETE"
                temp = {'url': temp_pic.find('img')['src'], 'alt': temp_pic.find('img')['alt'] , 'status': status}
                print(temp)
                news['images'].append(temp)
        #add to database
        insert_database(news)
    return news


if __name__ == "__main__":
    get_thairath_content()
