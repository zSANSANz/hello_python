# knn_pipeline.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_auc_score, roc_curve
)
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

# 1) Load dataset (sesuaikan path)
df = pd.read_csv("bank.csv")  # ganti path sesuai data

# 2) Contoh preprocessing sederhana (sesuaikan dengan dataset)
# - ubah target ke 0/1
df['deposit'] = df['deposit'].map({'no': 0, 'yes': 1})

# Pilih fitur numerik + lakukan one-hot pada kategorikal sederhana
X = df.drop(columns=['deposit'])
y = df['deposit']

# Untuk contoh, lakukan one-hot encoding pada kolom kategorikal
X = pd.get_dummies(X, drop_first=True)

# 3) Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4) SMOTE untuk menangani imbalance (opsional)
sm = SMOTE(random_state=42)
X_train_sm, y_train_sm = sm.fit_resample(X_train, y_train)

# 5) Pipeline: scaler + KNN
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# 6) Grid search untuk k dan metric
param_grid = {
    'knn__n_neighbors': [3,5,7,9,11],
    'knn__weights': ['uniform','distance'],
    'knn__p': [1,2]  # p=1 Manhattan, p=2 Euclidean
}

gs = GridSearchCV(pipe, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
gs.fit(X_train_sm, y_train_sm)

print("Best params:", gs.best_params_)
print("Best CV AUC:", gs.best_score_)

# 7) Evaluasi pada test set (ingat: pipeline termasuk scaler)
y_pred = gs.predict(X_test)
y_proba = gs.predict_proba(X_test)[:,1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC:", roc_auc_score(y_test, y_proba))
print("\nClassification report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)

# 8) Plot ROC
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test,y_proba):.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC - KNN")
plt.legend()
plt.show()
