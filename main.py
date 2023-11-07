import feedparser
from db import urlsFromDatabase

def feedFetch():
    urls = urlsFromDatabase()
    print(urls)
    articles = []

    for url in urls:
        print(url)
        parser = feedparser.parse(url)

        for x in range(len(parser['entries'])):
            feed = {
                    'title' : parser['entries'][x]['title'],
                    'published' : parser['entries'][x]['published'],
                    'link-original' : parser['entries'][x]['links'][0]['href'],
                    'content' : parser['entries'][x]['content'][0]['value']
            }
            articles.append(feed)
        
    return articles

feedFetch()
