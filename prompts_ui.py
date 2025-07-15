from dotenv import load_dotenv
import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint

from langchain_core.prompts import PromptTemplate
import json
import os

# Load environment variables (for HuggingFace token)
load_dotenv()

# Set your Hugging Face API token from environment variable
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ✅ Create the LLM
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=hf_token,
)

# ✅ Streamlit UI
st.header('📚 Research Paper Summarizer')

paper_input = st.selectbox(
    "Select Research Paper Name",
    ["Select...", "Attention Is All You Need",
     "BERT: Pre-training of Deep Bidirectional Transformers",
     "GPT-3: Language Models are Few-Shot Learners",
     "Diffusion Models Beat GANs on Image Synthesis"]
)

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1–2 paragraphs)", "Medium (3–5 paragraphs)", "Long (detailed explanation)"]
)

# ✅ Load Prompt Template Manually (since load_prompt doesn't work with file paths)
def load_prompt_from_file(filename):
    with open(filename, 'r') as f:
        template_dict = json.load(f)
    return PromptTemplate(**template_dict)

# Load template.json
template = load_prompt_from_file('template.json')

# ✅ Run the chain
if st.button('Summarize'):
    chain = template | llm
    result = chain.invoke({
        'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input
    })
    st.subheader("📄 Summary Output:")
    st.write(result)
