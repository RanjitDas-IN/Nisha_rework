import pveagle
import soundfile

def get_next_enroll_audio_data(wav_path, num_samples):
    # Read the WAV file
    pcm_data, sample_rate = soundfile.read(wav_path, dtype='int16')
    
    if pcm_data.ndim > 1:
        pcm_data = pcm_data[:, 0]  # take first channel if stereo

    if len(pcm_data) < num_samples:
        raise ValueError(f"Audio file {wav_path} is too short. Required: {num_samples} samples.")

    return pcm_data[:num_samples].tolist(), 100.0  # already complete recording

def main():
    access_key = 'QDyLUe1AJZ6i4Ia4Q5IyWrcc4LdJI8l05cC8QzAgKMwFRqGHhfH4yQ=='   # <<< Put your Picovoice AccessKey here

    # 1. Create profiler
    eagle_profiler = pveagle.create_profiler(access_key)

    # 2. Enroll using three recordings
    profiles = []
    for wav_path in ["NISHA_Rework/Voice_Recognition/voice1.wav"]:
        print(f"Enrolling from {wav_path}...")
        percentage = 0.0
        while percentage < 100.0:
            pcm, percentage = get_next_enroll_audio_data(wav_path, eagle_profiler.min_enroll_samples)
            percentage, feedback = eagle_profiler.enroll(pcm)
            print(f"Progress: {percentage:.1f}% — Feedback: {feedback.name}")

        # Export profile from each file
        profiles.append(eagle_profiler.export())

    # 3. Use the first profile (or merge if needed)
    final_profile = profiles[0]

    # 4. Save profile to disk
    with open("ranjit_profile2.pv", "wb") as f:
        f.write(final_profile.to_bytes())
    print("Enrollment complete! Profile saved as 'ranjit_profile2.pv'.")

    # 5. Cleanup
    eagle_profiler.delete()

if __name__ == "__main__":
    main()