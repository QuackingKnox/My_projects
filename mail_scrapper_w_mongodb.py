from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['db_mail_ru']
letters = db.letters

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')

elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:login-input')))
elem.send_keys('study.ai_172@mail.ru')
elem.submit()

elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:password-input')))
elem.send_keys('NextPassword172')
elem.submit()

WebDriverWait(driver, 5).until(EC.title_contains('Входящие'))

last_message_url = None
message_url_list = []

while True:
    tmp_list = driver.find_elements_by_xpath('//a[contains(@class,"js-letter-list-item")]')
    last_message_element = tmp_list[-1]

    for i in range(len(tmp_list)):
        tmp_list[i] = tmp_list[i].get_attribute('href')

    if tmp_list[-1] == last_message_url:
        break

    for item in message_url_list:
        try:
            tmp_list.remove(item)
        except ValueError:
            continue

    message_url_list.extend(tmp_list)

    action = ActionChains(driver)
    action.move_to_element(last_message_element)
    action.perform()

    last_message_url = tmp_list[-1]
dict_list = []

for item in message_url_list:
    driver.get(item)
    elem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))

    new_dict = {}

    new_dict['subject'] = elem.text
    new_dict["author's email"] = driver.find_element_by_xpath("//div[@class='letter__author']/span").get_attribute('title')
    new_dict['author_name'] = driver.find_element_by_xpath('//div[@class="letter__author"]/span').text
    new_dict['time'] = driver.find_element_by_xpath('//div[@class="letter__date"]').text.split(',')
    new_dict['text'] = driver.find_element_by_xpath('//div[contains(@id,"_BODY")]').text
    letters.insert_one(new_dict)
    dict_list.append(new_dict)

print(dict_list)
