'''
div class="tm-articles-list"
'''
'''
article
'''

'''
<h2 class="tm-title tm-title_h2">
<a href="/ru/articles/757476/" class="tm-title__link" data-test-id="article-snippet-title-link" data-article-link="true"><span>Как я создал свой дипфейк для презентации</span></a></h2>
'''
'''
div id="post-content-body"
'''
'''
<span class="tm-article-datetime-published"><time datetime="2023-08-28T16:17:50.000Z" title="2023-08-28, 19:17">44 минуты назад</time></span>
'''

import requests
import bs4
import fake_headers
import time

headers_gen = fake_headers.Headers(browser='firefox', os='win')
response = requests.get('https://habr.com/ru/articles/',
                        headers=headers_gen.generate(), proxies={})
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')

div_article_list_tag = main_soup.find('div', class_='tm-articles-list')

article_tags = div_article_list_tag.find_all('article')

parsed_data = []

for article_tag in article_tags:
    h2_tag = article_tag.find('h2', class_='tm-title_h2')
    a_tag = h2_tag.find('a')
    span_time_tag = article_tag.find('span', class_='tm-article-datetime-published')
    time_tag = span_time_tag.find('time')

    publish_time = time_tag['datetime']
    link_relative = a_tag['href']
    header = h2_tag.text

    link_absolute = f'https://habr.com{link_relative}'

    time.sleep(0.1)
    response_article_full = requests.get(link_absolute, headers=headers_gen.generate())
    response_article_full_html = response_article_full.text
    article_full_soup = bs4.BeautifulSoup(response_article_full_html, features='lxml')
    article_full_tag = article_full_soup.find('div', id='post-content-body')
    article_full_text = article_full_tag.text

    parsed_data.append({
        'link': link_absolute,
        'header': header,
        'publish_time': publish_time,
        'article_full_text': article_full_text
    })



print(parsed_data)



