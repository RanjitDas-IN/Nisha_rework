import torch
import torchaudio
import numpy as np
from scipy.spatial.distance import cosine
from speechbrain.inference import EncoderClassifier
from time import perf_counter
t0 = perf_counter()
# Preload model and setup
device = torch.device("cpu")
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": device},
    savedir="pretrained_model_cache"
).to(device).eval()

# Pre-create resampler to avoid re-instantiation
resampler_48k = torchaudio.transforms.Resample(orig_freq=48000, new_freq=16000)
resampler_44k = torchaudio.transforms.Resample(orig_freq=44100, new_freq=16000)
resampler_others = lambda fs: torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)

# Convert audio to required format & extract embedding
def get_embedding(wav_path):
    signal, fs = torchaudio.load(wav_path)

    # Mono downmix
    if signal.shape[0] > 1:
        signal = torch.mean(signal, dim=0, keepdim=True)

    # Use pre-created resamplers for common rates
    if fs == 48000:
        signal = resampler_48k(signal)
    elif fs == 44100:
        signal = resampler_44k(signal)
    elif fs != 16000:
        signal = resampler_others(fs)(signal)

    with torch.no_grad():
        emb = model.encode_batch(signal.to(device)).squeeze()
    return emb.cpu().numpy()

# Core comparison
def is_match(test_wav, profile_path="NISHA_Rework/Voice_Recognition/ranjit_profile.npy", threshold=0.25):
    emb = get_embedding(test_wav)
    profile = np.load(profile_path)
    score = 1 - cosine(emb, profile)
    return score >= threshold, score

# Only run if directly executed
if __name__ == "__main__":

    test_wav = "NISHA_Rework/Voice_Recognition/Main_voice6.wav"
    print("Verifying voice, please wait...")
    match, similarity = is_match(test_wav)
    print(f" Match: {match}, Accuracy: {similarity:.4f}")
print(f"Done in {perf_counter() - t0:.2f} sec")
