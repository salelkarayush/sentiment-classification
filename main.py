import re
import joblib
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel 

# Initialize the FastAPI App
app = FastAPI(
    title="E-commerce Sentiment Analysis API",
    description="Classifies product reviews as Positive, Neutral, or Negative.",
    version="1.0.0"
)

# Load the trained Model and Vectorizer
try:
    model = joblib.load('models/sentiment_model.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
except FileNotFoundError:
    raise RuntimeError("Model files not found. Please run train_model.py first.")

# Define Request and Response Schemas
class ReviewRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence_score: float

# Text cleaning function (must match the training pipeline)
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'•\s*', '', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: ReviewRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")

    cleaned_text = clean_text(request.text)
    text_vectorized = vectorizer.transform([cleaned_text])
    
    prediction = model.predict(text_vectorized)[0]
    
    # Extract confidence score
    probabilities = model.predict_proba(text_vectorized)[0]
    confidence = max(probabilities)
    
    return SentimentResponse(
        sentiment=prediction,
        confidence_score=round(float(confidence), 4)
    )

@app.get("/")
def health_check():
    return {"status": "API is up and running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)