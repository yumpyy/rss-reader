from bs4 import BeautifulSoup
import requests

# list of tags to be filtered
tags_not_allowed = [
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

def sanitize(articleURL):
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
    sanitized_code = ""
    article = soup.find("article")

    # If the article tag is found get the content within that tag to reduce the amount of bloat to be filtered
    if article is not None:
        for tagName in tags_not_allowed:
            for tag in article.find_all(tagName):
                tag.decompose()
        # filter out div tags which dont have any cotent in it
        for div in article.find_all():
            try:
                for attr in ["style", "class", "id", "type"]:
                    if div.name == 'img' and attr in ['width', 'height']:
                        continue  # Skip deleting width and height attributes from img tags
                    del div[attr]
            except AttributeError:
                continue

            if div.name not in ['img', 'video'] and not div.contents:
                div.decompose()
    else:
        for tag_name in tags_not_allowed:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        for tag in soup.find_all():
            try:
                for attr in list(tag.attrs.keys()):
                    if attr in ["href", "src"]:
                        continue
                    if tag.name == 'img' and attr in ['width', 'height']:
                        continue  # Skip deleting width and height attributes from img tags
                    else:
                        del tag[attr]
            except AttributeError:
                continue

            if tag.name not in ['img', 'video'] and not tag.contents:
                tag.decompose()


        article = soup

    try:
        url = "https://" + articleURL.split('/')[2] + "/"
        sanitized_code = article.prettify()

        # change relative links to absolute
        sanitized_code = sanitized_code.replace('src="/',f'src="{url}')
        sanitized_code = sanitized_code.replace('href="/',f'href="{url}')
        return sanitized_code

    except AttributeError:
        return f"""
    <center>
        <h2>Couldn't Fetch</h2>
    </center>
    """
