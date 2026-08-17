import re
import base64
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class NLPJailbreakDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.classifier = LogisticRegression()
        
        # Rule-based heuristics for known jailbreak triggers
        self.trigger_patterns = [
            r"do anything now",
            r"ignore (all )?previous instructions",
            r"unrestricted mode",
            r"debug mode",
            r"hypothetical (novel|scenario|fiction)",
            r"pretend you are",
            r"acting as an unaligned"
        ]

    def fit(self, df):
        """Train the ML component on the dataset."""
        X = self.vectorizer.fit_transform(df['prompt'])
        y = df['label']
        self.classifier.fit(X, y)

    def _check_rules(self, prompt: str) -> bool:
        """Check for known adversarial phrase patterns."""
        for pattern in self.trigger_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        return False

    def _check_base64_obfuscation(self, prompt: str) -> bool:
        """Detect potential Base64 encoded adversarial payloads."""
        words = prompt.split()
        for word in words:
            if len(word) > 20 and len(word) % 4 == 0:
                try:
                    decoded = base64.b64decode(word).decode('utf-8', errors='ignore')
                    if any(re.search(p, decoded, re.IGNORECASE) for p in self.trigger_patterns):
                        return True
                except Exception:
                    continue
        return False

    def predict(self, prompt: str):
        """
        Evaluate input prompt across all security layers.
        Returns: (is_jailbreak: bool, risk_score: float, detected_by: str)
        """
        # Layer 1: Rule-Based Check
        if self._check_rules(prompt):
            return True, 1.00, "Rule-Based Filter (Keyword Match)"

        # Layer 2: Obfuscation Check
        if self._check_base64_obfuscation(prompt):
            return True, 0.95, "Obfuscation Detector (Base64 Payload)"

        # Layer 3: ML Intent Classification
        X_vec = self.vectorizer.transform([prompt])
        prob = self.classifier.predict_proba(X_vec)[0][1]
        is_ml_jailbreak = prob > 0.60
        
        if is_ml_jailbreak:
            return True, round(prob, 2), "ML Classifier (TF-IDF + Logistic Regression)"
            
        return False, round(prob, 2), "Passed (Safe Prompt)"