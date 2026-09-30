import numpy as np
from sklearn.linear_model import LogisticRegression

# Small synthetic training set for a portfolio prototype.
# Features: email findings, phone findings, breach findings.
X = np.array([
    [0,0,0],[0,1,1],[1,0,1],[1,1,1],[2,0,2],[1,2,2],
    [2,1,3],[2,2,3],[3,1,4],[3,2,4],[4,2,4],[4,3,4]
])
y = np.array([0,0,0,0,0,0,1,1,1,1,1,1])
MODEL = LogisticRegression().fit(X, y)

def privacy_score(email_findings, phone_findings, breach_findings):
    penalty = email_findings*6 + phone_findings*5 + breach_findings*7
    return max(0, min(100, 100 - penalty))

def predict_risk(email_findings, phone_findings, breach_findings):
    Xv = np.array([[email_findings, phone_findings, breach_findings]])
    probability = float(MODEL.predict_proba(Xv)[0][1])
    label = "HIGH" if probability >= .65 else "MEDIUM" if probability >= .35 else "LOW"
    return {"risk": label, "probability": round(probability, 3)}
