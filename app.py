import os
import json
import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import re
from typing import Optional, Dict, Union

class RFPExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client for RFP extraction"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"

    def _preprocess_text(self, text: str, max_tokens: int = 4000) -> str:
        """Preprocess and truncate text while preserving context"""
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_tokens]

    def extract_rfp_information(self, text: str) -> Dict[str, Union[str, None]]:
        """Extract structured RFP information using OpenAI"""
        preprocessed_text = self._preprocess_text(text)
        
        rfp_fields = [
            "Bid Number", "Title", "Due Date", "Bid Submission Type", 
            "Term of Bid", "Pre Bid Meeting Details", "Installation Requirements", 
            "Bid Bond Requirement", "Delivery Timeline", "Payment Terms", 
            "Required Documentation", "Manufacturer Registration", 
            "Cooperative Contract Options", "Product Models", 
            "Product Part Numbers", "Product Categories", 
            "Contact Information", "Issuing Organization", 
            "Bid Objective Summary", "Technical Specifications"
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert RFP information extraction assistant."},
                {"role": "user", "content": f"""
                Extract precise, structured information from this RFP document. 
                Required Fields: {', '.join(rfp_fields)}
                
                Extraction Guidelines:
                1. Be extremely specific and precise
                2. Use actual text from document where possible
                3. Infer contextually if direct match isn't found
                4. Provide most relevant information for each field
                
                Document Text:
                {preprocessed_text}
                
                Respond ONLY with a valid, complete JSON object."""}
            ],
            response_format={"type": "json_object"},
            max_tokens=1000,
            temperature=0.1
        )
        
        return json.loads(response.choices[0].message.content)

def read_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_html(uploaded_file):
    soup = BeautifulSoup(uploaded_file.getvalue(), 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def read_txt(uploaded_file):
    return uploaded_file.getvalue().decode('utf-8')

def main():
    st.set_page_config(page_title="RFP Extractor", page_icon="📄")
    
    st.title("🔍 RFP Information Extraction")
    st.markdown("Extract comprehensive information from RFP documents.")
    
    # API Key Input (optional)
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Upload RFP Document", 
        type=['pdf', 'html']
    )
    
    # Additional extraction options
    show_raw_text = st.sidebar.checkbox("Show Raw Document Text")
    
    if st.button("Extract RFP Information") and uploaded_file:
        try:
            # Read file based on type
            if uploaded_file.type == 'application/pdf':
                text = read_pdf(uploaded_file)
            elif uploaded_file.type == 'text/html':
                text = read_html(uploaded_file)
            elif uploaded_file.type == 'text/plain':
                text = read_txt(uploaded_file)
            else:
                st.error("Unsupported file type")
                return
            
            # Optional: Display raw text
            if show_raw_text:
                st.subheader("Raw Document Text")
                st.text(text)
            
            # Initialize extractor
            extractor = RFPExtractor(api_key=api_key)
            
            # Extract information
            with st.spinner('Extracting RFP Information...'):
                rfp_info = extractor.extract_rfp_information(text)
            
            # Display results
            st.subheader("Extracted RFP Information")
            st.json(rfp_info)
            
            # Download option
            st.download_button(
                label="Download Extracted JSON",
                data=json.dumps(rfp_info, indent=2),
                file_name="rfp_extraction_results.json",
                mime="application/json"
            )
        
        except Exception as e:
            st.error(f"Extraction Error: {e}")

    # Usage instructions
    st.sidebar.header("How to Use")
    st.sidebar.markdown("""
    1. Upload PDF or HTML document.
    2. Enter OpenAI API Key on the sidebar.
    3. Click "Extract RFP Information".
    4. Review extracted data.
    5. Download JSON if needed
    """)

if __name__ == "__main__":
    main()