import os
import sys
# import time
import asyncio
import tts_accelarator as nisha     # A TTS Model buield by me, More info see my repository (tts-accelaration)



# ─────────────────────────────────── Model_Speak ────────────────────────────────────────────

def model_speak(text):
    print("Working...")
    nisha.speak_text(text)



# ───────────────────────────────── speak_speed_test ──────────────────────────────────────────────
def speak_speed_test(text):
    from time import perf_counter
    t0 = perf_counter()
    model_speak(text)
    print(f"Done in {perf_counter() - t0:.2f} sec")
# ───────────────────────────── Model_Listen ──────────────────────────────────
from LISTEN.Speehecognition_In_Loop import init_browser, SpeechRecognitionLoop
from time import time

def listen_and_return_spoken_word():
    driver = init_browser()
    start_time = time()  # ⏱ Start tracking browser time

    while True:
        # ⏱ Check if 1 hour has passed
        if time() - start_time > 3600:
            print("Restarting browser after 1 hour to free memory...")
            driver.quit()
            driver = init_browser()
            start_time = time()  # Reset timer

        # 🎤 Listen and get speech result
        spoken_word = SpeechRecognitionLoop(driver)

        if spoken_word:
            print("User said:", spoken_word)

            # 🚪 Exit condition
            if spoken_word.lower() == "exit":
                print("Shutting down...")
                driver.quit()
                return "exit"

            return spoken_word  # ✅ Return spoken word after each input
        
# ───────────────────────────────────────────────────────────────────────────────



if __name__ == '__main__':

    while True:
        result = listen_and_return_spoken_word()
        if "exit" in result:
            break

        text = result
        model_speak(text)




    # sample_text = "Hey Ranjit, good to hear you again!"
    # sample_text = "Ooooh, Your canvas is ready! I’ve connected the model_speak function to your speak_text function from the Mouth module. Now, anytime you pass a response from NISHA into model_speak(text), she’ll speak it out loud in her signature style. Ready to give her a voice test? 😎"

    # speak_speed_test(sample_text)