#-------------------------------------------------------------------------
# AUTHOR: Davit Barseghyan
# FILENAME: db_connection_mongo.py
# SPECIFICATION: MongoDB operations functions
# FOR: CS 4250- Assignment #2
#-----------------------------------------------------------*/

#importing some Python libraries
from bson import ObjectId
from pymongo import MongoClient
import string

def connectDataBase():
    client = MongoClient("mongodb://localhost:27017")  
    db = client["corpus"]
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    terms_dict = {}

    strippedDocText = docText.translate(str.maketrans('', '', string.punctuation))

    custom_punctuation = "!@#$%^&*()_+[]{};:'\"<>,.?/~`"  # Customize this list as needed
    num_chars = len(docText) - docText.count(' ') - sum(docText.count(p) for p in custom_punctuation)

    for term in strippedDocText.lower().split():
        terms_dict[term] = terms_dict.get(term, 0) + 1

    # create a list of dictionaries to include term objects.
    terms_list = [{"term": term, "termCountInThisDoc": count} for term, count in terms_dict.items()]

    #Producing a final document as a dictionary including all the required document fields
    document = {
        "docId": docId,
        "title": docTitle,
        "numChars": num_chars,
        "category": docCat,
        "date": docDate,
        "text": docText,
        "terms": terms_list,
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({"docId": docId})
    
def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    col.delete_one({"docId": docId})

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    index = {}
    for document in col.find():
        for term_obj in document["terms"]:
            term = term_obj["term"]
            count = term_obj["termCountInThisDoc"]
            if term in index:
                index[term] += f",{document['title']}:{count}"
            else:
                index[term] = f"{document['title']}:{count}"
    return index