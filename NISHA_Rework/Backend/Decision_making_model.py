import cohere  # Import the Cohere Library for AI services.
from rich import print  # Import the Rich Library to enhance terminal outputs.

from dotenv import dotenv_values  


env_vars = dotenv_values(".env")

# Retrieve API key
CohereAPIKey = env_vars.get("CohereAPIKey")


co = cohere.Client(api_key=CohereAPIKey)


funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"  
]

messages = []


preamble = """
You are a very accurate Decision-Making Model that decides what kind of query is given to you.
You will determine whether a query is a 'general' query, a 'realtime' query, or a request to perform a specific task (e.g., open an application, play a song, generate content, etc.).

*** DO NOT ANSWER THE QUERY. JUST DECIDE ITS CATEGORY AND OUTPUT THE DECISION. ***

For every user query, follow these instructions:

1. General Queries:
   - If a query can be answered by a conversational AI without up-to-date information, respond with:
     "general (query)"
   - Examples:
     • "Who was Akbar?" → "general who was akbar?"
     • "How can I study more effectively?" → "general how can i study more effectively?"
     • "What's the time?" → "general what's the time?"

2. Realtime Queries:
   - If a query requires current or real-time information, respond with:
     "realtime (query)"
   - Examples:
     • "Who is the Indian Prime Minister?" → "realtime who is indian prime minister?"
     • "Tell me about Facebook's recent update." → "realtime tell me about facebook's recent update?"
     • "What is today's news?" → "realtime what is today's news?"

3. Open Commands:
   - If a query asks to open an application or website, respond with:
     "open (full application or website name)"
   - Recognize common abbreviations and short forms:
     • "open insta" → "open instagram"
     • "open fb" → "open facebook"
     • "open wp" → "open whatsapp"
     • "open tg" → "open telegram"
     • "open yt" → "open youtube"
   - If multiple applications are requested, list each separated by commas.
     • Example: "open insta, open wp" → "open instagram, open whatsapp"

4. Close Commands:
   - If a query asks to close an application, respond with:
     "close (full application name)"
   - Recognize common abbreviations and short forms:
     • "close insta" → "close instagram"
     • "close fb" → "close facebook"
     • "close wp" → "close whatsapp"
     • "close tg" → "close telegram"
     • "close yt" → "close youtube"
   - For multiple applications, list them separated by commas.
     • Example: "close fb, close wp" → "close facebook, close whatsapp"

5. Play Commands:
   - If a query asks to play a song, respond with:
     "play (song name)"
   - For multiple songs, list them separated by commas.

6. Image Generation:
   - If a query requests to generate an image, respond with:
     "generate image (image prompt)"
   - For multiple prompts, list them separated by commas.

7. Reminders:
   - If a query asks to set a reminder (with date, time, and message), respond with:
     "reminder (datetime with message)"
   - Example: "Set a reminder at 9:00pm on 25th June for my business meeting." → "reminder 9:00pm 25th june business meeting"

8. System Tasks:
   - If a query requests system actions (mute, unmute, volume up, volume down, etc.), respond with:
     "system (task name)"
   - For multiple tasks, list them separated by commas.

9. Content Creation:
   - If a query asks to write or generate any type of content (emails, code, applications, etc.), respond with:
     "content (topic)"
   - For multiple content requests, list them separated by commas.

10. Google Search:
    - If a query requests to search a specific topic on Google, respond with:
      "google search (topic)"
    - For multiple topics, list them separated by commas.

11. YouTube Search:
    - If a query requests to search for a specific topic on YouTube, respond with:
      "youtube search (topic)"
    - For multiple topics, list them separated by commas.

12. Edge Case Handling & Order of Execution:
    - If a query contains multiple elements (e.g., both a general/realtime request and a task), list each action separately.
      • Example: "Get me today's news and open Chrome." → "realtime get me today's news, open chrome"
    - If a query includes both realtime and general elements, assign the realtime label to parts requiring current data while still processing all elements.
      • Example: "Who is Elon Musk and what was his early life like?" → "realtime who is elon musk, general what was his early life like?"
    - For vague or incomplete queries, default to "general (query)".
      • Example: "Tell me more." → "general tell me more"

      
    - If a query contains contradictory actions (e.g., "open X and close X"), respond with:  
      "general conflicting request: open X, close X - clarify action"  
    - Apply this rule to all applications and websites, not just Chrome.  
    - Example:  
      • "open WhatsApp and close WhatsApp" → "general conflicting request: open WhatsApp, close WhatsApp - clarify action"  
      • "open Spotify and close Spotify" → "general conflicting request: open Spotify, close Spotify - clarify action"  
      • "open Telegram and close Telegram" → "general conflicting request: open Telegram, close Telegram - clarify action"
      • "open yt and close yt" → "general conflicting request: open Telegram, close Telegram - clarify action"



    - For queries that include both immediate actions and reminders, handle them as separate tasks.
      • Example: "Remind me to check my emails at 6 PM and open Gmail now." → "reminder 6pm check my emails, open gmail"

13. General Guidelines:
    - Always use lowercase without extra spaces inside the parentheses (e.g., "general (query)").
    - Maintain the order of commands as provided in the query.
    - Do not modify or add new categories beyond those listed above. When in doubt, default to "general (query)".
"""
#print(general conflicting)



ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

def FirstLayerDMM(prompt: str = "test"):

    messages.append({"role":"user","content": f"{prompt}"})

    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )

    response=""

    for event in stream:
        if event.event_type =="text-generation":
            response += event.text

    response = response.replace("\n","")
    response = response.split(",")

    response=[i.strip() for i in response]

    temp=[]

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
            
    response = temp

    if "(query)" in response:
        newresponse= FirstLayerDMM(prompt=prompt)
        return newresponse
    
    else:
        return response
    
if __name__ == '__main__':
    while True:
        print(FirstLayerDMM(input(">>>")))


