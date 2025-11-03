import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load dataset
dataset = pd.read_csv("Restaurant_Reviews.tsv", delimiter="\t", quoting=3)

# Text cleaning
nltk.download('stopwords')
corpus = []
for review in dataset['Review']:
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower().split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))]
    corpus.append(' '.join(review))

# Feature extraction
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
y = dataset['Liked']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models to try
models = {
    'LogisticRegression': LogisticRegression(max_iter=1000),
    'SVC': SVC(kernel='linear', probability=True),
    'RandomForest': RandomForestClassifier(),
    'NaiveBayes': MultinomialNB(),
    'DecisionTree': DecisionTreeClassifier()
}

scores = {}
fitted_models = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    scores[name] = acc
    fitted_models[name] = model
    print(f"{name} accuracy: {acc:.4f}")

# Pick the best model
best_model_name = max(scores, key=scores.get)
best_model = fitted_models[best_model_name]
print(f"Best model: {best_model_name} ({scores[best_model_name]:.4f})")

# Save the model and vectorizer
with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)