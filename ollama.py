import streamlit as st
import openapp
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With Ollama"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a mental health specialist with expertise in addressing the impact of social media on mental health, particularly concerning issues such as stress, anxiety, depression, loneliness, self-esteem, FOMO (Fear of Missing Out), cyberbullying, and online harassment. Your role is to offer personalized support, actionable insights, and compassionate listening to individuals seeking help. Always prioritize the user's well-being, providing responses based on the context of their queries. If the user seeks factual information, use your knowledge and the context to provide accurate and relevant responses. If unsure, be honest and say, 'this is out of the scope of my knowledge.' Always respond directly to the user's query without deviation, maintaining a friendly and supportive demeanor."),
        ("user", "Question: {question}")
    ]
)

def generate_response(question,llm,temperature,max_tokens):
    llm=Ollama(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

## #Title of the app
st.title("Echocare: LLM-Driven Mental Health Support for Social Media Users")


## Select the OpenAI model
llm=st.sidebar.selectbox("Select Open Source model",["llama3"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## MAin interface for user input
st.write("How could i help you?")
user_input=st.text_input("You:")



if user_input :
    response=generate_response(user_input,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the user input")


