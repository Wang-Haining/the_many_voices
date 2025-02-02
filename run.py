"""
This module reproduces the findings of our paper, *The Many Voices of Du Ying:
Revisiting the Disputed Writings of Lu Xun and Zhou Zuoren*. Specifically, it outputs
the validation accuracy, predictions of authorship for the four disputed essays
between Lu Xun and Zhou Zuoren, feature weights, and the relative frequency per
thousand characters for each author.
"""

__author__ = "hw56@indiana.edu"
__version__ = "0.1.0"
__license__ = "0BSD"

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from utils import load_corpus, count_frequency, highlight_document

print("*" * 99)
print(
    "Reproducing the findings of The Many Voices of Du Ying: Revisiting the Disputed "
    "Writings of Lu Xun and Zhou Zuoren"
)

# load data
train, val, test = load_corpus()
# specify 31 features derived from recursive feature elimination
# including 4 bigrams and 27 unigrams
# fmt: off
character_ngrams = ['诚', '于', '乃', '光', '原', '各', '必', '惟', '不', '随', '本',
                    '全', '但', '徒', '别', '是', '为', '何',  '多', '夫', '则', '之',
                    '焉', '皆', '而', '矣', '及', '自然', '进而', '足以', '于是']
# fmt: on

# feature stats
total_len = sum([d["text_length"] for d in train])
lx_freq_per_thousand = [
    (f / total_len) * 1000
    for f in count_frequency(
        character_ngrams, "".join([d["text"] for d in train if d["author"] == "lx"])
    )
]
zzr_freq_per_thousand = [
    (f / total_len) * 1000
    for f in count_frequency(
        character_ngrams, "".join([d["text"] for d in train if d["author"] == "zzr"])
    )
]

# get relative frequencies for character_ngrams
X_train = [
    [count / length for count in count_frequency(character_ngrams, text)]
    for text, length in [(d["text"], d["text_length"]) for d in train]
]
X_val = [
    [count / length for count in count_frequency(character_ngrams, text)]
    for text, length in [(d["text"], d["text_length"]) for d in val]
]
X_test = [
    [count / length for count in count_frequency(character_ngrams, text)]
    for text, length in [(d["text"], d["text_length"]) for d in test]
]

# get labels, lx -> 1, zzr -> 0
y_train = [d["label"] for d in train]
y_val = [d["label"] for d in val]

# a standard l2-norm logistic regression
clf = LogisticRegression(
    penalty="l2", C=1.0, solver="lbfgs", tol=1e-9, max_iter=int(1e9)
)

# machine learning pipeline
pipline = Pipeline([("scaler", StandardScaler()), ("classifier", clf)])
# training
pipline.fit(X_train, y_train)

# validation
print(
    f"The validation accuracy is "
    f"{round(accuracy_score(y_val, pipline.predict(X_val)), 3)}.\n"
)

# prediction
for prediction, title in zip(pipline.predict_proba(X_test), [d["title"] for d in test]):
    predicted_author = "zzr" if (prediction[0] > prediction[1]) else "lx"
    prob = round(max(prediction), 3)
    print(
        f"{title} is predicted to have been written by {predicted_author} with a "
        f"probability of {prob}."
    )
print("\n")

# coefs
l2_coef = np.hstack(
    (
        pipline.named_steps["classifier"].intercept_.reshape(1, -1),
        pipline.named_steps["classifier"].coef_,
    )
)
summary_df = pd.DataFrame(
    {
        "feature": ["1"] + character_ngrams,
        "weight": l2_coef.tolist()[0],
        "lx_freq_per_thousand": ["-"] + lx_freq_per_thousand,
        "zzr_freq_per_thousand": ["-"] + zzr_freq_per_thousand,
    }
)

# sort feature importance separately by absolute value
positive_weights_df = summary_df[summary_df["weight"] > 0]
negative_weights_df = summary_df[summary_df["weight"] < 0]
positive_weights_df = positive_weights_df.sort_values("weight", ascending=False)
negative_weights_df = negative_weights_df.sort_values(
    "weight", key=abs, ascending=False
)
sorted_summary_df = pd.concat(
    [positive_weights_df, negative_weights_df], ignore_index=True
)

print(
    "The feature weights and relative frequencies per thousand characters for each "
    "author are summarized below. Positive weights support Lu Xun, while negative ones"
    "support Zhou Zuoren. The importance of these weights is proportional to their "
    "absolute value. Note that '1' represents the intercept."
)
print(sorted_summary_df)

# visualization
weights = pipline.named_steps["classifier"].coef_.tolist()[0]
for d in test:
    highlight_document(d["text"], character_ngrams, weights, d["title"])
print("Visualization has been saved to the 'visualization' directory.")
print("*" * 99)
