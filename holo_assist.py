from ysl.YSL import StreamLiker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import smtplib, ssl
from selenium.webdriver.common.action_chains import ActionChains
from collections import OrderedDict
import subprocess
import os
import time


class HoloAssist(StreamLiker):
    def __init__(self, channels_path):
        super(HoloAssist, self).__init__(channels_path)
        self.ip_add = None
        self.link = None

    def open_holotools(self):
        print()
        self.link = 'https://hololive.jetri.co/#/watch?videoId=' + ",".join(self.currently_streaming.values())

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

    @staticmethod
    def close_browser():
        os.system("TASKKILL /F /IM firefox.exe")

    def send_ip_add(self):
        port = 465  # For SSL
        password = os.environ.get("TEST_PASS")

        # Create a secure SSL context
        context = ssl.create_default_context()

        receiver = "dev.isaac23@gmail.com"
        sender = "sparklypotato23@gmail.com"

        data = subprocess.check_output(['ipconfig']).decode('utf-8').split('\n')
        self.ip_add = data[23][39:].strip()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("sparklypotato23@gmail.com", password)
            server.sendmail(sender, receiver, self.ip_add)
