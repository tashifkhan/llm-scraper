import html2text
import requests
from bs4 import BeautifulSoup

def return_md(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    markdowntext = html2text.html2text(soup.prettify())
    return markdowntext

def return_md2(url):
    res = requests.get("https://r.jina.ai/"+url)
    soup = BeautifulSoup(res.content)
    return soup.prettify()

def write_file(filename, markdowntext):
    with open(filename, "w+") as ft:
        ft.write(markdowntext)
        ft.close()

def main():
    write_file("test2.md", return_md("https://portfolio.tashif.codes/"))
    write_file("test3.md", return_md2("https://portfolio.tashif.codes/"))

if __name__ == "__main__":
    main()

