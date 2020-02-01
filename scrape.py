import requests
import urllib.request
import time
import csv
import re
from bs4 import BeautifulSoup
from pathlib import Path

base_url = "https://guernseypress.com/news/archive/"
data = []
keep_going = True
next_link = ''
stop_at = ''

p = Path('articles.csv')
if p.is_file():
    with p.open('r') as r:
        line = r.readline()
        reader = csv.reader([line])
        for row in reader:
            print(row[0])
            stop_at = row[0]

#/news/2020/01/13/a-call-for-more-women-in-power/
#/news/2020/01/13/a-call-for-more-women-in-power/

def add_to_data(articles):
    for i, article in enumerate(articles):
        try:
            url = article.a['href']
            
            if url == stop_at:
                return False
                break
            date = re.search("\d{4}/\d{2}/\d{2}", url).group()
            title = article.find(['h2', 'h3', 'h4']).string
            data.append([url, date, title])
            print(i)
        except:
            pass
            #print("inner error")
    return True

def write_and_merge():
    print(p.name)
    if list.count(data) == 0:
        return

    if p.is_file():
        p.rename('articles.bak')

    with p.open('w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)

        b = Path('articles.bak')
        if b.is_file():
            with b.open('r') as rf:
                csvFile.writelines(rf.readlines())
            b.unlink()


while keep_going:
    get_url = base_url + next_link
    response = requests.get(get_url)
    soup = BeautifulSoup(response.text, "html.parser")

    print(keep_going)

    try:
        articles = soup.select("article")
        keep_going = add_to_data(articles)
        print(keep_going)
    except:
        print("data error")

    try:
        next_link = soup.find('a', class_='pagination-item-next')['href']
    except:
        break

    if '2002' in next_link:
        break


time.sleep(5)

# print(data)

write_and_merge()