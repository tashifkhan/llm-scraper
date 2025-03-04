import streamlit as st

from scrapy import (
    return_awaited_md,
    prompt_generator,
    llm_prompt_response
)

st.title("LLM based WebScraper")
url = st.text_input("Enter Website URL")

if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        cleaned_content = return_awaited_md(url)
        st.session_state.dom_content = cleaned_content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")
            prompt = prompt_generator(st.session_state.dom_content, parse_description)
            response = llm_prompt_response(prompt)
            st.write(response)