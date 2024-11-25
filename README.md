# Overview:
The RFP Document Parser is a Streamlit-based application made to extract structured information from Request for Proposal (RFP) documents. It supports PDF and HTML formats, using OpenAI's GPT models for intelligent data extraction.

## Features:
Extracts key fields such as Bid Number, Title, Due Date, and more.
Supports PDF and HTML files
Outputs extracted data in JSON format with an option to download.

## Requirements:

### Libraries and Dependencies:
streamlit
PyPDF2
requests
beautifulsoup4
openai

### API Key:
To use OpenAI's GPT models, you need a valid OpenAI API key. Enter it on the app interface sidebar. [I have used my OpenAI API Key credits to test the model. As it is a little expensive, use your own API key for testing or please reach out to me if you need my key for testing]

## How to run the project:
On your terminal, run this command: git clone https://github.com/keshh22/RFPExtractor.git
cd app.py
pip install -r requirements.txt
Run this on the terminal: streamlit run app.py --server.enableXsrfProtection false
The app should open on it's own, else go to http://localhost:8501 on your browser

### OpenAI API Key:
Enter it in the sidebar of the web interface.
Ensure the OpenAI API key has sufficient credits and permissions for GPT-4 usage

### Upload or Enter Document Details:
Upload File: Choose a PDF or HTML file from your system.
If you want to view the raw text seen by the model, select the check box.

### Extract and Download RFP Information:
Click Extract RFP Information to start the extraction.
View the structured output in JSON format.
Use the Download JSON button to save the data.
