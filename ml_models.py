from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

class PretrainedModels:
    def __init__(self):
        self.vulnerability_model = joblib.load('pretrained_vulnerability_model.joblib')
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()

    def predict_vulnerability(self, features):
        return self.vulnerability_model.predict_proba(features)[:, 1]

    def detect_anomalies(self, features):
        scaled_features = self.scaler.fit_transform(features)
        return self.anomaly_detector.fit_predict(scaled_features)

def prepare_features(features_df):
    # Convert categorical features to one-hot encoding
    features_encoded = pd.get_dummies(features_df)
    
    # Normalize numerical features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_encoded)
    
    return features_scaled

def train_xgboost_model(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_pred)
    print(f"Model AUC score: {auc_score}")
    
    return model, scaler
