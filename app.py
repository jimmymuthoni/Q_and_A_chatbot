import streamlit as st
from dotenv import load_dotenv
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
load_dotenv()

#setting langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "Q&A Chatbot with OPENAI"


#prompts
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please provide reponse to the user queries"),
        ("user", "Question:{question}")
    ]
)


#function to generate response
def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    ouput_parser = StrOutputParser()
    chain = prompt | llm | ouput_parser
    answer = chain.invoke({"question": question})
    return answer
