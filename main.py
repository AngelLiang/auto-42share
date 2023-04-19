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
import log
import config

from dotenv import load_dotenv
load_dotenv()


CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
CHATGPT_APIKEY = os.getenv('CHATGPT_APIKEY')


driver = None


def gen_random_second(min=8, max=15) -> int:
    return random.randint(min, max) + random.random()


def click_setting():
    wait = WebDriverWait(driver, 120)
    button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div[1]/div[3]/div[1]/div[2]/div"))
    )
    button.click()


def enter_api_key(api_key=CHATGPT_APIKEY):
    # 显式等待
    wait = WebDriverWait(driver, 120)
    apikey_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='OpenAI API Key']"))
    )
    apikey_input.send_keys(api_key)
    log.logger.info('设置apikey')


def return_chat():
    new_chat = driver.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div")
    new_chat.click()
    log.logger.info('返回对话框')


def create_new_chat():
    wait = WebDriverWait(driver, 60)
    new_chat = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div/div[1]/div[3]/div[2]/div"))
    )
    new_chat.click()
    log.logger.info('创建新的对话框')


def send_message(text):
    wait = WebDriverWait(driver, 60)
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
    log.logger.info('发送消息')


def wait_reply_finish():
    entering_flag = driver.find_elements_by_class_name(
        'home_chat-message-status__EsVNi')
    log.logger.info('正在输入...')
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
    log.logger.info('分享并获取连接')
    return driver.current_url


def switch_chat():
    sleep(3)
    # 获取所有窗口句柄
    window_handles = driver.window_handles
    # 切换到第一个窗口
    driver.switch_to.window(window_handles[0])
    log.logger.info('切换对话框')
    # 等待切换
    sleep(3)


def start(api_key=CHATGPT_APIKEY, filepath='questions.csv'):
    log.logger.info('启动浏览器')
    global driver
    # 创建一个新的Chrome浏览器实例
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_extension('42share.crx')
    chromedriver_path = config.get_chromedriver_path()
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)

    driver.get("https://chat.42share.io/")
    log.logger.info('访问 https://chat.42share.io/')

    click_setting()
    enter_api_key(api_key)
    return_chat()

    question_group = read_csv.read_questions(filepath)
    for i, questions in enumerate(question_group, start=1):
        if len(questions) < 5:
            log.logger.info(f'第{i}行的问题小于5个，跳过')
            continue
        title = ''
        for j, chat_message in enumerate(questions):
            if not chat_message:
                log.logger.info(f'第{i}行第{j}列问题为空，跳过')
                continue
            if j == 0:
                # 取第一个问题作为标题
                title = chat_message
            send_message(chat_message)
            wait_reply_finish()
            reply = get_reply()
            if '出错了，稍后重试' in reply:
                log.logger.error('出错了，直接退出')
                exit(0)
                send_message(chat_message)
                wait_reply_finish()
        # send_message("请用10字以内总结前面全部对话")
        # wait_reply_finish()
        # title = get_reply()
        share_url = click_share_and_get_url()
        log.logger.info(f'{title} {share_url}')
        if title and share_url:
            write_excel.write_to_excel(title, share_url)

        switch_chat()
        # 打开新的对话框
        create_new_chat()
        # 等待一段时间
        sleep(7)

    # 关闭浏览器实例
    # driver.quit()


if __name__ == "__main__":
    start()
    # create_new_chat()
    # click_share_and_get_url()
