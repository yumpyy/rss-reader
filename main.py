import feedparser

def atomReader(url):
    parser = feedparser.parse(url)
    # print(parser)
    print(len(parser['entries']))
    # print(parser['entries'][0]['summary'])
    articles = []
    for x in range(len(parser['entries'])):
        feed = {
                'title' : parser['entries'][x]['title'],
                'published' : parser['entries'][x]['published'],
                'linkOriginal' : parser['entries'][x]['links'][0]['href'],
                # 'preview-image' : parser['entries'][x]['media_content'][0]['url'],
                'content' : parser['entries'][x]['content'][0]['value']
        }
        # print(feed)
        articles.append(feed)
    
    return articles

atomReader("test2.rss")
