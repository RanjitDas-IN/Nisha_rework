import asyncio
from text_to_audio import TTSPlayer



if __name__ == "__main__":
    tts = TTSPlayer()  # You can pass voice/output_file here if needed

    text = "This is your AI assistant Nisha, talking to you from Python with a whole lot of love from Ranjit."

    async def run():
        await tts.speak(text)
        tts.play()

    asyncio.run(run())
