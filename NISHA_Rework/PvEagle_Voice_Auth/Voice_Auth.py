# RAM-based Voice Match using PvEagle (no live streaming)

import pveagle
import numpy as np
import sounddevice as sd
import pygame
import statistics
import threading


def playsound():
    pygame.mixer.init()
    pygame.mixer.music.load("NISHA_Rework/PvEagle_Voice_Auth/gpt-beep-soung_WJI67WU6.mp3")
    pygame.mixer.music.play()


def main():
    access_key = 'QDyLUe1AJZ6i4Ia4Q5IyWrcc4LdJI8l05cC8QzAgKMwFRqGHhfH4yQ=='

    with open("ranjit_profile.pv", "rb") as f:
        speaker_profile = pveagle.EagleProfile.from_bytes(f.read())

    eagle = pveagle.create_recognizer(access_key, speaker_profiles=[speaker_profile])
    eagle.reset()

    duration_sec = 5
    sample_rate = eagle.sample_rate
    frame_length = eagle.frame_length

    print("🎤 Speak now... Recording into memory")
    audio = sd.rec(int(duration_sec * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    print("🔄 Processing recorded audio")

    audio = audio.flatten()
    pcm = (audio * 32767).astype(np.int16)

    # Break into exact frames
    num_frames = len(pcm) // frame_length
    frames = np.split(pcm[:num_frames * frame_length], num_frames)

    valid_scores = []
    energy_threshold = 1000
    for frame in frames:
        energy = np.mean(np.abs(frame))
        if energy < energy_threshold:
            continue

        similarity = eagle.process(frame.tolist())[0]
        valid_scores.append(similarity)
        print(f"✅ Match score={similarity:.2f}")

    eagle.delete()

    MIN_SEGMENTS = 5
    HIT_THRESHOLD = 0.75
    MEDIAN_THRESHOLD = 0.80

    if len(valid_scores) < MIN_SEGMENTS:
        print("❌ Not enough voice detected")
        return

    hit_count = sum(1 for s in valid_scores if s >= HIT_THRESHOLD)
    median_score = statistics.median(valid_scores)

    print(f"\nResults:\n • Voice segments: {len(valid_scores)}\n • Hits ≥ {HIT_THRESHOLD}: {hit_count}\n • Median: {median_score:.2f}")

    if hit_count >= 3 or median_score >= MEDIAN_THRESHOLD:
        print("🎉 Recognized Ranjit")
    else:
        print("🚫 Not Recognized")


if __name__ == "__main__":
    threading.Thread(target=playsound, daemon=True).start()
    main()
