def hello():
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
     
     