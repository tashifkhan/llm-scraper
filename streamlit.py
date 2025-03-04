import streamlit as st

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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LLM based Web Scraper</h1>", unsafe_allow_html=True)

st.markdown("""
This tool helps you scrape and analyze web content using AI. Simply enter a URL,
describe what you're looking for, and get structured results!
""")


st.markdown("<h2 class='subheader'>Step 1: Enter Website URL</h2>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    url = st.text_input("Website URL", placeholder="https://example.com")
with col2:
    scrape_button = st.button("🔍 Scrape", use_container_width=True)


if scrape_button:
    if url:
        with st.spinner("🕸️ Scraping website content..."):
            try:
                cleaned_content = return_awaited_md(url)
                st.session_state.dom_content = cleaned_content
                st.success("✅ Website scraped successfully!")

                with st.expander("View Raw DOM Content"):
                    st.text_area("", cleaned_content, height=300)
            except Exception as e:
                st.error(f"Failed to scrape the website: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid URL")


if "dom_content" in st.session_state:
    st.markdown("<h2 class='subheader'>Step 2: Extract Information</h2>", unsafe_allow_html=True)
    st.markdown("Describe what information you want to extract from the website:")

    parse_description = st.text_area(
        "Extraction instructions",
        placeholder="Example: Extract all product names and prices from this e-commerce page",
        height=100
    )

    if st.button("Extract Information", use_container_width=True):
        if parse_description:
            with st.spinner("analyzing the content..."):
                try:
                    prompt = prompt_generator(st.session_state.dom_content, parse_description)
                    response = llm_prompt_response(prompt)

                    st.markdown("<h2 class='subheader'>Results</h2>", unsafe_allow_html=True)
                    st.markdown(response)

                    st.download_button(
                        "📥 Download Results",
                        response,
                        file_name="extraction_results.md",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error during content extraction: {str(e)}")
        else:
            st.warning("⚠️ Please describe what information you want to extract")

