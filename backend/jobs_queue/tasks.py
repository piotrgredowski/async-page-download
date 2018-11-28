import urllib.request

from bs4 import BeautifulSoup


def get_page(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove CSS & JS
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()

    # Break into lines and remove trailing whitespace
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip()
              for line in lines
              for phrase in line.split("  "))
    # Remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
