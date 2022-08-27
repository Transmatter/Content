from flask import Flask ,make_response
from flask import request
from newsapi import NewsApiClient
from Database.database import insert_database, get_database
import Controller.Thairath as tr
import Controller.dekd as dekd
import Controller.Sanook as sanook
from flask_cors import cross_origin,CORS
import service.spell_correction as sc
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
# model = sc.train_model()

@app.route('/')
def home():
    return 'hello, enjoy'


@app.route('/LocalNews')
@cross_origin()
def fetch_news():  # put application's code here
    tr.get_thairath_content()
    # dekd.get_content()
    sanook.get_content()
    collection = get_database()
    collection.find().sort('public_date',-1)
    return 'news have been store in database'  # return http response or json {message: }


@app.route('/InterNews', methods=['GET'])
@cross_origin()
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

        news_format = {'source': article['source']['name'], 'category': 'random ', 'title': article['title'],
                       'publicDate': article['publishedAt'], 'content': article['content'],
                       'images': [{'alt':'','url':article['urlToImage'], 'verifyStatus':"EMPTY", 'verifiedBy':'','verifiedDate':''}],
                       'author': article['author'], 'url': article['url']
                       ,"approveStatus":"NOT_APPROVE", 'approvedBy':'', 'approvedDate':'', 'type':'INTER_CONTENT'
                       }

        date = news_format["publicDate"]
        time = ''
        i = 0
        for d in date:
            if not d.isalpha():
                time += d
            elif i == 0:
                time += ' '
                i = 1
        news_format["publicDate"] = time
        insert_database(news_format)
    collection = get_database()
    collection.find().sort('publicDate', -1)
    # return http response or json {message: }
    return 'added news successfully'# return http response or json {message: }

# @app.route('/spellcheck', methods=['GET'])
# @cross_origin()
# def spell_check():
#     args = request.args
#     keyword = args.get('keyword')
#     return make_response(sc.check_spell_correction(model,keyword))

if __name__ == '__main__':
    app.run()
