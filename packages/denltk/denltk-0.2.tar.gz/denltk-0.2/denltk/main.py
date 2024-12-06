def hello1():
     print('''
           import nltk
from nltk.tag import hmm

# Create a small custom corpus (word, POS tag pairs)
train_data = [
    [('The', 'DT'), ('cat', 'NN'), ('sat', 'VBD')],
    [('A', 'DT'), ('dog', 'NN'), ('barked', 'VBD')],
    [('The', 'DT'), ('dog', 'NN'), ('runs', 'VBZ')],
    [('She', 'PRP'), ('loves', 'VBZ'), ('dogs', 'NNS')]
]

# Create the HMM tagger
trainer = hmm.HiddenMarkovModelTrainer()

# Train the HMM POS tagger
tagger = trainer.train(train_data)

# Test sentence
test_sentence = "The dog runs".split()

# Tag the test sentence
tagged_sentence = tagger.tag(test_sentence)

# Print the tagged sentence
print(tagged_sentence)
''')
     
     
     
def hello2():
     print('''
# Program 2: Text Classification using Naive Bayes
# Implement a Naive Bayes classifier for text classification using the 20 Newsgroups dataset.

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Load the 20 Newsgroups dataset
newsgroups = fetch_20newsgroups(subset='all')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(newsgroups.data, newsgroups.target, test_size=0.2, random_state=42)

# Convert text data into feature vectors using CountVectorizer
vectorizer = CountVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the Naive Bayes classifier
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vectorized, y_train)

# Make predictions
y_pred = nb_classifier.predict(X_test_vectorized)

# Evaluate the model
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Classification Report:\n", metrics.classification_report(y_test, y_pred))

''')
     
def hello3():
     print('''
# Program 3: Dependency Parsing using CKY Algorithm
# Implement the CKY algorithm for dependency parsing using a context-free grammar.

import nltk
from nltk import CFG

# Define a simple context-free grammar (CFG)
grammar = CFG.fromstring("""
  S -> NP VP
  VP -> V NP
  NP -> Det N
  Det -> 'a' | 'the'
  N -> 'dog' | 'cat'
  V -> 'chases' | 'sees'
""")

# Input sentence (as a list of words)
sentence = ['the', 'dog', 'chases', 'a', 'cat']

# Create a parser using the CKY algorithm
parser = nltk.ChartParser(grammar)

# Parse the sentence
for tree in parser.parse(sentence):
    tree.pretty_print()
           ''')
     
def hello4():
     print('''
# Program 4: Word Embeddings using Word2vec 
# Implement Word2vec using the Gensim library and train it on a given text corpus.
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data (if necessary)
# nltk.download('punkt')

# Sample corpus (a list of sentences)
corpus = [
    "I love machine learning",
    "Word embeddings are useful in NLP",
    "Word2Vec is a popular algorithm",
    "Machine learning is fun"
]

# Tokenize the corpus (split into words)
tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

# Train Word2Vec model
model = Word2Vec(tokenized_corpus, vector_size=50, window=3, min_count=1, sg=0)
# model
# # Example: Get the vector for a word
word_vector = model.wv['machine']

# Output the word vector
print("Vector for 'machine':", word_vector)

# Example: Find most similar words to 'machine'
similar_words = model.wv.most_similar('machine', topn=3)
print("Most similar words to 'machine':", similar_words)

           ''')
     

def hello5():
     print('''
# Program 5: Text Summarization using Extractive Summarization
# Implement an extractive summarization algorithm using Textrank

import spacy
import pytextrank

# Load a pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Add the TextRank component to the spaCy pipeline
nlp.add_pipe("textrank")

# Sample text to summarize
text = """
Text summarization is the process of creating a concise and coherent version of a longer text document. 
There are two main types of text summarization techniques: extractive and abstractive. 
Extractive summarization selects key sentences directly from the text, while abstractive summarization generates new sentences.
"""

# Process the text
doc = nlp(text)

# Extractive summarization: Get top sentences based on TextRank
summary = [sent.text for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=2)]

# Print the summary
print("Summary:", " ".join(summary))

           ''')
     

