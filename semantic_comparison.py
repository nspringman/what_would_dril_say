# https://towardsdatascience.com/how-to-rank-text-content-by-semantic-similarity-4d2419a84c32
from re import sub
from gensim.utils import simple_preprocess
import numpy as np
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity
import pandas as pd
import random
from nltk.corpus import stopwords
import json
import time

tw = pd.read_csv('data/cleaned_tweets.csv')['content'].tolist()
qs = pd.read_csv('data/cleaned_questions.csv')['title'].tolist()

#query_string = 'fruit and vegetables'
# documents = ['cars drive on the road', 'tomatoes are actually fruit']

# query_string = "Why do I sometimes feel that I am the most useless person in the world?"
documents = tw

stopwords = set(stopwords.words('english'))
start = time.time()
# From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
def preprocess(doc):
    # Tokenize, clean up input document string
    doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    doc = sub(r'<[^<>]+(>|$)', " ", doc)
    doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

# Preprocess the documents, including the query string
corpus = [preprocess(document) for document in documents]

print(time.time() - start)
# Load the model: this is a big file, can take a while to download and open
glove = api.load("glove-wiki-gigaword-50")    
similarity_index = WordEmbeddingSimilarityIndex(glove)

# Build the term dictionary, TF-idf model
# dictionary = Dictionary(corpus+[query])
dictionary = Dictionary(corpus)
tfidf = TfidfModel(dictionary=dictionary)
print(time.time() - start)
# Create the term similarity matrix.  
similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)
print(time.time() - start)
output_file = open('semantic_comparison.json','w+')
output = []

for x in range (0,300):
    query_string = qs[(int)(len(qs) * random.random())] # pick a random question
    query = preprocess(query_string)

    # Compute Soft Cosine Measure between the query and the documents.
    # From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
    query_tf = tfidf[dictionary.doc2bow(query)]

    index = SoftCosineSimilarity(
                tfidf[[dictionary.doc2bow(document) for document in corpus]],
                similarity_matrix)

    doc_similarity_scores = index[query_tf]

    # Output the sorted similarity scores and documents
    sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
    output_obj = { 'question': query_string }
    answer_array = []
    ticks = 0
    for idx in sorted_indexes:
        ticks += 1
        if ticks == 5:
            break
        answer_array.append({
            'answer': documents[idx],
            'similarity': f'{doc_similarity_scores[idx]:0.3f}',
            'sentiment': 0.6
        })
    output_obj['answers'] = answer_array
    output.append(output_obj)

end = time.time()
print(end - start)
json.dump(output, output_file)