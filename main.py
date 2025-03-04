import os
import html2text
import requests
from google import genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

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

def prompt_generator(scrapped_content, prompt):
    return (
    f"""
        Website Scapped Content:
        {scrapped_content}

        based on the sceapped content answer the follwing question and provide answers following these guidlines:
            "1. **Extract Information:** Only extract the information that directly matches the provided scarpped content. "
            "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
            "3. **Empty Response:** If no information matches the description, return an empty string ('')."
            "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."

        question: {prompt}

    """)

def llm_prompt_response(prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(response.text)

def main():
    # write_file("test2.md", return_md("https://portfolio.tashif.codes/"))
    # write_file("test3.md", return_awaited_md("https://portfolio.tashif.codes/"))
    llm_prompt_response("Hello what all can you do?")

if __name__ == "__main__":
    main()

