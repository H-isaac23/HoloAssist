from flask import Flask, render_template
from holo_assist import HoloAssist
import os

email = os.environ.get('TEST_EMAIL')
passwd = os.environ.get('TEST_PASS')
hta = HoloAssist('channel ids.txt', email, passwd)
hta.close_browser()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/like')
def like():
    hta.close_browser()
    hta.start_liking_with_data("isaac", "localhost", "DevAisha23!", "YSL", "stream_data",
                               "C:/Users/ISAAC/PycharmProjects/videoLikerYoutube2.0/Stream data")
    hta.open_holotools()
    hta.clear_data()
    return render_template('like.html')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.12')