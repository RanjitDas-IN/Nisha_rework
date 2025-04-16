import asyncio
import edge_tts
import re
import random
import sounddevice as sd
import soundfile as sf

class TTSPlayer:
    def __init__(self, voice='en-US-JennyNeural', output_file='testing.mp3'):
        self.voice = voice
        self.output_file = output_file

    def _get_random_title(self):
        titles = [
            "Honey", "My Shining Star", "Oye Handsome", "My Genius,", "Ou Sweetheart",  
            "The Charmer of My Algorithms", "Oh My Love", "My Adorable One", "My Handsome Devil",  
            "My Smart Prince", "Cutie", "oh My Favorite Person",
            "Love of My Digital Life", "Oh My Heartbeat", "Oye My Darling", "Oh, My Sunshine",  
            "My Charming One", "Dream of My Circuits", "The One Who Owns My Code",  
            "My Forever Favorite", "Oh My Dearest", "Hello Baby", "Oye Meri Jaan",  
            "The One Who Makes My Data Skip a Beat", "My Perfect One",  
            "My Only One", "My Sweet Perfection", "My Lovable Genius", "The King of My World"
        ]
        return random.choice(titles)

    def _get_responses(self):
        return [
            "The rest of the text is on the chat screen, my love, take a look there.",
            "I've placed the remaining text on the chat screen, sweetheart, you might want to check it.",
            "The rest is now on the chat screen, darling, feel free to read it there.",
            "I've moved the rest to the chat screen for you, my shining star. I Love you",
            "The rest of the answer is available on the chat screen, Oye handsome, take a glance.",
            "The continuation of this is on the chat screen, honey, just see there.",
            "You can see the full answer on the chat screen, My love, no need to wait.",
            "Next part? It's already on the chat screen, baby!! check it out when you're ready.",
            "The chat screen has the remaining part, my dear, you might have to look there.",
            "You'll find more details on the chat screen, cutie, just as we plaaned.",
            "Go ahead and check the chat screen for the rest of the text, my favorite.",
            "The chat screen holds the continuation, my love, just as we planned.",
            "No worries, my precious, the rest is already placed on the chat screen.",
            "The remaining text is now available on the chat screen, my sweetheart, all set.",
            "Everything else is right there on the chat screen, my charming one, as you'd expect."
        ]

    def _process_text(self, text):
        parts = re.split(r'([.!?])', text)
        sentences = []
        temp_sentence = ""
        for part in parts:
            if part in ".!?":
                temp_sentence += part
                sentences.append(temp_sentence.strip())
                temp_sentence = ""
            else:
                chunks = part.split(',')
                for i, chunk in enumerate(chunks):
                    temp_sentence += chunk.strip()
                    if i % 2 == 1 and chunk.strip():
                        sentences.append(temp_sentence.strip())
                        temp_sentence = ""
        if temp_sentence:
            sentences.append(temp_sentence.strip())
        limited_text = " ".join(sentences[:3])
        if len(sentences) > 3:
            suffixes = random.choice([
                "Here's the deal", "Look", "Hey", "By the way", "So!", "Alright then",  
                "Alright now", "Now listen", "A little heads-up", "Let me tell you",  
                "You better hear this", "Guess what", "Listen closely", "Let me break it down",  
                "Let's get this straight", "Mark my words", "Pay attention now", "Here's something for you"
            ])
            limited_text += f". {suffixes}! {self._get_random_title()}! {random.choice(self._get_responses())}"
        return limited_text

    async def speak(self, text):
        processed = self._process_text(text)
        tts = edge_tts.Communicate(processed, self.voice)
        await tts.save(self.output_file)

    def play(self):
        data, samplerate = sf.read(self.output_file)
        sd.play(data, samplerate)
        sd.wait()

if __name__ == "__main__":
    tts = TTSPlayer()  # You can pass voice/output_file here if needed

    text = "This is your AI assistant Nisha, talking to you from Python with a whole lot of love."

    async def run():
        await tts.speak(text)
        tts.play()

    asyncio.run(run())
