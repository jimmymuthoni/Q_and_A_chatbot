from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

#setting langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "Q&A Chatbot with Ollama"


## prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

#function to generate response
def generate_response(question,llm, engine,temperature, max_tokens):
    llm = Ollama(model=engine)
    ouput_parser = StrOutputParser()
    chain = prompt | llm | ouput_parser
    answer = chain.invoke({"question": question})
    return answer

# setting up the UI
st.title("Q&A Chatbot With Ollama")
st.sidebar.title("Settings")

#response parametes
temperature = st.sidebar.slider("Tempearture", min_value = 0.0, max_value = 1.0, value = 0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value = 20, max_value = 100, value = 50)


##main interface for user input
st.write("Go ahead and ask any question:")
user_input = st.text_input("You:")
if user_input:
    response = generate_response(user_input, engine=engine, temperature, max_tokens)
    st.write(response)

else:
    st.write("Please provide the question.")

