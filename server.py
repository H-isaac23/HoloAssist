from flask import Flask, render_template
from holo_assist import HoloAssist

user = "isaac"
host = "localhost"
passwd = "DevAisha23!"
db = "YSL"
table_name = "stream_data"
my_dir = "C:/Users/ISAAC/PycharmProjects/YSL/Stream data"
path = 'C:/Program Files (x86)/geckodriver.exe'
profile = 'C:/Users/ISAAC/AppData/Roaming/Mozilla/Firefox/Profiles/fwnbfuph.default-release'

hta = HoloAssist('channel ids.txt')
hta.send_ip_add()
hta.close_browser()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/like')
def like():
    hta.close_browser()
    hta.get_start_time()
    hta.check_streams()
    hta.config_driver(path, profile, mute_sound=True)
    hta.like_videos()
    hta.get_end_time()
    hta.append_data_on_file(my_dir)
    hta.append_data_on_db(user, host, passwd, db, table_name)
    hta.open_holotools()
    hta.clear_data()
    return render_template('like.html')

if __name__ == '__main__':
    app.run(debug=True, host=hta.ip_add)