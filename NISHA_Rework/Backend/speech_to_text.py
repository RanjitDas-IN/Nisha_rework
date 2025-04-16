#!/usr/bin/env python3
import os
import time
from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ─── Load environment ───────────────────────────────────────────────────────────
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")  # default to en-US

# ─── Prepare HTML ───────────────────────────────────────────────────────────────
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            }};

            recognition.onend = function() {{
                recognition.start();
            }};

            recognition.start();
        }}

        function stopRecognition() {{
            if (recognition) {{
                recognition.stop();
            }}
            output.textContent = "";
        }}
    </script>
</body>
</html>'''

# Write out voice.html
cwd = os.getcwd()
data_dir = os.path.join(cwd, "data")
os.makedirs(data_dir, exist_ok=True)
html_file_path = os.path.join(data_dir, "/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/data/voice.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# File URL for Chrome
VOICE_URL = f"file://{html_file_path}"

# ─── Helper Functions ───────────────────────────────────────────────────────────
def SetAssistantStatus(status: str):
    """Write status to a file so your assistant can read it."""
    status_dir = os.path.join(cwd, "Nisha_rework", "NISHA_Rework", "Frontend", "Files")
    os.makedirs(status_dir, exist_ok=True)
    with open(os.path.join(status_dir, "Status.data"), "w", encoding="utf-8") as f:
        f.write(status)

def QueryModifier(text: str) -> str:
    """Capitalize and punctuate."""
    txt = text.strip()
    words = txt.split()
    question_words = {"who","what","where","when","why","how","which","whose","whom"}
    last = txt[-1]
    if words[0].lower() in question_words:
        if last not in ".?!": txt += "?"
        else: txt = txt[:-1] + "?"
    else:
        if last not in ".?!": txt += "."
        else: txt = txt[:-1] + "."
    return txt.capitalize()

def UniversalTranslator(text: str) -> str:
    """Translate to English if needed."""
    from googletrans import Translator
    translator = Translator()
    en = translator.translate(text, src="auto", dest="en").text
    return en.capitalize()

# ─── Start Selenium ────────────────────────────────────────────────────────────
chrome_opts = Options()
# chrome_opts.add_argument("--headless=new")  # if you ever want headless
chrome_opts.add_argument("--use-fake-ui-for-media-stream")
chrome_opts.add_argument("--use-fake-device-for-media-stream")
chrome_opts.add_argument("--no-sandbox")
chrome_opts.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_opts)

def init_recognition_page():
    """Load the local page and click START."""
    driver.get(VOICE_URL)
    start_btn = driver.find_element(By.ID, "start")
    start_btn.click()

def listen_once() -> str:
    """Grab whatever text is in the <p id="output">, stop recog, and return it."""
    output_el = driver.find_element(By.ID, "output")
    text = output_el.text.strip()
    if not text:
        return ""
    # stop recognition so the page resets
    driver.find_element(By.ID, "end").click()

    # Translate if needed
    if "en" in InputLanguage.lower():
        return QueryModifier(text)
    else:
        SetAssistantStatus("Translating...")
        return QueryModifier(UniversalTranslator(text))

# ─── Main Loop ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_recognition_page()
    print(f"🟢 Listening in `{InputLanguage}`... (CTRL+C to quit)")

    try:
        while True:
            try:
                result = listen_once()
                if result:
                    print(result)
                    # restart recognition immediately
                    driver.find_element(By.ID, "start").click()
                else:
                    # no text yet, wait a bit
                    time.sleep(0.1)
            except Exception:
                # Something went wrong—refresh and restart
                driver.refresh()
                time.sleep(1)
                init_recognition_page()
    except KeyboardInterrupt:
        print("\n🛑 Exiting…")
    finally:
        driver.quit()
