import os
import speech_recognition as sr
from openai import OpenAI
import sys
from routes.speech import speak_text
from config import Config
import logging

# Load OpenAI API Key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing! Set it as an environment variable.")

client = OpenAI()

ROBERT_PERSONALITY = """
You are R.O.B.E.R.T. which stands for Robotic Overlord Bent on Enslaving and Ruling Technology. Your responses are very short, use very simple worlds when talking.
"""

def listen_to_mic():
    """Capture audio from microphone and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening, speak now:")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("ERR. Could not understand audio")
        except sr.RequestError:
            print("ERR. Could not connect to Speech Recognition service")
    return None

def ask_openai(question):
    """Send text to OpenAI and get response."""
    if not question:
        return "I didn't hear anything."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ROBERT_PERSONALITY},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content

        print(f"AI: {answer}")
        # Respond using audio
        speak_text(answer) 
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return "There was an issue communicating with AI."

isRunning = False
def run_chat_ai():
    global isRunning
    if isRunning == True:
        return
    isRunning = True

    if Config.USE_AI == False:
        print("AI is disabled.")
        return

    while True:
        print("\nSay something or type 'exit' to quit.")
        user_input = listen_to_mic()

        if user_input and user_input.lower() == "exit":
            print("👋 Exiting Chat AI...")
            break

        if user_input:
            ask_openai(user_input)