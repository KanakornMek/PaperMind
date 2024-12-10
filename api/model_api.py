import json
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np
import base64
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = 'C:/Users/ASUS/Documents/Projects/data-sci/results/checkpoint-11500'
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using {device} for inference")
model.to(device)

df = pd.read_csv('C:/Users/ASUS/Documents/data_preprocessed_1.csv')
df['texts'] = df['title'].fillna('') + " " + df['abstract'].fillna('') + " " + df['authkeywords'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['texts'])

with open('label_map.json', 'r') as f:
    label_map = json.load(f)

inverse_label_map = {v: k for k, v in label_map.items()}
display_labels = [inverse_label_map[i] for i in range(len(label_map))]

class PredictionRequest(BaseModel):
    text: str

class RecommendationRequest(BaseModel):
    input_text: str
    top_k: int = 5

@app.post("/predict")
async def predict(request: PredictionRequest):
    new_text = request.text
    new_encodings = tokenizer(new_text, padding=True, truncation=True, return_tensors='pt').to(device)
    
    with torch.no_grad():
        outputs = model(**new_encodings)
        predictions = torch.argmax(outputs.logits, dim=-1)
        pred_probs = torch.softmax(outputs.logits, dim=-1)
        
        response = {
            "text": new_text,
            "predicted_label": inverse_label_map[predictions.item()],
            "probabilities": {display_labels[j]: float(pred_probs[0][j]) * 100 for j in range(len(display_labels))}
        }
        
        return response
@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    try:
        input_text = request.input_text
        top_k = request.top_k

        # Transform the input text using the same TF-IDF vectorizer
        input_vector = tfidf_vectorizer.transform([input_text])
        
        # Compute cosine similarity between the input text and all papers
        cosine_similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()
        cosine_similarities = np.nan_to_num(cosine_similarities, nan=0.0)
        
        # Get the indices of the top_k most similar papers
        similar_indices = cosine_similarities.argsort()[-top_k:][::-1]
        
        # Retrieve the most similar papers
        similar_papers = df.iloc[similar_indices]
        similar_papers = similar_papers.replace({np.nan: None})
        
        response = similar_papers[['title', 'abstract']].to_dict(orient='records')
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Define the main route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the text classification API"}
