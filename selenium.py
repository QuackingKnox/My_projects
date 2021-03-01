import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re

data = pd.read_csv('data.csv')

missed_data_3 = data[data.isnull()['Room Scheduling Product']]

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)


competitor = ['CollegeNet', '25LIVE', 'Ad astra', 'EMS']
counter = 0

for i in missed_data_3['Account Name']:
    counter += 1
    if counter in missed_data_3.index.tolist():
        a = True
        for j in competitor:
            q_list = i.split()
            q_list.append(j)
            q_string = '+'.join(q_list)
            if j == 'EMS':
                q_string = q_string + '+-emergency+-medical+-services'
            driver.get(f'https://www.google.com/search?q={q_string}')
            time.sleep(5)
            element = driver.find_elements_by_xpath("//div[@class='g']")
            for e in element[:3]:
                not_found = e.find_elements_by_xpath(".//span[text()='Не найдено:']")
                cite = e.find_elements_by_partial_link_text('.edu')
                data.at[counter, 'Room Scheduling Product'] = 'No Solution'
                if not not_found and e.find_elements_by_partial_link_text('.edu'):
                    data.at[counter, 'Room Scheduling Product'] = j
                    a = False
                    break
            if a != True:
                break
