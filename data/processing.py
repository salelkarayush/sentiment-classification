import pandas as pd
import re
# List of your scraped files
files = ["data/raw/clothing_reviews.csv", "data/raw/guitar_bag.csv", "data/raw/headphones.csv", "data/raw/phone_reviews.csv", "data/raw/negative_phone.csv", "data/raw/shoes.csv"]

# Read and concatenate all files
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs, ignore_index=True)

print(f"Total rows scraped: {len(df)}")

# Drop rows where 'Review Text' or 'Review Rating' is missing
df = df.dropna(subset=['Review Text', 'Review Rating'])

print(f"Total rows after removing empty reviews: {len(df)}")


def clean_flipkart_text(text):
    # 1. Convert to lowercase
    text = str(text).lower()
    
    # 2. Remove bullet points
    text = re.sub(r'•\s*', '', text) 
    
    # 3. Remove punctuation, special characters, and emojis (Keep only letters and numbers)
    text = re.sub(r'[^a-z0-9\s]', '', text) 
    
    # 4. Remove extra spaces created by deleting characters
    text = re.sub(r'\s+', ' ', text).strip() 
    
    # 5. Remove the "more" artifact left over from truncated reviews
    # We use regex word boundaries (\b) so we don't accidentally remove "more" from "I want more"
    text = re.sub(r'\bmore\b$', '', text).strip()
    
    return text

# Apply the function to create a new column
df['Clean_Text'] = df['Review Text'].apply(clean_flipkart_text)

def map_sentiment(rating):
    rating = float(rating)
    
    if rating >= 4.0:
        return 'Positive' # 4 and 5 stars
    elif rating == 3.0:
        return 'Neutral'  # 3 stars
    else:
        return 'Negative' # 1 and 2 stars

# Create the target variable column
df['Sentiment'] = df['Review Rating'].apply(map_sentiment)

# Check class distribution
print(df['Sentiment'].value_counts())

# Save the dataset for the training script
df.to_csv("data/cleaned/cleaned_reviews.csv", index=False)