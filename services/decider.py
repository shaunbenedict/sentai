import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq = Groq(api_key=os.getenv("Groq_APIKEY"))

def modelname(names, msg):
    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are supposed to decide who should be responding next from the list of names: " + names},
            {"role": "user", "content": msg}
        ],
        max_tokens=500,
        temperature=1,
    )
    content = response.choices[0].message.content or ""
    return content

def concluder(msg):
    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are supposed to decide if the conversation have come to a conclusion or not. If yes, add 'CONCLUDE' and the summary of the conversation."},
            {"role": "user", "content": msg}
        ],
        max_tokens=500,
        temperature=1,
    )
    content = response.choices[0].message.content or ""
    return content