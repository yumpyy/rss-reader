import feedparser
from db import urlsFromDatabase

def feedFetch():
    urlData = urlsFromDatabase()
    # print(urls)
    # global articles
    articles = []
    feed = {}

    for url in urlData:
        # print(url)
        parser = feedparser.parse(url[0])
        # print(parser)
        for x in range(len(parser['entries'])):
            feed = {
                    'feed-name' : url[1],
                    'title' : parser['entries'][x]['title'],
                    'published' : parser['entries'][x]['published_parsed'],
                    'linkOriginal' : parser['entries'][x]['links'][0]['href']
                    }

            # if 'summary' in feed:
            #     feed['summary'] = parser['entries'][x]['summary']
            # else:
            #     feed['summary'] = ''

            if 'content' in feed:
                feed['content'] = parser['entries'][x]['content'][0]['value']
            else:
                feed['content'] = parser['entries'][x]['summary']

            articles.append(feed)

    articles = dateSort(articles)
    return articles

def dateSort(articles):
    for article in articles:
        date = article['published']
        date = list(date)
        # date = f'{date[0]}/{date[1]}/{date[2]} {date[3]}:{date[4]}'
        # article['published'] = date 

    articles.sort(key=lambda article: (article['published'][0], article['published'][1], article['published'][2], article['published'][3], article['published'][4]), reverse=True)

    for article in articles:
        date = article['published']
        date = list(date)
        date = f'{date[0]}/{date[1]}/{date[2]} {date[3]}:{date[4]}'
        article['published'] = date 

    # print(articles)
    return articles
    
feedFetch()
# dateSort(feedFetch())
