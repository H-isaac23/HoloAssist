from ysl.YSL import StreamLiker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from collections import OrderedDict
import os
import time


class HoloAssist(StreamLiker):
    def __init__(self, channels_path, email, passwd):
        super(HoloAssist, self).__init__(channels_path, email, passwd)
        self.link = None

    def open_holotools(self):
        print()
        self.link = 'https://hololive.jetri.co/#/watch?videoId=' + ",".join(self.active_streams)

        if self.link == 'https://hololive.jetri.co/#/watch?videoId=':
            print("No streamers are currently streaming.")
            self.driver_quit()
        else:
            self.driver.get(self.link)
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div/main/div/div/div/div[3]/div[1]'))
            )

            self.driver.execute_script("localStorage.setItem('rulePauseOther', 0);")
            time.sleep(5)
            self.driver.refresh()
            time.sleep(10)

            for i in range(1, self.number_of_active_streams + 1):
                try:
                    num = str(i)
                    print(num, f'/html/body/div/main/div/div/div/div[3]/div[{num}]')
                    elm = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'/html/body/div/main/div/div/div/div[3]/div[{num}]'))
                    )
                    ActionChains(self.driver).move_to_element(elm).click(elm).perform()
                    time.sleep(2)
                except:
                    print("Yeah an error")

            mute_videos = self.driver.find_element_by_xpath('/html/body/div/main/div/div/div/div[1]/div[4]/div[2]/div[2]')
            ActionChains(self.driver).move_to_element(mute_videos).click().perform()
            time.sleep(5)


    def clear_data(self):
        self.start_time = None
        self.time_started = None
        self.total_time_elapsed = 0
        self.time_ended = None

        self.currently_streaming = {}
        self.streams_liked = {}
        self.streams_liked_id = []
        self.video_ids = []
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0
        self.active_streams = []
        self.date = None
        self.link = None

    @staticmethod
    def close_browser():
        os.system("TASKKILL /F /IM firefox.exe")

    def send_email(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.driver.get("https://mail.google.com/mail/u/0/#inbox")

        compose = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=":bv"]/div/div'))
        )

        ActionChains(self.driver).move_to_element(compose).click(compose).perform()

        to = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[23]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/textarea'))
        )

        ActionChains(self.driver).move_to_element(to).click(to).perform()

        to.send_keys("dev.isaac23@gmail.com")

        sub = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[23]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[3]/div/input'))
        )

        ActionChains(self.driver).move_to_element(sub).click(sub).perform()

        sub.send_keys("Test")

        msg = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[23]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[2]/div[2]/div'))
        )

        ActionChains(self.driver).move_to_element(msg).click(msg).perform()

        msg.send_keys("Hi")

        send = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[23]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]'))
        )

        ActionChains(self.driver).move_to_element(send).click(send).perform()



if __name__ == "__main__":
    email = os.environ.get('TEST_EMAIL')
    passwd = os.environ.get('TEST_PASS')
    hta = HoloAssist('channel ids.txt', email, passwd)
    hta.close_browser()
    hta.config_driver('C:/Program Files (x86)/geckodriver.exe', ['--mute-audio'])
    hta.start_liking_with_data("isaac", "localhost", "DevAisha23!", "YSL", "stream_data",
                              "C:/Users/ISAAC/PycharmProjects/videoLikerYoutube2.0/Stream data")
    hta.open_holotools()
    hta.clear_data()

    # hta = HoloAssist(email, passwd, sl.number_of_active_streams)
    # hta.config_driver('C:/Program Files (x86)/geckodriver.exe', ['--mute-audio'])
    # hta.link = 'https://hololive.jetri.co/#/watch?videoId=' + ','.join(sl.streams_liked_id)
    # hta.open_holotools()
    # hta.clear_data()
    # hta.driver_quit()
