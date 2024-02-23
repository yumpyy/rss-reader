from bs4 import BeautifulSoup
import requests

# list of tags to be filtered
tagsNotAllowed = [
    "iframe",
    "h1",
    "button",
    # "a",
    "ul",
    "li",
    "style",
    "script",
    "link",
    "meta",
    # "video",
    "span",
    "form",
    "textarea",
    "nav",
    "svg"
]

headers = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36"
        }

def cleanHTML(articleURL):
    try:
        r = requests.get(articleURL, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return f"""
    <center>
        <h2>Couldn't Fetch</h2>
        <span>{e}<span>
    </center>
    """

    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    cleanHTMLCode = ""

    
    article = soup.find("article")

    # If the article tag is found get the content within that tag to reduce the amount of bloat to be filtered
    if article is not None:
        for tagName in tagsNotAllowed:
            for tag in article.find_all(tagName):
                tag.decompose()
        # filter out div tags which dont have any cotent in it
        for div in article.find_all():
            if not div.contents:
               div.decompose()

            # filter out junk from tags
            try:
                for attr in ["style", "class", "id", "type"]:
                    del div[attr]
            except AttributeError:
                continue
    else:
        for tag_name in tagsNotAllowed:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        for div in soup.find_all():
            if not div.contents:
               div.decompose()
            try:
                for attr in ["style", "class", "id", "type"]:
                    del div[attr]
            except AttributeError:
                continue

        article = soup

    try:
        websiteURL = "https://" + articleURL.split('/')[2] + "/"
        cleanHTMLCode = article.prettify()

        # change relative links to absolute
        cleanHTMLCode = cleanHTMLCode.replace('src="/',f'src="{websiteURL}')
        cleanHTMLCode = cleanHTMLCode.replace('href="/',f'href="{websiteURL}')
        return cleanHTMLCode

    except AttributeError:
        return f"""
    <center>
        <h2>Couldn't Fetch</h2>
    </center>
    """
