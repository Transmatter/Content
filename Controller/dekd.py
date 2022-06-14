from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from Database.database import insert_database


def format_time(incorrect_date):
    check_time = incorrect_date.split()
    if 'เวลา' in check_time:
        format_case = {
            'ม.ค':'01',
            'ก.พ.': '02',
            'มี.ค.': '03',
            'เม.ย.': '04',
            'พ.ค.': '05',
            'มิ.ย.': '06',
            'ก.ค.': '07',
            'ส.ค.': '08',
            'ก.ย.': '09',
            'ต.ค.': '10',
            'พ.ย.': '11',
            'ธ.ค.': '12'
        }
        month = check_time[1]
        check_time[1] = format_case[month]
        year = check_time[2]
        year = '25'+ year
        check_time[2] = str(int(year)-543)
        check_time[4] += ":00"
        correct_date = check_time[2]+'-'+check_time[1]+'-'+check_time[0]+' '+check_time[4]
        return correct_date
    else:
        time = check_time[1]
        if 'ชั่วโมง' in check_time:
            d = datetime.today() - timedelta(hours=int(time))
            correct_date = d.strftime('%Y-%m-%d %H:%M:%S')
            return correct_date
        else:
            d = datetime.today() - timedelta(minutes=int(time))
            correct_date = d.strftime('%Y-%m-%d %H:%M:%S')
            return correct_date

def forming_data():
    url = 'https://www.dek-d.com/loveroom/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return html_page


def get_content():
    html_page = forming_data()
    thread = html_page.find('section', {'id': 'loveroom_teen_tabmenu'}).find_next('div').find_all('a')
    store_url = []
    title = []
    content = []
    for i, s in enumerate(thread):
        store_url.append('https://www.dek-d.com' + s['href'])
        title.append(s['title'])
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        for i, url in enumerate(store_url):
            content = {'source': 'เด็กดี', 'type': 'ชีวิตวัยรุ่น', 'title': '', 'public_date': '', 'content': '',
                       'images': [], 'author': '', 'url': '',
                       'comment': []}
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print(soup.prettify())
            content['title'] = title[i]
            content['url'] = store_url[i]
            text = soup.find('section', {'id': "content-area"}).get_text(strip=True)
            text = text.replace("ตั้งกระทู้ใหม่", '').replace("Play0%Volume00:0000:00Full ScreenAd", '')
            content['content'] = text
            user = soup.find('div', {'class': "author-box -board"}).find('a', {'class': "user-link"})
            if user is not None:
                content['author'] = user.get_text()
            else:
                user = soup.find('div', {'class': "author-box -board"}).find('div', {'class': "user-link"})
                if user is not None:
                    content['author'] = user.get_text()

            mentionimg = soup.find_all('img',{'class':'mentionimg'})
            if mentionimg is not None:
                for img in mentionimg:
                    img_temp = {'url':img['src'],'alt':''}
                    content['images'].append(img_temp)
            # get comment section
            comments = soup.find_all('article', {'class': "comment-card-box comment-item-box"})
            if comments is not None:
                for _i, each_comment in enumerate(comments):
                    image = []
                    image_detail = {}
                    images = each_comment.find('div', {'class': "comment-text"}).find_all('img')
                    if image is not None:
                        for img in images:
                            image_detail['url'] = img['src']
                            image_detail['alt'] = ''
                            image.append(image_detail)
                    temp_com = {'content': each_comment.find('div', {'class': "comment-text"}).get_text(strip=True),
                                'author': each_comment.find('a', {'class': "alias-name"}).get_text(strip=True),
                                'time': each_comment.find('span', {'class': "time"}).get_text(strip=True),
                                'images': image
                                }
                    content['comment'].append(temp_com)
            date = soup.find('div', {'class': "author-box -board"}).find('span').get_text(strip=True)
            content['public_date'] = format_time(date)
            insert_database(content)
        driver.close()
    except WebDriverException:
        return 404


if __name__ == "__main__":
   get_content()