import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def train_sentiment_model(csv_path):
    df = pd.read_csv(csv_path)
    
    # Ensure no empty values snuck through
    df = df.dropna(subset=['Clean_Text', 'Sentiment'])

    #Splitting Data (80% Train, 20% Test)...
    # Stratify ensures our minority classes (Neutral/Negative) are distributed evenly
    X_train, X_test, y_train, y_test = train_test_split(
        df['Clean_Text'], 
        df['Sentiment'], 
        test_size=0.2, 
        random_state=42, 
        stratify=df['Sentiment']
    )

    #Vecorizing text with TF-IDF
    vectorizer = TfidfVectorizer(max_features=1500, ngram_range=(1, 2))
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test) # Transform only for test data!

    # class_weight='balanced' for handling the e-commerce data imbalance
    model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=500)
    model.fit(X_train_vec, y_train)

    #Model Evaluation:
    y_pred = model.predict(X_test_vec)
    
    # The classification report prints Precision, Recall, and F1-Score for each class
    print(classification_report(y_test, y_pred))

    # Saving Model Artifacts for API...
    joblib.dump(model, 'models/sentiment_model.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    print("Saved 'sentiment_model.pkl' and 'tfidf_vectorizer.pkl'")

if __name__ == "__main__":
    train_sentiment_model("data/cleaned/cleaned_reviews.csv")