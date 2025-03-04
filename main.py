import html2text
import requests
from bs4 import BeautifulSoup

def return_md(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    markdowntext = html2text.html2text(soup.body.prettify())
    return markdowntext

def return_awaited_md(url):
    res = requests.get("https://r.jina.ai/"+url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup.prettify()

def write_file(filename, markdowntext):
    with open(filename, "w+") as ft:
        ft.write(markdowntext)
        ft.close()

def main():
    write_file("test2.md", return_md("https://portfolio.tashif.codes/"))
    write_file("test3.md", return_awaited_md("https://portfolio.tashif.codes/"))

if __name__ == "__main__":
    main()

