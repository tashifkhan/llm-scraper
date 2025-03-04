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
            "5. **Markdown Format:** The Ouput must be a well formated markdown file"

        question: {prompt}

    """)


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def llm_prompt_response(prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

def main():
    scrapped_content = return_awaited_md("https://cropmate.tashif.codes/")
    print(scrapped_content)
    prompt = prompt_generator(scrapped_content, "what is this website all about?")
    print(prompt)
    response = llm_prompt_response(prompt)
    print(response)

if __name__ == "__main__":
    main()

