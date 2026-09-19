from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate,load_prompt
import os

load_dotenv()

# Initialize the Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Streamlit UI
st.header('Analysis Tool')

paper_input = st.selectbox("Select Papaer Name", ["Polity", "Geography", "Economy", "Science & Technology"])
analysis_type = st.selectbox("Select Analysis Type", ["Year Wise","Topic Wise","Topic Wise Year Trend"])

# Load the prompt template
template_path = os.path.join(os.path.dirname(__file__), '_3_0_template.json')
template = load_prompt(template_path)

# When the user clicks the "Analyze" button, invoke the chain with the provided inputs
if st.button('Analyze'):
    chain = template | model
    result = chain.invoke(
        {
            'paper_input' : paper_input,
            'analysis_type' : analysis_type
        }
    )
    st.write(result.content)
