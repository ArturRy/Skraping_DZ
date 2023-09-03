"""
<span class="table-ip4-home">
                         83.168.22.81    </span>
"""

import requests
import bs4

response = requests.get('https://www.iplocation.net/')
html_data = response.text
soup = bs4.BeautifulSoup(html_data, 'lxml')
span_tag = soup.find('span', class_="table-ip4-home")
ip_4 = span_tag.text.strip()
print(ip_4)