def hello6():
     print('''
# Program 6: Named Entity Recognition using HMM
# Implement a Hidden Markov Model (HMM) for Named Entity Recognition (NER).

import nltk
from nltk.tag import hmm
from nltk.corpus import conll2002

# Download necessary NLTK datasets
# nltk.download('conll2002')

# Train a Hidden Markov Model (HMM) for NER using the conll2002 dataset
train_sents = conll2002.iob_sents('esp.train')  # Training data
test_sents = conll2002.iob_sents('esp.testb')  # Test data

# Train the HMM model
trainer = hmm.HiddenMarkovModelTrainer()
ner_model = trainer.train(train_sents)

# Test the model on a sentence
test_sentence = [("John", "NP"), ("Doe", "NP"), ("is", "VB"), ("a", "DT"), ("doctor", "NN")]
ner_tags = ner_model.tag_sents([test_sentence])

# Print the NER results
print(ner_tags)
           ''')
     

def hello7():
     print('''
# Program 7: Sentiment Analysis using Supervised Learning
# Implement a supervised learning model for sentiment analysis using the IMDB dataset.

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_files

# Load the IMDB dataset (reviews labeled with sentiment: positive/negative)
# You can download the IMDB dataset from sklearn or other sources, here it is assumed to be pre-loaded
# If using an external dataset, you can load it as follows:
# imdb = load_files("path_to_imdb_data", categories=["pos", "neg"])

# For simplicity, we use a smaller example dataset with predefined labels
data = {
    'data': ["I love this movie", "This was a terrible movie", "Amazing film!", "I hate this film", "Great performance", "Not good at all"],
    'target': [1, 0, 1, 0, 1, 0]
}

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=0.3, random_state=42)

# Convert text to numerical features using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Predict on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))

           ''')
     
     
def hello8():
     print('''
# Program 8: Semantic Similarity Measure using WordNet
# Implement a semantic similarity measure using WordNet.

from nltk.corpus import wordnet as wn

# Download necessary NLTK data
import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# Define two words
word1 = "dog"
word2 = "cat"

# Get WordNet synsets for each word
synsets1 = wn.synsets(word1)
synsets2 = wn.synsets(word2)

# Calculate similarity between the first synset of both words
similarity = synsets1[0].wup_similarity(synsets2[0])

# Output the similarity score
print(f"Semantic similarity between '{word1}' and '{word2}': {similarity}")

''')
     
     
def hello9():
     print('''
# Program 9: Character-to-Sentence Embeddings using CNN
# Implement character-to-sentence embeddings using a Convolutional Neural Network (CNN).

import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# Sample sentences (a small example for simplicity)
sentences = ["I love machine learning", "Deep learning is amazing", "Natural language processing is fun"]

# Tokenize the sentences by characters
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(sentences)
sequences = tokenizer.texts_to_sequences(sentences)

# Pad the sequences to have equal length
X = pad_sequences(sequences, padding='post')

# Define the model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=50, input_length=X.shape[1]))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification (can be adjusted)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()

# Example: Training the model (dummy labels for illustration)
y = np.array([1, 1, 0])  # Example labels (binary classification)
model.fit(X, y, epochs=5)
           ''')
     
     
def hello10():
     print('''

import nltk
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Sample document and query
document = """
Text summarization is the task of creating a shortened version of a text document that retains the most important information. 
There are two primary types of summarization: extractive and abstractive. Extractive summarization selects key sentences from the document, 
while abstractive summarization generates new sentences to summarize the content.
"""
query = "summarization"

# Tokenize the document into sentences
sentences = nltk.sent_tokenize(document)

# Vectorize sentences using TF-IDF
vectorizer = TfidfVectorizer(stop_words=stopwords.words("english"))
X = vectorizer.fit_transform(sentences)

# Compute similarity matrix
cosine_sim = (X * X.T).toarray()

# Create a graph using the correct function
graph = nx.from_numpy_array(cosine_sim)

# Rank sentences using PageRank
ranked_sentences = nx.pagerank(graph)

# Sort sentences based on their rank
sorted_sentences = sorted(ranked_sentences, key=ranked_sentences.get, reverse=True)

# Select top 2 sentences for the summary
summary = [sentences[i] for i in sorted_sentences[:2]]

# Output the summary
print("Summary:", " ".join(summary))
     
     ''')