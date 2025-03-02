import html2text
import requests
from bs4 import BeautifulSoup
import os

res = requests.get("https://pypi.org/project/beautifulsoup4/")
soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.prettify())
markdowntext = html2text.html2text(soup.prettify())
# print(markdowntext)

with open("./test.md", "w+") as mdfl:
    mdfl.write(markdowntext)
    mdfl.close()

res2 = requests.get("https://r.jina.ai/"+"https://pypi.org/project/beautifulsoup4/")
# print(res2.content)
soup2 = BeautifulSoup(res2.content)
print(soup2.prettify())
with open("./test2.md", "w+") as mdfl2:
    mdfl2.write(soup2.prettify())
    mdfl2.close()

