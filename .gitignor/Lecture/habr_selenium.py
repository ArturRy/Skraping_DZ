from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

def wait_element(browser, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
browser = Chrome(service=browser_service)
browser.get('https://habr.com/ru/articles/')
article_tags = wait_element(browser, by=By.CLASS_NAME, value='tm-articles-list')


parsed_data = []

for article_tag in article_tags.find_elements(By.TAG_NAME, 'article'):
    h2_tag = article_tag.find_element(By.TAG_NAME, 'h2')
    a_tag = h2_tag.find_element(By.TAG_NAME, 'a')

    span_time_tag = article_tag.find_element(By.CLASS_NAME, 'tm-article-datetime-published')

    time_tag = wait_element(span_time_tag, 1, by=By.TAG_NAME, value='time')
    publish_time = time_tag.get_attribute('datetime')
    header = h2_tag.text
    link_absolute = a_tag.get_attribute('href')


    parsed_data.append({
        'link': link_absolute,
        'header': header,
        'publish_time': publish_time
    })

for item in parsed_data:
    time.sleep(0.1)
    link = item['link']
    browser.get(link)
    article_tag = wait_element(browser, 1, By.ID, value='post-content-body')
    article_text = article_tag.text
    item['article_text'] = article_text




