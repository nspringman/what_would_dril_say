# from https://towardsdatascience.com/how-to-rank-text-content-by-semantic-similarity-4d2419a84c32
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
import nltk
import random
import pandas as pd
from nltk.corpus import stopwords

tw = pd.read_csv('data/cleaned_tweets.csv')
tweets = tw['content'].tolist()
qs = pd.read_csv('data/cleaned_questions.csv')['title'].tolist()

# Download stopwords list
nltk.download('punkt')
stop_words = set(stopwords.words('english')) 

# Interface lemma tokenizer from nltk with sklearn
class LemmaTokenizer:
    ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`', '[', ']', '?', 'reddit', 'nsfw']
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]

# Lemmatize the stop words
tokenizer = LemmaTokenizer()
token_stop = tokenizer(' '.join(stop_words))

for i in range(0,10):
    search_terms = qs[(int)(len(qs) * random.random())]
    documents = tweets

    # Create TF-idf model
    vectorizer = TfidfVectorizer(stop_words=token_stop, 
                                tokenizer=tokenizer)
    doc_vectors = vectorizer.fit_transform([search_terms] + documents)

    # Calculate similarity
    cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors).flatten()
    document_scores = [item.item() for item in cosine_similarities[1:]]

    best_match = max(range(len(document_scores)), key=document_scores.__getitem__)
    print(search_terms)
    print(tweets[best_match])
    print('\n')