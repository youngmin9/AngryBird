#완전하진 않으나, 형태의 공유가 필요할 듯 해서 우선 업로드할게요

import streamlit as st
from textblob import TextBlob
import random

# Emotion Grading Function, 등급 나누는 방식 설정
def grade_emotion(sentiment):
    if sentiment >= 0.5:
        return "High"
    elif sentiment >= 0 and sentiment < 0.5:
        return "Medium"
    else:
        return "Low"

# Empathetic Chatbot Function
def get_empathetic_response(user_message):
    blob = TextBlob(user_message)
    sentiment = blob.sentiment.polarity

    # Positive Responses
    positive_responses = [
        "That sounds wonderful! Can you tell me more about it?",
        "I'm glad to hear that! What made you feel this way?",
        "Awesome! What's making you feel so good?"
    ]

    # Neutral Responses
    neutral_responses = [
        "I see. Is there another topic you'd like to discuss?",
        "Got it. How about we talk about something else?",
        "Could you elaborate a bit more on that?",
        "If you're feeling down, feel free to unload your thoughts here!"
    ]

    # Negative Responses
    negative_responses = [
        "I'm sorry to hear that. What's been bothering you?",
        "It sounds tough. Would you like to share more?",
        "I'm here to listen. What's been on your mind?",
        "I understand it's challenging. Talking about it might help.",
        "I'm sorry to hear that you're feeling this way...",
        "If you're comfortable, could you tell me more about what's bothering you?",
        "It's okay to feel this way. I'm here to listen and support.",
        "I'm here for you. Let's talk about what's on your mind."
    ]

    # Selecting Response Based on Sentiment
    if sentiment > 0.3:
        return random.choice(positive_responses)
    elif sentiment < 0.3:
        return random.choice(negative_responses)
    else:
        return random.choice(neutral_responses)


# Streamlit App
def main():
    st.set_page_config(page_title="Emotion Analysis Chatbot", page_icon="😡")
    st.title("Emotion Analysis Chatbot")

    # User Input
    user_message = st.text_input("Enter your message:")
    
    # Emotion Analysis
    if user_message:
        blob = TextBlob(user_message)
        sentiment = blob.sentiment.polarity
        emotion_grade = grade_emotion(sentiment)
        
        st.write(f"Angry Level: {emotion_grade}")

        # Empathetic Chatbot Response
        bot_response = get_empathetic_response(user_message)
        st.text("Chatbot: " + bot_response)

if __name__ == "__main__":
    main()
