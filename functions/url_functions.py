import urllib.request

from bs4 import BeautifulSoup
from googlesearch import search


def read_text_from_url(url: str) -> str:
    """
    Returns the text content at a url.

    PARAMETERS DESCRIPTION:
    url -> The url of the webpage to read
    """

    uf = urllib.request.urlopen(url)
    html = uf.read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style", "nav"]):
        script.extract()    # rip it out

    for class_name in ["header", "footer", "navbar", "sidebar"]:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            element.extract()

    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

def online_search(query: str) -> str:
    """
    Returns a list of urls from an online search powered by google given a query.

    PARAMETERS DESCRIPTION:
    query -> The query to search online
    """

    urls = ""
    for j in search(query, num=10, stop=10, pause=2):
        urls += f"{j}\n"
    return urls