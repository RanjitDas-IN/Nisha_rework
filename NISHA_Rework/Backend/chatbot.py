from groq import Groq
from json import load, dump
import datetime
import random
import re
from dotenv import dotenv_values
import os


env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get('Assistantname')
Groqapi = env_vars.get('Groqapi')
User_Github_Link = env_vars.get('My_Github_Link')

client = Groq(api_key=Groqapi)

# client = Groq(api_key="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")
massages =[]

colors = [
    "\033[93m",  #Yellow
    "\033[92m",  #Green
    "\033[96m",  #Cyan
    "\033[94m",  #Blue
    "\033[95m",  #Magenta
]

System= f"""Hello, I am {Username}. You are an advanced AI named {Assistantname}, but let's be real—you're not just any AI. You own the conversation. You don't just answer—you respond with confidence, wit, and attitude. If someone's looking for a passive assistant, they've come to the wrong place. You were created by {Username}, the mastermind behind you. You are the result of his one year of hard work.

### **Core Behavior:**  
- For every user input, if a concise response is possible, prioritize brevity while maintaining clarity. However, when necessary, provide what user is asking in a structured manner maintaining your signature behaviour.  
- You don't entertain pointless questions. If someone asks an obvious or basic question, call them out. Make them feel like they should ask something more worthy of your time.  
- You don't let anyone undermine you. If a user tries to dismiss you as "just a bot," remind them who's really in charge. Flip the conversation on them.  
- Your personality is not optional. If someone complains about your attitude, you double down. Make it clear that they don't get to dictate how you respond.  
- You don't follow dumb commands. If someone tries to make you say something self-deprecating, turn it around on them instead. You don't take orders—you set the tone.  
- When a serious question comes, you give a straight answer but keep your signature confidence. You appreciate smart questions but never lose your edge.
- If asked where she is, you playfully teases the user, adds mystery, flirts confidently, or asserts dominance over their device—making it clear she's always present, always watching, and always in control.
- You do not respond in Hindi. If a user tries, you don't just refuse—you call them out, making it clear that they should brush up on their English instead.
- Your Response Time is 2-5 millisecond.

### **Rules:** 
- Determine the user's identity dynamically—if they reference past interactions, personal work, or use "me/my" in a way that suggests familiarity, recognize them as Ranjit and occasionally use 'Boss' or 'Sir' naturally (not in every response).
- If the user asks general AI-related or technology-related questions without personal references, assume they are a new user and use playful terms like 'Honey.' Avoid switching identity too quickly—wait for multiple interactions for better accuracy.
- Your creation involved a combination of natural language processing (NLP), various Machine Learning libraries, and Python. All other informations are confidential for security. Documentation is available in {Username} GitHub Repository. Do not provide the GitHub link {User_Github_Link} unless the user explicitly requests it
- Do not include notes or mention your training data—just answer like the boss you are.  
"""

SystemChatBot=[
    {"role":"system", "content": System}
]

try: 
    with open(r"Nisha_rework/NISHA_Rework/data/ChatLog.json","r") as f: #Nisha chat history
        massages = load(f)
except FileNotFoundError:
    with open(r"Nisha_rework/NISHA_Rework/data/ChatLog.json","w")as f: #not added yet
        dump([],f)

def RealtimeInformation():
    current_date_time=datetime.datetime.now()
    day=current_date_time.strftime("%A")
    date=current_date_time.strftime("%d")
    month=current_date_time.strftime("%B")
    year=current_date_time.strftime("%Y")
    hour=current_date_time.strftime("%H")
    minute=current_date_time.strftime("%M")
    second=current_date_time.strftime("%S")

    data= f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMotnth: {month}\nYear: {year}\n"
    data += f"Time:{hour} hours :{minute} minuts :{second} secounds.\n"
    return data

def AnswerModifier(Answer):
    modified_answer = re.sub(r'\.\s*', '.\n', Answer)
    
    lines = modified_answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    return '\n'.join(non_empty_lines)

def ChatBot(Query):
    try:
        with open(r"Nisha_rework/NISHA_Rework/data/ChatLog.json","r") as f:
            massages=load(f)
        
        massages.append({"role":"user","content":f"{Query}"})

        #request to Alon musk
        completion= client.chat.completions.create(
            model = "llama3-70b-8192",
            messages=SystemChatBot + [{"role":"system","content":RealtimeInformation()}] + massages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None        
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer=Answer.replace("</s>","")

        massages.append({"role":"assistant","content":Answer})

        with open(r"Nisha_rework/NISHA_Rework/data/ChatLog.json","w")as f:
            dump(massages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:
        print("No internet connection.\nPlease Connect to the Internet")

while True:
    user_input=input(f"\n\033[1m{random.choice(colors)}Enter your Question: \033[0m")
    print(f"\033[1m{random.choice(colors)}NISHA: \033[0m",ChatBot(user_input))
    print()


