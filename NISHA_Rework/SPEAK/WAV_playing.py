import asyncio
import edge_tts
import sounddevice as sd
import soundfile as sf
from time import perf_counter
t0 = perf_counter()


voices = [ 'en-US-AvaMultilingualNeural']
text = (
       """Elara traced the faded constellation on Liam’s forearm with a gentle finger. They lay tangled in the tall grass of the Brahmaputra riverbank, the Guwahati sun painting the sky in hues of mango and rose. The air hummed with the drone of unseen insects and the distant calls of river birds.

They had met by accident, a spilled cup of chai at a bustling market stall. Elara, a weaver with hands that knew the language of silk, and Liam, a visiting botanist captivated by the region’s vibrant flora. Their initial awkwardness had blossomed into stolen glances, shared cups of sweet lassi, and whispered conversations under the shade of ancient banyan trees.

Liam had only intended to stay for a season, documenting rare orchids. Elara had always known the rhythm of her village, the comforting predictability of the loom and the river. Yet, in each other’s eyes, they found a landscape more compelling than any they had known before.

He would tell her about the intricate veins of a newly discovered leaf, his voice filled with a quiet wonder that mirrored her own fascination with the unfolding patterns of her threads. She would describe the subtle shifts in the river’s current, the way the light danced on its surface, her words weaving tapestries as vibrant as her creations.

Their love was a quiet rebellion against the unspoken boundaries of their different worlds. His temporary stay, her rooted life – these were obstacles they chose to ignore in the intoxicating present. Each shared sunset felt like an eternity, each touch a promise whispered on the humid breeze.

One evening, as the first stars began to prick the darkening sky, Liam took her hand. His gaze was earnest, his voice low. “Elara,” he began, the familiar name a melody on his tongue.

She stilled, her heart a frantic drum against her ribs. She knew this moment was coming, the inevitable edge of his departure drawing closer.

But instead of farewell, he said, “I’ve found a rare species of Vanda near the Kaziranga. It only blooms in this specific microclimate. My research… it will take longer than I anticipated.”

A slow smile spread across Elara’s face, mirroring the soft glow of the fireflies beginning their nightly dance. He hadn’t said forever, hadn’t promised a life unburdened by distance and difference. But in the lengthening of his stay, in the unspoken commitment to the land that held them both, they found a fragile, precious hope.

They lay back in the grass, the vastness of the Indian sky a silent witness to their quiet joy. The river flowed on, carrying its secrets to the sea, and for now, under the watchful gaze of the stars, the lovers had found a little more time. Their story, like the intricate patterns Elara wove, was still unfolding, thread by delicate thread."""
    )
    
sample_text = "Ooooh, Your canvas is ready! I’ve connected the model_speak function to your speak_text function from the Mouth module. Now, anytime you pass a response from NISHA into model_speak(text), she’ll speak it out loud in her signature style. Ready to give her a voice test? 😎"


voice = voices[0]
output_file = "test_results.mp3"

async def amain():
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
    loop.run_until_complete(amain())
    # pass
finally:
    loop.close()

print(f"Done in {perf_counter() - t0:.2f} sec")

def play_audio():
    data, samplerate = sf.read(output_file)

    # Play the audio
    sd.play(data, samplerate)
    sd.wait()  # Wait until playback finishes
play_audio()