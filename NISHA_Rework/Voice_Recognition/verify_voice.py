import torch
import torchaudio
import numpy as np
from scipy.spatial.distance import cosine
from speechbrain.inference import EncoderClassifier

# Setup
print("Device is Setting Up")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Model selecting...\tIt may takes time because of CPU")
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": device}
).eval()

def get_embedding(wav_path):
    print("getting the embeddings...")
    signal, fs = torchaudio.load(wav_path)
    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)
    if fs != 16000:
        signal = torchaudio.transforms.Resample(fs, 16000)(signal)
    with torch.no_grad():
        embedding = model.encode_batch(signal.to(device))
    return embedding.squeeze().cpu().numpy()

def is_match(test_wav, profile_path="NISHA_Rework/Voice_Recognition/ranjit_profile.npy", threshold=0.25):
    print("Matching the embeddings...")
    emb = get_embedding(test_wav)
    profile = np.load(profile_path)
    score = 1 - cosine(emb, profile)
    return score >= threshold, score

# Test your new voice
test_wav = "NISHA_Rework/Voice_Recognition/Main_voice6.wav"  # your input
print("Happening, Please wait...")
match, sim = is_match(test_wav)

print(f"Match={match}, Similarity={sim:.3f}")