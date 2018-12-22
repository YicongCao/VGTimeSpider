import re
import requests
import html2text
import urllib
import os
from time import sleep

topic_url = []
error_count = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/49.0.2623.87 Safari/537.36'
}

for i in range(2000):
    req_template = "https://www.vgtime.com/topic/index/load.jhtml?page={0}&pageSize=50"
    r = requests.get(req_template.format(i+1), headers=headers)
    if r.status_code != 200:
        error_count += 1
        print('error [{0}] crawling page [{1}]'.format(r.status_code, i))
        print('total error times: [{0}]'.format(error_count))
    else:
        links = re.findall(r'(\/topic.*?jhtml)', r.text)
        links = list(set(links))
        topic_url.extend(links)
        print('extended [{0}] links'.format(len(links)))
        if (len(links) == 0):
            error_count += 1
    if error_count > 3:
        break
    # sleep(0.01)

topic_url = list(set(topic_url))
print('got [{0}] urls'.format(len(topic_url)))

curr_dir = os.path.abspath(os.path.curdir)
topic_file = open('gametopicex.txt', 'w', encoding='utf-8')
converter = html2text.HTML2Text()
converter.ignore_images = True
converter.ignore_emphasis = True
converter.ignore_links = True
converter.ignore_tables = True
converter.strong_mark = ''
error_count = 0

for url in topic_url:
    url = urllib.parse.urljoin('https://www.vgtime.com/', url)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        error_count += 1
        print('error [{0}] crawling page [{1}]'.format(r.status_code, url))
        print('total error times: [{0}]'.format(error_count))
    else:
        idx_start = r.text.find("<article>")
        idx_end = r.text.find("</article>")
        article = r.text[idx_start:idx_end]
        content = converter.handle(article)
        topic_file.write(content + '\r\n======\r\n')
        # topic_file.flush()
        print(content + "\r\n======\r\n")
    # sleep(0.01)
    # if error_count > 3:
    #     print('error too many times')
    #     break

topic_file.close()
