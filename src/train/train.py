"""Anti-Detect Model Training"""
import os
import json
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data(filepath='data.json'):
    """Load training data"""
    full_path = os.path.join(BASE_DIR, filepath)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_features(data):
    """Extract features from data"""
    features = []
    labels = []
    
    for item in data:
        features.append([
            item['response_length'],
            item['status_code'],
            int('captcha' in item['content'].lower()),
            int('blocked' in item['content'].lower()),
            int('robot' in item['content'].lower()),
            int('denied' in item['content'].lower()),
            int('security' in item['content'].lower()),
            int('please wait' in item['content'].lower())
        ])
        labels.append(item['is_anti_crawl'])
    
    return np.array(features), np.array(labels)


def train_model():
    """Train anti-detect model"""
    print("Loading data...")
    data = load_data()
    
    print("Extracting features...")
    X, y = extract_features(data)
    
    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    print("Saving model...")
    models_dir = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    with open(os.path.join(models_dir, 'anti_detect_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    print("Training complete!")


if __name__ == '__main__':
    train_model()