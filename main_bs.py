import unicodedata

import requests
import bs4
import fake_headers
from pprint import pprint
from unicodedata import normalize

count = 0
html = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=Python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={count}&disableBrowserCache=true'
fakeHeader = fake_headers.Headers(browser='chrome', os='win')
response = requests.get(f'{html}', headers=fakeHeader.generate())
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')
count1 = main_soup.find('h1', class_='bloko-header-section-3').text.split(' ')[0]

job = []
while len(job) < int(count1):

    html = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=Python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={count}&disableBrowserCache=true'
    fakeHeader = fake_headers.Headers(browser='chrome', os='win')
    response = requests.get(f'{html}', headers=fakeHeader.generate())
    main_html = response.text
    main_soup = bs4.BeautifulSoup(main_html, 'lxml')
    div2 = main_soup.find_all('div', class_='serp-item')

    for items in div2:
        h3 = items.find('h3', class_='bloko-header-section-3')
        span = h3.find('span')
        a = span.find('a', class_='serp-item__title')
        pay = items.find('span', class_='bloko-header-section-2')
        if pay:
            pay = pay.text
        else:
            pay = 'Зарплата не указана'
        company = items.find('div', class_='bloko-text').text
        city = items.find_all('div', class_='bloko-text')[1].text

        job.append(
            {'link': a['href'],
             'pay': unicodedata.normalize('NFKC', pay),
             'company': unicodedata.normalize('NFKC', company),
             'city': unicodedata.normalize('NFKC', city)
             }
        )

        next1 = (main_soup.find('div', class_='bloko-gap bloko-gap_top'))
        html2 = ((next1.find('a', class_='bloko-button')['href']))
    count += 1

# pprint((job))
print(len(job))
usd = ['USD', 'usd', '$']
usd_job = []
for j in job:
    if j['pay'].split(' ')[-1] in usd:
        usd_job.append(j)
pprint(usd_job)
print(len(usd_job))