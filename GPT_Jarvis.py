import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()

def record_text():

    while(True):
        try:
            with sr.Microphone() as source2:
                
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                print("say something...")
                
                audio2 = r.listen(source2)
                
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
    
                return MyText
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

def send_to_GPT(messages , model="gpt-3.5-turbo"):

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return messages

# messages = []

while(True):
    text = record_text()
    if "exit" in text or "fuck off" in text or "quit" in text:
        print(f"User: " ,text)
        print("JARVIS: okay..okay....geez")
        break
    
    print(f"User: " ,text)
    messages = [{"role":"user", "content": text}]
    response = send_to_GPT(messages)
    print("JARVIS: " + response[1].content)
    SpeakText(response[1].content)