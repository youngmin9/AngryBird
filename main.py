import openai 
import streamlit as st
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Emotion Grading Function, 등급 나누는 방식 설정
def grade_emotion(sentiment):
    # if sentiment >= 0.7:
    #     return "5[매우 높은 분노 수준]"
    # elif sentiment >= 0.5:
    #     return "4[높은 분노 수준]"
    # elif sentiment >= 0.3:
    #     return "3[중간 분노 수준]"
    # elif sentiment >= 0.1:
    #     return "2[낮은 분노 수준]"
    # else:
    #     return "1[매우 낮은 분노 수준]"
    
   if sentiment >= 0.5:
       return "5[High]"
   elif sentiment >= 0 and sentiment < 0.5:
       return "3[Neutral]"
   else:
       return "1[Low]"


# Initialize VADER Sentiment Analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Streamlit configuration
st.set_page_config(page_title="angrychat", page_icon="😡")
st.title("😡 [감정 쓰레기통] Angry Chat") 
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

    # VADER Sentiment Analyzer를 사용하여 감정 분석
    sentiment_scores = sia.polarity_scores(prompt)
    compound_score = sentiment_scores['compound']
    pos_score =sentiment_scores['pos']
    neg_score = sentiment_scores['neg']
    neu_score = sentiment_scores['neu']

    emotion_grade = grade_emotion(compound_score)

    st.write(f"Angry Level: {emotion_grade}")
    st.write(f"긍정 지수: {pos_score}")
    st.write(f"중립 지수: {neu_score}")
    st.write(f"부정 지수: {neg_score}")
    st.write(f"종합 분노 점수: {compound_score}")
    st.chat_message("assistant").write(msg.content)

# import openai 
# import streamlit as st
# import os
# from textblob_text import TextBlob
# # import random

# # Emotion Grading Function, 등급 나누는 방식 설정
# def grade_emotion(sentiment):
#     if sentiment >= 0.5:
#         return "5[High]"
#     elif sentiment >= 0 and sentiment < 0.5:
#         return "3[Neutral]"
#     else:
#         return "1[Low]"
    

# # load_dotenv()
# st.set_page_config(page_title="angrychat", page_icon="😡")
# st.title("😡 [Emotion Garbage] 앵그리챗") 
# openai_api_key = st.secrets["OPENAI_API_KEY"]

# # with st.sidebar:
# #     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
# #     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
# #     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
# #     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "무엇 때문에 기분이 좋지 않으신가요?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     openai.api_key = openai_api_key
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = openai.ChatCompletion.create(model="ft:gpt-3.5-turbo-0613:personal::7uH4MDPG", messages=st.session_state.messages)
#     msg = response.choices[0].message
#     st.session_state.messages.append(msg)

#     blob = TextBlob(prompt)
#     sentiment = blob.sentiment.polarity
#     emotion_grade = grade_emotion(sentiment)

#     st.write(f"Angry Level: {emotion_grade}")
#     st.chat_message("assistant").write(msg.content)
