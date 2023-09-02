import openai 
import streamlit as st
import os
from textblob_text import TextBlob
# import random

# Emotion Grading Function, 등급 나누는 방식 설정
def grade_emotion(sentiment):
    if sentiment >= 0.5:
        return "5[High]"
    elif sentiment >= 0 and sentiment < 0.5:
        return "3[Neutral]"
    else:
        return "1[Low]"
    

# load_dotenv()
st.set_page_config(page_title="Emotion Garbage", page_icon="😡")
st.title("😡 [Emotion Garbage] Chatbot") 
openai_api_key = st.secrets["OPENAI_API_KEY"]

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇 때문에 기분이 좋지 않으신가요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="ft:gpt-3.5-turbo-0613:personal::7uH4MDPG", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)

    blob = TextBlob(prompt)
    sentiment = blob.sentiment.polarity
    emotion_grade = grade_emotion(sentiment)

    st.write(f"Angry Level: {emotion_grade}")
    st.chat_message("assistant").write(msg.content)
