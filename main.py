import openai 
import streamlit as st
import os
from dotenv import load_dotenv
from textblob_text import TextBlob
import random

# Emotion Grading Function, 등급 나누는 방식 설정
def grade_emotion(sentiment):
    if sentiment >= 0.5:
        return "High"
    elif sentiment >= 0 and sentiment < 0.5:
        return "Medium"
    else:
        return "Low"
    

load_dotenv()
st.set_page_config(page_title="Emotion Analysis Chatbot", page_icon="😡")
st.title("💬 Chatbot") 
openai_api_key = os.getenv('OPENAI_API_KEY')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)

    blob = TextBlob(prompt)
    sentiment = blob.sentiment.polarity
    emotion_grade = grade_emotion(sentiment)

    st.write(f"Angry Level: {emotion_grade}")
    st.chat_message("assistant").write(msg.content)
