import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.multiclass import OneVsRestClassifier


np.random.seed(42)

# 200 samples, 128 features
X = np.random.randn(200, 128)

# 3 classes (0, 1, 2)
y = np.random.choice([0, 1, 2], size=200)


df = pd.DataFrame(X, columns=[f'Feature_{i+1}' for i in range(128)])
df['Target'] = y


X = df.drop('Target', axis=1)
y = df['Target']

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# pipeline with OneVsRestClassifier
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', OneVsRestClassifier(LogisticRegression(max_iter=1000)))
])

# 5. Train pipeline
pipe.fit(X_train, y_train)

# 6. Predict
y_pred = pipe.predict(X_test)

# 128-dimensional == PCA
pca = PCA(n_components=2)
X_test_2d = pca.fit_transform(X_test)

# 8. Create DataFrame for visualization
df_vis = pd.DataFrame(X_test_2d, columns=["PCA1", "PCA2"])
df_vis['Predicted'] = y_pred


plt.figure(figsize=(10, 6))
sns.scatterplot(
    x="PCA1", y="PCA2",
    hue="Predicted",
    palette="Set2",
    data=df_vis,
    s=100,
    edgecolor="k"
)
plt.title("128D Feature Vectors (Face/Voice) - Pipeline Predictions (after PCA)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="Predicted Class")
plt.grid(True)

# Save and open the image

# plt.savefig("pipeline_prediction.png")
# webbrowser.open("pipeline_prediction.png")