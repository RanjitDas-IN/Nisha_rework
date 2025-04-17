from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time

Link = r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/LISTEN/Nisha_voice.html"

chrome_options = Options()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument("--headless=new")
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_experimental_option("detach", True)

# ✅ Initialize and return browser (only once)
def init_browser():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("file://" + Link)
    return driver

# ✅ Use existing browser to recognize one spoken sentence
def SpeechRecognitionLoop(driver):
    try:
        driver.find_element(by=By.ID, value="start").click()
        print("Listening...")

        while True:
            try:
                Text = driver.find_element(by=By.ID, value="output").text
                if Text:
                    driver.find_element(by=By.ID, value="end").click()
                    spoken_word = Text.strip()
                    return spoken_word
                sleep(0.5)
            except Exception:
                sleep(1)
    except Exception as e:
        print("Speech recognition failed:", e)
        return None
