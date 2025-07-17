import streamlit as st
from dotenv import load_dotenv
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY ")

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
def generate_response(question,llm, temperature, max_tokens):
    llm = ChatOpenAI(model=llm, api_key = api_key)
    ouput_parser = StrOutputParser()
    chain = prompt | llm | ouput_parser
    answer = chain.invoke({"question": question})
    return answer

# setting up the UI
st.title("Q&A Chatbot With OpenAI")
st.sidebar.title("Settings")

#drop down to select models
llm = st.sidebar.selectbox("Select an Open AI model", ["gpt-4-o", "gpt-4-turbo", "gpt-4"])

#response parametes
temperature = st.sidebar.slider("Tempearture", min_value = 0.0, max_value = 1.0, value = 0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value = 20, max_value = 100, value = 50)


##main interface for user input
st.write("Go ahead and ask any question:")
user_input = st.text_input("You:")
if user_input:
    response = generate_response(user_input, llm, temperature, max_tokens)
    st.write(response)

else:
    st.write("Please provide the question.")