from flask import Flask
import Controller.Thairath as tr
import Controller.dekd as dekd
import Controller.Sanook as sanook


app = Flask(__name__)


@app.route('/')
def fetch_news():  # put application's code here
    tr.get_content()
    dekd.get_content()
    sanook.get_content()
    return 'news have been store in database'


if __name__ == '__main__':
    app.run()
