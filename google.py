import os
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
if not CHROMEDRIVER_PATH:
    print(f'CHROMEDRIVER_PATH:{CHROMEDRIVER_PATH}')
    exit(0)

# 创建一个新的Chrome浏览器实例
driver = webdriver.Chrome(CHROMEDRIVER_PATH)

# 打开Google搜索引擎
driver.get("https://www.google.com/")

# 在搜索框中输入关键词并按下Enter键
search_box = driver.find_element_by_name("q")
search_box.send_keys("Python Selenium")
search_box.send_keys(Keys.RETURN)

# 获取搜索结果的标题和URL
search_results = driver.find_elements_by_css_selector("div.g")
for result in search_results:
    title_element = result.find_element_by_css_selector("h3")
    title = title_element.text
    url_element = result.find_element_by_css_selector("a")
    url = url_element.get_attribute("href")
    print(f"{title}: {url}")

# 关闭浏览器实例
driver.quit()
