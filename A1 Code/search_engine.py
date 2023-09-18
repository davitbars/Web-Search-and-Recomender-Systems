#-------------------------------------------------------------------------
# AUTHOR: Davit Barseghyan
# FILENAME: search_engine.py
# SPECIFICATION:  read the file collection.csv and output the accuracy of a proposed search engine given the query q ={cat and dogs}
# FOR: CS 4250- Assignment #1
# TIME SPENT: 30 min so far
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math # needed to import it in order to use logs

documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

#Conduct stopword removal.
filtered_docs = []
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
for doc in documents:
  filtered_doc = ' '.join([word for word in doc.split() if word not in stopWords])
  filtered_docs.append(filtered_doc)

print(f"\nThe docs without stopwords are: {filtered_docs}")

#Conduct stemming.
stemming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

stemmed_documents = []
for doc in filtered_docs:
  words = doc.split()
  stemmed_words = [stemming.get(word, word) for word in words]
  stemmed_doc = ' '.join(stemmed_words)
  stemmed_documents.append(stemmed_doc)

print(f"\nThe stemmed docs are: {stemmed_documents}")

#Identify the index terms.
terms = []
for doc in stemmed_documents:
  temp = doc.split()
  for word in temp:
    if word not in terms:
      terms.append(word)

print(f"\nThe terms are: {terms}")

#Build the tf-idf term weights matrix.
# Calculate the tfs of each word in each doc
tfs = []
for doc in stemmed_documents:
  temp = doc.split()
  term_freq = {}
  for word in temp:
      term_freq[word] = term_freq.get(word, 0) + 1
  tfs.append(term_freq)

# Calculate inverse document frequency (IDF) for each term
num_docs = len(documents)
       
idf_values = []
for term in terms:
    df = sum([1 for doc in stemmed_documents if term in doc.split()])
    idf = math.log10(num_docs / df)
    idf_values.append(idf)

num_terms = len(terms)
tfidf_matrix = []

# Calculate TF-IDF values and populate the matrix
for doc_index, doc in enumerate(stemmed_documents):
    tfidf_row = []
    for term_index, term in enumerate(terms):
        tf = (tfs[doc_index].get(term, 0))/len(doc.split())  # Get TF for the term in the current document
        idf = idf_values[term_index]  # Get IDF for the term
        tfidf_row.append(tf * idf)
    tfidf_matrix.append(tfidf_row)


# Print the TF-IDF matrix with labels
print("\nThe document matrix is:")
print("\tlove\tcat\tdog")
for i, row in enumerate(tfidf_matrix):
    print(f"D{i+1}\t{row[0]:.4f}\t{row[1]:.4f}\t{row[2]:.4f}")

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
query = "cat and dogs"
docScores = []

# Remove Stopwords and stem the words using the initial parameters 
filtered_query = ' '.join([word for word in query.split() if word not in stopWords])
words = filtered_query.split()
stemmed_words = [stemming.get(word, word) for word in words]
stemmed_doc = ' '.join(stemmed_words)

# Binary query vector
binary_query = [1 if term in stemmed_words else 0 for term in terms]

# Calculate document vectors
document_vectors = tfidf_matrix

# Calculate document scores
for doc_vector in document_vectors:
    score = sum(qi * di for qi, di in zip(binary_query, doc_vector))
    docScores.append(score)


# Print document scores
print("\nThe document scores are:")
for i, score in enumerate(docScores):
    print(f"Document D{i + 1} Score: {score:.4f}")

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
threshold = 0.1

# Initialize variables to count true positives, false positives, and false negatives
true_positives = 0
false_positives = 0
false_negatives = 0

# Count true positives, false positives, and false negatives
for score, label in zip(docScores, labels):
    if score >= threshold and label == ' R':
        true_positives += 1
    elif score >= threshold and label == ' I':
        false_positives += 1
    elif score >= threshold and label == ' R':
        false_negatives += 1

# Calculate precision
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

# Calculate recall
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print("\nThe precision and recall are:")
# Print precision and recall
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
