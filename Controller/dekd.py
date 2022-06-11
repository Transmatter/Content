from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from Database.database import insert_database
from webdriver_manager.chrome import ChromeDriverManager


def forming_data():
    url = 'https://www.dek-d.com/loveroom/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return html_page


def get_content():
    html_page = forming_data()
    thread = html_page.find('section', {'id':'loveroom_teen_tabmenu'}).find_next('div').find_all('a')
    store_url = []
    title = []
    content = []
    for i, s in enumerate(thread):
        store_url.append('https://www.dek-d.com'+s['href'])
        title.append(s['title'])
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        for i,url in enumerate(store_url):
            content = {'source':'เด็กดี','type':'ชีวิตวัยรุ่น','title': '', 'public_date': '', 'content': '', 'images': [], 'author': '', 'url': '',
                       'comment': []}
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print(soup.prettify())
            content['title'] = title[i]
            content['url'] = store_url[i]
            text = soup.find('section', {'id': "content-area"}).get_text(strip=True)
            text =text.replace("ตั้งกระทู้ใหม่",'').replace("Play0%Volume00:0000:00Full ScreenAd",'')
            content['content'] = text
            user = soup.find('div',{'class':"author-box -board"}).find('a',{'class':"user-link"})
            if user is not None:
                content['author'] = user.get_text()
            else:
                user = soup.find('div', {'class': "author-box -board"}).find('div', {'class': "user-link"})
                if user is not None:
                    content['author'] = user.get_text()
            # print(content[content])
            # print("*******************")
            #get comment section
            comments = soup.find_all('article',{'class':"comment-card-box comment-item-box"})
            if comments is not None:
                for _i,each_comment in enumerate(comments):
                    temp_com = {'com_detail': each_comment.find('div', {'class': "comment-text"}).get_text(strip=True),
                                'name': each_comment.find('a', {'class': "alias-name"}).get_text(strip=True),
                                'time': each_comment.find('span', {'class': "time"}).get_text(strip=True)}
                    content['comment'].append(temp_com)
            content['public_date'] = soup.find('div',{'class':"author-box -board"}).find('span').get_text(strip=True)
            insert_database(content)
        driver.close()
    except WebDriverException:
        return 404
    



if __name__ == "__main__":
    print(get_content())