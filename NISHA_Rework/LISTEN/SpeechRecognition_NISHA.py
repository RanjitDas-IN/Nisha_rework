from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time

# Local HTML file path
Link = r"C:\Users\ranji\OneDrive\Desktop\NISHA_Rework\LISTEN\Nisha_voice.html"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument("--headless=new")
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")


chrome_options.add_experimental_option("detach", True)


def start_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(Link)
    return driver



driver = start_driver()
start_time = time()  # Track script uptime



def SpeechRecognitionModel():
    try:
        driver.find_element(by=By.ID, value="start").click()
        print("Listening...")

        while True:
            try:
                Text = driver.find_element(by=By.ID, value="output").text
                if Text:
                    driver.find_element(by=By.ID, value="end").click()
                    return Text

                sleep(0.5)

            except Exception as e:
                # print(f"Error in retrieving speech: {e}")
                sleep(1)  # Small wait before retrying

    except Exception as e:
        # print(f"Error in SpeechRecognitionModel: {e}")
        return None



if __name__=='__main__':
    # Main loop with error handling
    while True:
        try:
            # Restart browser every 60 minutes (memory cleanup)
            if time() - start_time > 3600:  
                print("Restarting Chrome to free up memory...")
                driver.quit()
                driver = start_driver()
                start_time = time()  # Reset timer

            # Get speech recognition text
            text = SpeechRecognitionModel()

            if text:
                print("Recognized:", text, "\n")

                # Exit condition
                if text.lower() == "exit" :
                    print("Exiting speech recognition.")
                    break

            # Restart if script fails
        except Exception as e:
            driver.quit()
            driver = start_driver()
            start_time = time()  # Reset timer
        

