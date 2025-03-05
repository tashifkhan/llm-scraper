import streamlit as st
import os
import re

from scrapy import (
    return_awaited_md,
    prompt_generator,
    llm_prompt_response
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4527A0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #5E35B1;
        margin-bottom: 1rem;
    }
    .success-text {
        color: #1DB954;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #6200EA;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .nav-item {
        padding: 0.5rem 1rem;
        text-align: center;
        cursor: pointer;
        border-radius: 8px;
    }
    .nav-active {
        background-color: #6200EA;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def clean_markdown_response(response):
    """Clean markdown code blocks and format the response properly."""
    if response.startswith("```") and "```" in response[3:]:
        first_line_end = response.find('\n')
        if first_line_end > 3:
            language = response[3:first_line_end].strip()
            if language == "markdown" or language == "md":
                response = response[first_line_end + 1:]
            else:
                response = response[first_line_end + 1:]
        else:
            response = response[3:]
        
        last_block = response.rfind("```")
        if last_block != -1:
            response = response[:last_block].strip()
    
    return response

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Web Scraper"

st.markdown("<h1 class='main-header'>LLM-powered Assistant</h1>", unsafe_allow_html=True)

if st.session_state.current_page == "Web Scraper":
    st.markdown("<h2 class='subheader'>Web Scraper</h2>", unsafe_allow_html=True)

    st.markdown("""
    This tool helps you scrape and analyze web content using AI. Simply enter a URL,
    describe what you're looking for, and get structured results!
    """)

    st.markdown("<h3 class='subheader'>Step 1: Enter Website URL</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("Website URL", placeholder="https://tashif.codes", key="scraper_url")
    with col2:
        scrape_button = st.button("🔍 Scrape", use_container_width=True, key="btn_scrape_site")

    if scrape_button:
        if url:
            with st.spinner(" Scraping website content..."):
                try:
                    cleaned_content = return_awaited_md(url)
                    st.session_state.dom_content = cleaned_content

                    with st.expander("Preview Extracted Website Content"):
                        st.text_area("HTML Content", cleaned_content, height=300)
                    st.success("✅ Website scraped successfully!")

                except Exception as e:
                    st.error(f"Failed to scrape the website: {str(e)}")
        else:
            st.warning("⚠️ Please enter a valid URL")

    if "dom_content" in st.session_state:
        st.markdown("<h3 class='subheader'>Step 2: Extract Information</h3>", unsafe_allow_html=True)
        st.markdown("Describe what information you want to extract from the website:")

        parse_description = st.text_area(
            "Extraction instructions",
            placeholder="Example: Extract all product names and prices from this e-commerce page",
            height=100,
            key="scraper_instructions"
        )

        if st.button("Extract Information", use_container_width=True, key="btn_extract"):
            if parse_description:
                with st.spinner("Analyzing the content..."):
                    try:
                        prompt = prompt_generator(st.session_state.dom_content, parse_description)
                        response = llm_prompt_response(prompt)
                        
                        cleaned_response = clean_markdown_response(response)
                        
                        st.markdown("<h3 class='subheader'>Results</h3>", unsafe_allow_html=True)
                        
                        with st.container():
                            st.divider()
                            st.markdown(cleaned_response)
                            st.divider()

                        st.download_button(
                            "Download Results",
                            cleaned_response,
                            file_name="extraction_results.md",
                            mime="text/plain",
                            key="download_scraper_results"
                        )
                    except Exception as e:
                        st.error(f"Error during content extraction: {str(e)}")
            else:
                st.warning("⚠️ Please describe what information you want to extract")