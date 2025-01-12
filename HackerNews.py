# ethical and unethical ways to scrape a website's data
# use a website's /robots.txt to see what's allowed

import requests
from bs4 import BeautifulSoup
import pprint

# grabbing website and parsing w bs4
response = requests.get("https://news.ycombinator.com/news")
response2 = requests.get("https://news.ycombinator.com/news?p=2")
soup = BeautifulSoup(response.text, "html.parser")
soup2 = BeautifulSoup(response2.text, "html.parser")

# grabbing the article links and votes
links = soup.select(".titleline > a")
links2 = soup2.select(".titleline > a")
subtext = soup.select(".subtext")
subtext2 = soup2.select(".subtext")

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories(hnlist):
    return sorted(hnlist, key=lambda k:k["votes"], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        vote = subtext[index].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_stories(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))