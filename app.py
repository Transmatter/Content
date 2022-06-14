import pymongo
from flask import Flask
from flask import request
from newsapi import NewsApiClient
from Database.database import insert_database, get_database
import json
import Controller.Thairath as tr
import Controller.dekd as dekd
import Controller.Sanook as sanook

app = Flask(__name__)


@app.route('/')
def home():
    return 'hello, enjoy'


@app.route('/LocalNews')
def fetch_local_news():  # put application's code here
    tr.get_content()
    dekd.get_content()
    # sanook.get_content()
    collection = get_database()
    collection.find({}).sort("public_date" ,-1 )
    return 'news have been store in database'  # return http response or json {message: }


@app.route('/InterNews', methods=['GET'])
def fetch_inter_news():
    topic = request.args.get('topic')
    time = request.args.get('time')
    API_KEY = '52416b411fea44b1be07faf152d9f178'
    newsapi = NewsApiClient(API_KEY)
    all_articles = newsapi.get_everything(q=topic,
                                          from_param=time,
                                          language='en',
                                          page_size=5,
                                          page=1,
                                          sort_by='relevancy')
    # readable_news = json.dumps(all_articles,indent=4)

    articles = all_articles['articles']
    news_format = {}
    print(articles)
    for article in articles:

        news_format = {'source': article['source']['name'], 'type': 'random ', 'title': article['title'],
                       'public_date': article['publishedAt'], 'content': article['content'],
                       'images': [{'alt':'','url':article['urlToImage']}],
                       'author': article['author'], 'url': article['url']}

        date = news_format["public_date"]
        time = ''
        i = 0
        for d in date:
            if not d.isalpha():
                time += d
            elif i == 0:
                time += ' '
                i = 1
        news_format["public_date"] = time
        insert_database(news_format)
    collection = get_database()
    collection.find().sort('public_date', -1)
    # return http response or json {message: }
    return 'added news successfully'# return http response or json {message: }


if __name__ == '__main__':
    app.run()
