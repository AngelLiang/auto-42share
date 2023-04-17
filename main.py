import os
from time import sleep
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import read_csv
import write_excel


from dotenv import load_dotenv
load_dotenv()


CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
CHATGPT_APIKEY = os.getenv('CHATGPT_APIKEY')
SHARE_TITLE = '分享 Prompt'

if not CHROMEDRIVER_PATH:
    print(f'CHROMEDRIVER_PATH:{CHROMEDRIVER_PATH}')
    exit(0)

# 创建一个新的Chrome浏览器实例
chrome_options = Options()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--start-maximized")
chrome_options.add_extension('42share.crx')
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)

driver.get("https://chat.42share.io/")


wait = WebDriverWait(driver, 20)


def gen_random_second(min=8, max=15) -> int:
    return random.randint(min, max) + random.random()


def click_setting():
    button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div[1]/div[3]/div[1]/div[2]/div"))
    )
    button.click()


def enter_api_key():
    # 显式等待
    apikey_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='OpenAI API Key']"))
    )
    apikey_input.send_keys(CHATGPT_APIKEY)


def return_chat():
    new_chat = driver.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div")
    new_chat.click()


def create_new_chat():
    new_chat = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div/div[1]/div[3]/div[2]/div"))
    )
    new_chat.click()


def send_message(text):
    chat_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.home_chat-input-panel-inner__8J59p > textarea.home_chat-input__qM_hd"))
    )
    chat_input.send_keys(text)
    send_button = driver.find_element_by_class_name(
        "home_chat-input-send__rsJfH")
    random_second = gen_random_second()
    sleep(random_second)  # 等待几秒再发送
    send_button.click()


def wait_reply_finish():
    entering_flag = driver.find_elements_by_class_name(
        'home_chat-message-status__EsVNi')
    print('正在输入...')
    while len(entering_flag) >= 1:
        sleep(3)
        entering_flag = driver.find_elements_by_class_name(
            'home_chat-message-status__EsVNi')


def get_reply():
    div_element = driver.find_elements_by_class_name(
        'home_chat-message-item__hDEOq')[-1]
    # 查找class为markdown-body的下级p元素
    p_element = div_element.find_element_by_class_name(
        'markdown-body').find_element_by_tag_name('p')
    # 获取p元素文本值
    text = p_element.text
    return text


def click_share_and_get_url() -> str:
    # 点击分享
    elem = driver.find_element_by_xpath("//div[@title='分享 Prompt']")
    elem.click()
    # 等待一定时间，让新窗口完全打开
    sleep(10)
    # 获取所有窗口句柄
    window_handles = driver.window_handles
    # 切换到新打开的窗口
    driver.switch_to.window(window_handles[-1])
    return driver.current_url


def switch_chat():
    sleep(3)
    # 获取所有窗口句柄
    window_handles = driver.window_handles
    # 切换到第一个窗口
    driver.switch_to.window(window_handles[0])
    # 等待切换
    sleep(3)


def main():
    click_setting()
    enter_api_key()
    return_chat()

    question_group = read_csv.read_questions()
    for questions in question_group:
        for chat_message in questions:
            if not chat_message:
                continue
            send_message(chat_message)
            wait_reply_finish()
        send_message("请用10字以内总结前面全部对话")
        wait_reply_finish()
        title = get_reply()
        share_url = click_share_and_get_url()
        print(f'{title} {share_url}')
        if title and share_url:
            write_excel.write_to_excel(title, share_url)

        switch_chat()

        # 打开新的对话框
        create_new_chat()
        # 等待一段时间
        sleep(7)

    # 关闭浏览器实例
    # driver.quit()


main()
# create_new_chat()
# click_share_and_get_url()
