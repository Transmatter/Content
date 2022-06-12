from flask import Flask
from flask import request
from newsapi import NewsApiClient
import json
import Controller.Thairath as tr
import Controller.dekd as dekd
import Controller.Sanook as sanook

app = Flask(__name__)


@app.route('/')
def home():
    return 'hello, enjoy'


@app.route('/LocalNews')
def fetch_news():  # put application's code here
    tr.get_content()
    dekd.get_content()
    sanook.get_content()
    return 'news have been store in database'


@app.route('/InterNews', methods=['GET'])
def fetch_inter_news():
    topic = request.args.get('topic')
    time = request.args.get('time')
    API_KEY = '52416b411fea44b1be07faf152d9f178'
    newsapi = NewsApiClient(API_KEY)
    all_articles = newsapi.get_everything(q=topic,
                                          from_param=time,
                                          language='en',
                                          sort_by='relevancy')
    readable_news = json.dumps(all_articles,indent=4)
    print(readable_news)
    print(type(readable_news))
    return readable_news


if __name__ == '__main__':
    app.run()
