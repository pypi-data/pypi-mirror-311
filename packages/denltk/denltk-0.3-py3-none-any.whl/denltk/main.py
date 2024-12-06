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
     
     
def tejas():
     print('''
          pro 1 


import nltk
from nltk.corpus import treebank
from sklearn.metrics import confusion_matrix, accuracy_score

# Download necessary resources
nltk.download('treebank')
nltk.download('universal_tagset')

# Load the Penn Treebank dataset with universal tagset
tagged_sentences = nltk.corpus.treebank.tagged_sents(tagset='universal')

# Split the data into training and testing sets (e.g., 80/20 split)
train_size = int(len(tagged_sentences) * 0.8)
train_set = tagged_sentences[:train_size]
test_set = tagged_sentences[train_size:]

# Train an HMM using NLTK's HiddenMarkovModelTrainer
from nltk.tag.hmm import HiddenMarkovModelTrainer

trainer = HiddenMarkovModelTrainer()
hmm_model = trainer.train(train_set)

# Evaluate the model on the test set
accuracy = hmm_model.evaluate(test_set)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Generate predictions for the test set to create confusion matrix
true_tags = []
predicted_tags = []

for sentence in test_set:
    words = [word for word, _ in sentence]
    true_tags.extend([tag for _, tag in sentence])
    predicted_tags.extend(hmm_model.tag(words))

# Flatten predicted_tags (removing words)
predicted_tags_flat = [tag for _, tag in predicted_tags]

# Calculate confusion matrix
cm = confusion_matrix(true_tags, predicted_tags_flat, labels=hmm_model._states)
print(f"Confusion Matrix:\n{cm}")

# Optional: Normalize confusion matrix and print as a heatmap
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(cm, annot=True, fmt='d', xticklabels=hmm_model._states, yticklabels=hmm_model._states, cmap='coolwarm')
plt.xlabel('Predicted Tags')
plt.ylabel('True Tags')
plt.title('Confusion Matrix for PoS Tagging')
plt.show()




prog 2 


import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk

# Download NLTK resources
nltk.download('stopwords')

# 1. Load Dataset
categories = None  # Use all categories
data = fetch_20newsgroups(subset='all', categories=categories, remove=('headers', 'footers', 'quotes'))

# 2. Data Preprocessing
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = text.split()
    tokens = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return " ".join(tokens)

# Preprocess all documents
data_cleaned = [preprocess(doc) for doc in data.data]

# 3. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(data_cleaned, data.target, test_size=0.2, random_state=42)

# 4. Feature Extraction
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# 5. Train Naive Bayes Classifier
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# 6. Evaluate the Model
y_pred = model.predict(X_test_vect)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

report = classification_report(y_test, y_pred, target_names=data.target_names)
print("Classification Report:\n", report)





prog 3 


import nltk
from nltk import CFG
from nltk.parse import ChartParser

# 1. Define Grammar in Chomsky Normal Form (CNF)
grammar = CFG.fromstring("""
    S -> NP VP
    VP -> V NP | V
    NP -> Det N | N
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog' | 'mat'
    V -> 'chased' | 'sat'
""")

# 2. Create a Parser
parser = ChartParser(grammar)

# 3. Parse a Sentence
def parse_sentence(sentence):
    """
    Parse a given sentence using NLTK's ChartParser.
    Args:
        sentence: Input sentence as a list of words.
    """
    print("Parsing Sentence:", " ".join(sentence))
    trees = list(parser.parse(sentence))  # Parse the sentence
    if trees:
        for tree in trees:
            print("Dependency Tree:")
            tree.pretty_print()  # Visualize the tree
    else:
        print("The sentence could not be parsed.")

# Example Usage
sentence = "the cat chased the dog".split()
parse_sentence(sentence)



prog 4 

# 4

# File: word2vec_embedding.py

import gensim
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')

# 1. Preprocess the Corpus
def preprocess_corpus(corpus):
    """
    Preprocess the corpus by tokenizing, removing stopwords, and keeping only alphabetic words.
    Args:
        corpus: List of sentences (text data).
    Returns:
        List of tokenized and preprocessed sentences.
    """
    stop_words = set(stopwords.words('english'))
    processed_corpus = []
    for sentence in corpus:
        tokens = word_tokenize(sentence.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        processed_corpus.append(filtered_tokens)
    return processed_corpus

# Example Corpus (Replace this with your dataset)
corpus = [
    "The cat sat on the mat.",
    "The dog chased the cat.",
    "Dogs and cats are animals.",
    "The mat was sat on by the cat.",
]

# Preprocess the corpus
processed_corpus = preprocess_corpus(corpus)
print("Processed Corpus:", processed_corpus)

# 2. Train Word2Vec Model
def train_word2vec(corpus, vector_size=100, window=5, min_count=1, epochs=10):
    """
    Train a Word2Vec model using Gensim.
    Args:
        corpus: Preprocessed corpus.
        vector_size: Dimensionality of word vectors.
        window: Context window size.
        min_count: Minimum frequency for a word to be included.
        epochs: Number of training epochs.
    Returns:
        Trained Word2Vec model.
    """
    model = Word2Vec(sentences=corpus, vector_size=vector_size, window=window, min_count=min_count, workers=4)
    model.train(corpus, total_examples=model.corpus_count, epochs=epochs)
    return model

# Train the Word2Vec model
model = train_word2vec(processed_corpus)

# 3. Visualize Word Embeddings
def visualize_embeddings(model, method="pca"):
    """
    Visualize word embeddings using PCA or t-SNE.
    Args:
        model: Trained Word2Vec model.
        method: Dimensionality reduction method ("pca" or "tsne").
    """
    words = list(model.wv.index_to_key)  # Get vocabulary
    vectors = model.wv[words]           # Get word vectors

    if method == "pca":
        reducer = PCA(n_components=2)
        reduced_vectors = reducer.fit_transform(vectors)
    elif method == "tsne":
        reducer = TSNE(n_components=2, random_state=42, perplexity=5)
        reduced_vectors = reducer.fit_transform(vectors)
    else:
        raise ValueError("Invalid method. Choose 'pca' or 'tsne'.")

    # Plot the reduced vectors
    plt.figure(figsize=(10, 10))
    plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], edgecolors='k', c='orange')
    for i, word in enumerate(words):
        plt.annotate(word, xy=(reduced_vectors[i, 0], reduced_vectors[i, 1]), fontsize=12)
    plt.title(f"Word Embeddings Visualization ({method.upper()})")
    plt.show()

# Visualize embeddings using PCA
visualize_embeddings(model, method="pca")

# Visualize embeddings using t-SNE
visualize_embeddings(model, method="tsne")



prog 5 


# 5
# Required Libraries
!pip install rouge-score

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import networkx as nx
from rouge_score import rouge_scorer
nltk.download('punkt')
nltk.download('stopwords')

# Text Preprocessing
def preprocess_text(text):
    """
    Preprocess the input text: tokenize sentences and words, remove stopwords.
    Args:
        text (str): The input text.
    Returns:
        List of tokenized sentences and cleaned sentences.
    """
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)  # Sentence tokenization
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence.lower())  # Tokenize words
        words = [word for word in words if word.isalnum() and word not in stop_words]
        processed_sentences.append(words)
    return sentences, processed_sentences

# Build Similarity Matrix
def build_similarity_matrix(sentences):
    """
    Create a similarity matrix for the sentences using cosine similarity.
    Args:
        sentences (list): List of tokenized sentences.
    Returns:
        similarity_matrix (numpy.ndarray): Sentence similarity matrix.
    """
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Join words to recreate sentences
    joined_sentences = [' '.join(sentence) for sentence in sentences]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(joined_sentences)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# TextRank Algorithm
def textrank_summarization(text, top_n=3):
    """
    Summarize the text using the TextRank algorithm.
    Args:
        text (str): The input text.
        top_n (int): Number of sentences to include in the summary.
    Returns:
        summary (str): Extracted summary.
    """
    original_sentences, processed_sentences = preprocess_text(text)
    similarity_matrix = build_similarity_matrix(processed_sentences)

    # Create a graph from the similarity matrix
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Rank sentences based on scores
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(original_sentences)), reverse=True)

    # Select top N sentences for the summary
    summary = " ".join([sentence for _, sentence in ranked_sentences[:top_n]])
    return summary

# Example Text
text = """
Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence
concerned with the interactions between computers and human language, in particular how to program computers
to process and analyze large amounts of natural language data. The result is a computer capable of
"understanding" the contents of documents, including the contextual nuances of the language within them.
The technology can then accurately extract information and insights contained in the documents as well as
categorize and organize the documents themselves.
"""

# Generate Summary
summary = textrank_summarization(text, top_n=2)
print("Summary:")
print(summary)

# Evaluate Summary using ROUGE
def evaluate_summary(reference, generated):
    """
    Evaluate the generated summary using ROUGE metrics.
    Args:
        reference (str): Reference summary.
        generated (str): Generated summary.
    Returns:
        scores (dict): ROUGE scores.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores

# Reference Summary (Manually written)
reference_summary = """
NLP is a field of AI focused on programming computers to process and analyze natural language.
It enables computers to understand documents' content, extract insights, and organize documents.
"""

# Evaluate the generated summary
rouge_scores = evaluate_summary(reference_summary, summary)
print("\nROUGE Scores:")
print(rouge_scores)


prog 6 

import unicodedata
import nltk
from nltk.corpus import conll2002
from hmmlearn.hmm import MultinomialHMM
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np

# Download NLTK data
nltk.download('conll2002')

# Normalize text to handle special characters
def normalize_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

# Load and preprocess the dataset
def preprocess_data(data):
    normalized_data = []
    for sent in data:
        normalized_sent = [(normalize_text(word), tag) for word, tag, _ in sent]
        normalized_data.append(normalized_sent)
    return normalized_data

# Load train and test datasets
train_data = preprocess_data(conll2002.iob_sents('esp.train'))
test_data = preprocess_data(conll2002.iob_sents('esp.testb'))

# Extract features (words) and labels (NER tags)
def extract_features_and_labels(data):
    X = [[word for word, tag in sent] for sent in data]
    y = [[tag for word, tag in sent] for sent in data]
    return X, y

X_train, y_train = extract_features_and_labels(train_data)
X_test, y_test = extract_features_and_labels(test_data)

# Flatten data for encoding
flat_X_train = [word for sent in X_train for word in sent]
flat_y_train = [tag for sent in y_train for tag in sent]
flat_X_test = [word for sent in X_test for word in sent]
flat_y_test = [tag for sent in y_test for tag in sent]

# Encode words and tags
word_encoder = LabelEncoder()
tag_encoder = LabelEncoder()

word_encoder.fit(flat_X_train + flat_X_test)
tag_encoder.fit(flat_y_train + flat_y_test)

X_train_encoded = [word_encoder.transform([word for word in sent]) for sent in X_train]
X_test_encoded = [word_encoder.transform([word for word in sent]) for sent in X_test]

y_train_encoded = [tag_encoder.transform([tag for tag in sent]) for sent in y_train]
y_test_encoded = [tag_encoder.transform([tag for tag in sent]) for sent in y_test]

# Prepare input for HMM (flatten sequences for hmmlearn)
def prepare_hmm_data(X, y):
    lengths = [len(seq) for seq in X]
    X_flat = np.concatenate(X)
    y_flat = np.concatenate(y)
    return X_flat, y_flat, lengths

X_train_hmm, y_train_hmm, train_lengths = prepare_hmm_data(X_train_encoded, y_train_encoded)
X_test_hmm, y_test_hmm, test_lengths = prepare_hmm_data(X_test_encoded, y_test_encoded)

# Train HMM
hmm_model = MultinomialHMM(n_components=len(tag_encoder.classes_), random_state=42, n_iter=100)
hmm_model.fit(X_train_hmm.reshape(-1, 1), train_lengths)

# Predict using HMM
y_pred_hmm = []
start_idx = 0
for length in test_lengths:
    end_idx = start_idx + length
    seq = X_test_hmm[start_idx:end_idx].reshape(-1, 1)
    predicted = hmm_model.predict(seq)
    y_pred_hmm.extend(predicted)
    start_idx = end_idx

# Decode predictions and true labels
y_pred_decoded = tag_encoder.inverse_transform(y_pred_hmm)
y_true_decoded = tag_encoder.inverse_transform(y_test_hmm)

# Evaluation
accuracy = accuracy_score(y_true_decoded, y_pred_decoded)
conf_matrix = confusion_matrix(y_true_decoded, y_pred_decoded, labels=tag_encoder.classes_)
classification_report_str = classification_report(y_true_decoded, y_pred_decoded, labels=tag_encoder.classes_)

print(f"Accuracy: {accuracy:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(classification_report_str)


prog 7 

import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('movie_reviews')

from nltk.corpus import movie_reviews

# Load IMDB dataset from NLTK
def load_imdb_data():
    """
    Load the IMDB dataset from the NLTK movie_reviews corpus.
    Returns:
        - data: List of text reviews.
        - labels: List of sentiment labels ('pos', 'neg').
    """
    data = []
    labels = []
    for fileid in movie_reviews.fileids():
        data.append(movie_reviews.raw(fileid))
        labels.append(movie_reviews.categories(fileid)[0])
    return data, labels

# Preprocess the dataset
def preprocess_text(text):
    """
    Preprocess text data by tokenizing, removing stopwords, and keeping only alphabetic tokens.
    Args:
        text: Raw text data.
    Returns:
        Preprocessed text as a string.
    """
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(filtered_tokens)

# Load and preprocess the dataset
data, labels = load_imdb_data()
data = [preprocess_text(review) for review in data]

# Encode labels as binary values
label_map = {'pos': 1, 'neg': 0}
labels = [label_map[label] for label in labels]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42, stratify=labels)

# Build a pipeline for training
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),  # Convert text to bag-of-words
    ('tfidf', TfidfTransformer()),     # Apply TF-IDF transformation
    ('classifier', LinearSVC())        # Linear Support Vector Classifier
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"F1-Score: {f1:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))


prog 8 

import nltk
from nltk.corpus import wordnet as wn
from sklearn.metrics import mean_squared_error
import numpy as np

# Download NLTK resources
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('words')

# WordSim-353 dataset (A small subset for demonstration)
# Each pair contains two words and the similarity score (rated from 0 to 10 by human annotators)
wordsim_353 = [
    ("car", "auto", 9.0),
    ("ship", "boat", 8.0),
    ("dog", "cat", 9.5),
    ("man", "woman", 10.0),
    ("tree", "bush", 7.5),
    ("apple", "banana", 8.5),
    ("love", "hate", 2.0),
    ("king", "queen", 9.5),
    ("school", "education", 8.0),
    ("dog", "wolf", 8.5),
]

# Function to calculate similarity using Wu-Palmer similarity
def calculate_similarity(word1, word2):
    """
    Calculate the semantic similarity between two words using Wu-Palmer similarity.
    Args:
        word1: First word.
        word2: Second word.
    Returns:
        Similarity score (float), or None if no synsets are found.
    """
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    if not synsets1 or not synsets2:
        return 0.0  # Return 0 if no synsets found for either word

    # Take the first synset (most common sense)
    synset1 = synsets1[0]
    synset2 = synsets2[0]

    # Calculate similarity using Wu-Palmer similarity
    similarity = synset1.wup_similarity(synset2)
    return similarity if similarity is not None else 0.0

# List to store predicted and true similarity scores
predicted_scores = []
true_scores = []

# Calculate similarity for each word pair and store the results
for word1, word2, true_score in wordsim_353:
    predicted_score = calculate_similarity(word1, word2)
    predicted_scores.append(predicted_score)
    true_scores.append(true_score)

# Evaluate the results using Mean Squared Error (MSE)
mse = mean_squared_error(true_scores, predicted_scores)
print(f"Mean Squared Error between predicted and true similarity scores: {mse:.4f}")

# Optionally, you could calculate the Pearson correlation for a better evaluation
from scipy.stats import pearsonr
corr, _ = pearsonr(predicted_scores, true_scores)
print(f"Pearson correlation: {corr:.4f}")


prog 9 



import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Step 1: Load the IMDB dataset
# IMDB dataset comes preloaded with Keras
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

# Step 2: Preprocess the data (pad sequences)
max_sequence_length = 500  # Max length for each sentence
x_train = pad_sequences(x_train, maxlen=max_sequence_length)
x_test = pad_sequences(x_test, maxlen=max_sequence_length)

# Step 3: Define a simple CNN model for sentence embeddings
input_text = Input(shape=(max_sequence_length,))

# Character-level embedding (the characters are tokens already in the IMDB dataset)
embedding_layer = Embedding(input_dim=10000, output_dim=128, input_length=max_sequence_length)(input_text)

# Apply Convolutional layers
conv_layer = Conv1D(filters=128, kernel_size=3, activation='relu')(embedding_layer)
pool_layer = GlobalMaxPooling1D()(conv_layer)

# Dense layer
dense_layer = Dense(128, activation='relu')(pool_layer)
dropout_layer = Dropout(0.5)(dense_layer)
output = Dense(1, activation='sigmoid')(dropout_layer)

# Create the CNN model
model = Model(inputs=input_text, outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 4: Train the model
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

# Step 5: Get the sentence embeddings by taking the output from the CNN layers (before the final dense layer)
embedding_model = Model(inputs=input_text, outputs=pool_layer)

# Get sentence embeddings for the training data
sentence_embeddings = embedding_model.predict(x_train)

# Step 6: Visualize the sentence embeddings using PCA or t-SNE

# First, reduce the dimensionality using PCA
pca = PCA(n_components=2)
reduced_embeddings_pca = pca.fit_transform(sentence_embeddings)

# Plot the reduced embeddings using PCA
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings_pca[:, 0], reduced_embeddings_pca[:, 1], c=y_train, cmap='coolwarm', alpha=0.5)
plt.title("Sentence Embeddings Visualization using PCA")
plt.colorbar()
plt.show()

# Alternatively, reduce using t-SNE
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings_tsne = tsne.fit_transform(sentence_embeddings)

# Plot the reduced embeddings using t-SNE
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings_tsne[:, 0], reduced_embeddings_tsne[:, 1], c=y_train, cmap='coolwarm', alpha=0.5)
plt.title("Sentence Embeddings Visualization using t-SNE")
plt.colorbar()
plt.show()





prog 10

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer
import string
import sklearn

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# 1. Preprocess the text (tokenization, stopword removal)
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)  # Tokenize text into sentences
    clean_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence.lower())  # Tokenize into words and lowercase
        clean_words = [word for word in words if word.isalpha() and word not in stop_words]
        clean_sentences.append(' '.join(clean_words))

    return clean_sentences, sentences

# 2. Create a similarity matrix based on cosine similarity
def create_similarity_matrix(sentences):
    # Create the cosine similarity matrix
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# 3. Implement Graph-Based Method (TextRank)
def text_rank_summary(text, top_n=3):
    # Preprocess the text
    clean_sentences, original_sentences = preprocess_text(text)

    # Create a similarity matrix
    similarity_matrix = create_similarity_matrix(clean_sentences)

    # Build a graph based on the similarity matrix
    nx_graph = nx.from_numpy_array(similarity_matrix)

    # Apply PageRank (TextRank)
    scores = nx.pagerank(nx_graph)

    # Sort the sentences by their score
    ranked_sentences = [original_sentences[i] for i in sorted(scores, key=scores.get, reverse=True)]

    # Select top N sentences
    summary = ' '.join(ranked_sentences[:top_n])
    return summary

# 4. Evaluate the summary using ROUGE metric
def evaluate_summary(reference, summary):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, summary)
    return scores

# Example text and query
text = """
Natural language processing (NLP) is a sub-field of artificial intelligence (AI) that is concerned with the interactions between computers and human (natural) languages. It deals with applications such as speech recognition, text analysis, sentiment analysis, machine translation, and much more. NLP is a highly interdisciplinary field, combining linguistics, computer science, and AI techniques to understand and generate human language in a way that is both meaningful and valuable.
The ultimate goal of NLP is to develop systems that can perform tasks that require understanding and manipulating natural language, such as summarizing text, answering questions, and making recommendations. NLP has made significant progress over the past few years, with the development of powerful language models like GPT and BERT. These models have revolutionized the way machines understand and interact with human language, making NLP a crucial technology in today's world.
"""

query = "NLP and its applications"

# Generate summary based on the query (query-based summarization)
summary = text_rank_summary(text, top_n=2)
print("Generated Summary:", summary)

# Evaluate using ROUGE (using the query as the reference summary)
rouge_scores = evaluate_summary(query, summary)
print("ROUGE Scores:", rouge_scores)
 

 
           ''')