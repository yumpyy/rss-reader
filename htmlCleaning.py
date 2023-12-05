from bs4 import BeautifulSoup
import requests

tagsNotAllowed = [
    "iframe",
    "h1",
    "button",
    "a",
    "ul",
    "li",
    "style",
    "script",
    "link",
    "meta",
    "video",
    "span",
    "form",
    "textarea",
    "nav"
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

    if article:
        for tag in article.find_all(tagsNotAllowed):
            tag.decompose()

        for div in article.find_all():
            if not div.contents:
                div.decompose()

    else:
        for tag in soup.find_all(tagsNotAllowed):
            tag.decompose()

        for div in soup.find_all():
            if not div.contents:
                div.decompose()

        article = soup

    try:
        cleanHTMLCode = article.prettify()
        return cleanHTMLCode

    except AttributeError:
        return f"""
    <center>
        <h2>Couldn't Fetch</h2>
    </center>
    """
