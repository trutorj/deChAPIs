from src.app import app
import pymongo
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import pdist, squareform

client = pymongo.MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]

# Extract all the messages and users
mensajes = list(db.find({"type": "message"}, {"user_id":1, "text":1, "_id":0}))

# Extract the content of the messages and the users
textos = [e["text"] for e in mensajes]
usuarios = [e["user_id"] for e in mensajes]

# Check or install stopwords and punkt
nltk.download('stopwords')
nltk.download('punkt')

# Define a function to clean the data
def textCleaner(frase):
    stop_words = set(stopwords.words('english')) 
    # Tokeniza
    word_tokens = word_tokenize(frase)
    # Extract whatever is not a stop word
    cleaned = [w for w in word_tokens if w not in stop_words]
    joined = " ".join(cleaned)
    return joined

# Apply the function to every message
cleaned = [textCleaner(e) for e in textos ]
#print(cleaned)

# Vectorize the words
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(cleaned) 
print(list(count_vectorizer.vocabulary_.keys()))
m = sparse_matrix.todense()
#print(m.shape)

# Create the dataframe of words
doc_term_matrix = sparse_matrix.todense()
df_words = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=usuarios)
#print(df_words.shape)

# Group the users the words by user
user_words = df_words.groupby(df_words.index).sum()
#print(user_words.shape)

# Calculate the distance matrix
user_dist = pd.DataFrame(1/(1 + squareform(pdist(user_words, 'cosine'))),
                         index=user_words.index, columns=user_words.index)
#print(user_dist.shape)

# For each user, calculate the most similar and store in a dictionary
dic_rec = {}
for i in range(len(user_dist.columns)):
    dic_rec[user_dist.columns[i]] = user_dist.iloc[i].sort_values(ascending=False)[1:2].index[0]

