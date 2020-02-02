import requests
from urllib.parse import urlparse
import urllib.request
import time
import csv
import re
from bs4 import BeautifulSoup
from pathlib import Path

base_url = "https://guernseypress.com"

p = Path('data/articles.csv')
r = p.open('r')
reader = csv.reader(r.readlines())

def download_article(url, filepath):
    out_file = Path(filepath)
    
    if out_file.exists():
        print(filepath + ': already exists')
        return
    
    response = requests.get(url.geturl())
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find('div', class_='single-content').find_all('p')

    with out_file.open('w') as article_file:
        for para in content:
            if para.text == 'Advertising': #skip advetising
                continue;
            article_file.write(para.text)
            article_file.write('\n\n')
    print(filepath)

url_col = 0
date_col = 1
title_col = 2

for row in reader:
    dirpath = 'data/' + row[date_col]
    Path(dirpath).mkdir(parents=True, exist_ok=True)
    
    article_url = urlparse(base_url + row[url_col])
    filename = article_url.path.strip('/').rsplit('/', 1)[-1] + '.txt'
    filepath = dirpath+'/'+filename
    download_article(article_url, filepath)


