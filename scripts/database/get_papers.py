from pymongo import MongoClient
import pandas as pd
import spacy
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

nlp = spacy.load("en_core_web_sm")

MONGO_URI = 'mongodb://datasci:scopus888@localhost:27017'

client = MongoClient(MONGO_URI)

db = client['datasci']
collection = db['papers']

documents = collection.find()

documents_list = list(documents)

# Extract relevant nested fields
data = []
for doc in documents_list:
    title = doc.get('content', {}).get('title', '')
    abstract = doc.get('content', {}).get('abstract', '')
    keywords = doc.get('content', {}).get('keywords', '')
    category = doc.get('category', '')  # Assuming category is a top-level field
    data.append({'title': title, 'abstract': abstract, 'keywords': keywords, 'category': category})

# Convert list of documents to a DataFrame
df = pd.DataFrame(data)

# Optionally, remove the MongoDB-specific _id field
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

# Preprocess text function
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Combine and preprocess text fields
texts = df['title'] + " " + df['abstract'] + " " + df['keywords']
texts = texts.apply(preprocess_text)

# Tokenization
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
max_len = 100
X = pad_sequences(sequences, maxlen=max_len)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['category'])
y = to_categorical(y, num_classes=len(label_encoder.classes_))

# Split data into training and validation sets
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Close the MongoDB connection
client.close()

# Print shapes of the prepared data
print(f"X_train shape: {X_train.shape}")
print(f"X_val shape: {X_val.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_val shape: {y_val.shape}")
