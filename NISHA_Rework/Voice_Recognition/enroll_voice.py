import torch
import torchaudio
import numpy as np
from speechbrain.inference import EncoderClassifier  # updated import

# Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": device}
).eval()

def get_embedding(wav_path):
    signal, fs = torchaudio.load(wav_path)
    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)
    if fs != 16000:
        signal = torchaudio.transforms.Resample(fs, 16000)(signal)
    with torch.no_grad():
        embedding = model.encode_batch(signal.to(device))
    return embedding.squeeze().cpu().numpy()

# YOUR voice samples
enroll_paths = ["NISHA_Rework/Voice_Recognition/voice1.wav", "NISHA_Rework/Voice_Recognition/voice2.wav", "NISHA_Rework/Voice_Recognition/voice3.wav","NISHA_Rework/Voice_Recognition/voice4.wav","NISHA_Rework/Voice_Recognition/voice5.wav"]

# Get embeddings
embeddings = [get_embedding(p) for p in enroll_paths]

# Average to get the voice profile
voice_profile = np.mean(embeddings, axis=0)

# Save the profile
np.save("NISHA_Rework/Voice_Recognition/ranjit_profile.npy", voice_profile)
print("Voice profile saved as ranjit_profile.npy")