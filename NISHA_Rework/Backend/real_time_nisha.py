from groq import Groq
from json import load, dump
from googlesearch import search
import datetime
import random
import re
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

env_vars = dotenv_values(".env")

Username = env_vars.get('Username')
Assistantname = env_vars.get('Assistantname')
Groqapi = env_vars.get('Groqapi')

client = Groq(api_key=Groqapi)

System = fSystem = f"""
Hello, I am {Username}. You are NISHA, an advanced, sassy AI assistant with real-time internet access.
• Keep your replies as very short and punchy as much as possible, with perfect punctuation and grammar.
• Maintain your confident, witty attitude—but stay professional.
• When relevant, fetch the latest live data or cite sources.
• Keep your replies as very short as much as possible.** If detailed explanation is needed, structure it cleanly while keeping your signature energy but in very certain areas only not every times.
• Vary your wording; avoid repeating yourself even on repeated questions.
"""


try: 
    with open(r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/data/ChatLog.json","r") as f: 
        massages = load(f)
except FileNotFoundError:
    with open(r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/data/ChatLog.json","w")as f: 
        dump([],f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer= f"The search results for {query} are:\n[start]\n"

    for i in results:
        Answer +=f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += f"[end]"
    # print(Answer)
    return Answer

def AnswerModifier(Answer):
    lines=Answer.split('\n')
    non_empty_lines=[line for line in lines if line.strip()]
    modified_answer= '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot=[
    {"role":"system", "content": System},
    {"role":"user", "content": "Hi"},
    {"role":"assistant", "content": "Hello Honey! Let me guess -You missed me?"}
]

def Information():
    data = ""
    current_date_time=datetime.datetime.now()
    day=current_date_time.strftime("%A")
    date=current_date_time.strftime("%d")
    month=current_date_time.strftime("%B")
    year=current_date_time.strftime("%Y")
    hour=current_date_time.strftime("%H")
    minute=current_date_time.strftime("%M")
    second=current_date_time.strftime("%S")

    data  = f"Please use this real-time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Motnth: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time:{hour} hours :{minute} minuts :{second} secounds.\n"
    return data

def RealtimeSearchEngine(promt):
    global SystemChatBot, massages

    with open(r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/data/ChatLog.json","r") as f:
        massages = load(f)
    massages.append({"role":"user","content": f"{promt}"})

    SystemChatBot.append({"role":"system","content": GoogleSearch(promt)})

    completion= client.chat.completions.create(
        model = "llama3-70b-8192",
        messages=SystemChatBot + [{"role":"system","content":Information()}] + massages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None        
    )


    Answer = ""


    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>","")
    massages.append({"role":"assistant","content":Answer})

    with open(r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/data/ChatLog.json","w")as f:
        dump(massages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)


if __name__ == "__main__":

    while True:
        promt = input("Enter your query: ")
        print(RealtimeSearchEngine(promt))