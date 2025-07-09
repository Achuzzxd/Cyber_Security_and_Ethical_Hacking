from feature_extraction import extract_features
import pandas as pd
import joblib

model = joblib.load('models/phishing_detector_model.pkl')

def predict_urls(urls):
    feature_list = [extract_features(url) for url in urls]
    new_X = pd.DataFrame(feature_list)
    new_X = new_X[model.feature_names_in_]
    predictions = model.predict(new_X)
    label_map = {0: 'Phishing', 1: 'Legitimate'}
    return [(url, label_map[pred]) for url, pred in zip(urls, predictions)]

