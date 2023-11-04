import feedparser

def atomReader(url):
    parser = feedparser.parse(url)
    # print(parser)
    # print(parser['entries'][0]['summary'])
    feed = {
            'title' : parser['entries'][5]['title'],
            'published' : parser['entries'][5]['published'],
            'linkOriginal' : parser['entries'][5]['links'][0]['href'],
            'preview-image' : parser['entries'][5]['media_content'][0]['url'],
            'content' : parser['entries'][5]['content'][0]['value']
    }

    return feed

# atomReader("test2.rss")
