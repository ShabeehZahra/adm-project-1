# -*- coding: utf-8 -*-
"""Untitled34.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P1fexJwB8YOXJD9zC1MUmcaH2jkpigbc
"""

!pip install streamlit
!pip install wordcloud
!pip install pyngrok
!pip install catboost  # if you're using CatBoostClassifier

# app.py
import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from pyngrok import ngrok
from catboost import CatBoostClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix
import nltk
from nltk.corpus import stopwords
import re

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Define text preprocessing and feature engineering functions
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.lower()  # Lowercase
    text = text.split()  # Split into words
    text = [word for word in text if word not in stop_words]  # Remove stopwords
    text = ' '.join(text)
    return text

def feature_engineering(df):
    df['text'] = df['text'].apply(preprocess_text)
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['text'])
    y = df['sentiment']
    return X, y, vectorizer

# Define model training and evaluation functions
def train_model(model_class, X_train, y_train, **kwargs):
    model = model_class(**kwargs)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_train, X_test, y_train, y_test):
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    train_auc = roc_auc_score(y_train, train_preds)
    test_auc = roc_auc_score(y_test, test_preds)
    return train_auc, test_auc

def predict_model(model_class, user_input, X_train, X_test, y_train, y_test, vectorizer, **kwargs):
    model = train_model(model_class, X_train, y_train, **kwargs)
    user_input_transformed = vectorizer.transform([user_input])
    sentiment = model.predict(user_input_transformed)[0]
    result = {
        'Train AUC': evaluate_model(model, X_train, X_test, y_train, y_test)[0],
        'Test AUC': evaluate_model(model, X_train, X_test, y_train, y_test)[1],
        'Confusion Matrix': confusion_matrix(y_test, model.predict(X_test)).tolist()
    }
    return sentiment, result

# Load and preprocess data
def load_data():
    # Replace this with actual data loading code
    data = {'text': ['I love this!', 'This is bad.', 'I am happy.', 'I am sad.'],
            'sentiment': [1, 0, 1, 0]}
    df = pd.DataFrame(data)
    return df

df = load_data()
X, y, vectorizer = feature_engineering(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Streamlit UI
st.title("Sentiment Analysis App")

user_input = st.text_area("Enter text:", "Type your text here...")
Models_toggle = st.sidebar.selectbox('Choose Model', ('Logistic Regression', 'BernoulliNB', 'CatBoostClassifier'))

if Models_toggle == 'Logistic Regression':
    predict_sentiment = st.sidebar.button('Predict Sentiment')
    C = st.slider('C', 0.01, 10.0, 1.0)
    max_iter = st.slider('Max Iterations', 100, 1000, 100)
    n_jobs = st.slider('Number of Jobs', 1, 4, 1)

    if predict_sentiment:
        sentiment, result = predict_model(LogisticRegression, user_input, X_train, X_test, y_train, y_test, vectorizer, C=C, max_iter=max_iter, n_jobs=n_jobs)
        st.metric(label='Sentiment', value=sentiment)
        st.subheader("Model Performance")
        st.write(pd.DataFrame(result))
else:
    pass

if Models_toggle == 'BernoulliNB':
    predict_sentiment = st.sidebar.button('Predict Sentiment')
    alpha = st.slider('Alpha', 0.0, 10.0, 1.0)

    if predict_sentiment:
        sentiment, result = predict_model(BernoulliNB, user_input, X_train, X_test, y_train, y_test, vectorizer, alpha=alpha)
        st.metric(label='Sentiment', value=sentiment)
        st.subheader("Model Performance")
        st.write(pd.DataFrame(result))
else:
    pass

if Models_toggle == 'CatBoostClassifier':
    predict_sentiment = st.sidebar.button('Predict Sentiment')
    n_estimators = st.slider('Number of Estimators', 1, 100, 100)
    max_depth = st.slider('Maximum Depth', 1, 10, 6)

    if predict_sentiment:
        sentiment, result = predict_model(CatBoostClassifier, user_input, X_train, X_test, y_train, y_test, vectorizer, n_estimators=n_estimators, depth=max_depth)
        st.metric(label='Sentiment', value=sentiment)
        st.subheader("Model Performance")
        st.write(pd.DataFrame(result))
else:
    pass

from pyngrok import ngrok

# Set the ngrok authtoken for ngrok v2
ngrok.set_auth_token("2jNfZmktn63X5Sd5PXfYHZs84Iz_rmUq41zpDXLEe1phv1s")

from pyngrok import ngrok
import streamlit as st

# Set the ngrok authtoken (replace 'your_ngrok_v2_authtoken' with your actual ngrok v2 authtoken)
ngrok.set_auth_token('2jNfZmktn63X5Sd5PXfYHZs84Iz_rmUq41zpDXLEe1phv1s')

# Expose Streamlit app with ngrok, specifying the port within 'addr' for HTTPv2 tunnels
public_url = ngrok.connect(addr='8080')  # Change to the correct port if different
st.write(f"**Running Streamlit app:** {public_url}")

# Ensure your Streamlit app code follows here
# Example: st.title("My Streamlit App")
#          st.write("Hello, world!")