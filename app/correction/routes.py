from flask import request

from app.models.centuryXVIIIWords import centuryXVIIIWords
from app.models.centuryXVIIWords import centuryXVIIWords
from app.models.results import Results
from app.correction import bp
from app.extensions import db

import re
from collections import Counter
import string
import uuid

import nltk
from nltk.metrics import precision, recall

VALID_CENTURIES = [ 7, 8 ]
letterStr = "abcdefghijklmnopqrstuvwxyzăîșț"

@bp.route("/correction/get", methods=['GET'])
def get():
    args = request.args
    if "id" not in args:
      return 'Missing argument (id)!', 400

    tableData = Results.query.get(args["id"])

    id = tableData.__dict__['id']
    century = tableData.__dict__['century']
    originalText = tableData.__dict__['inputText']
    correctedText = tableData.__dict__['outputText']
    precision = tableData.__dict__['precision']
    recall = tableData.__dict__['recall']
    createdAt = tableData.__dict__['createdAt']

    tempObj = {
        "id": id,
        "century": century, 
        "originalText": originalText, 
        "correctedText": correctedText,
        "precision": precision,
        "recall": recall,
        "createdAt": createdAt
    }

    return tempObj


@bp.route('/correction/getAll')
def getAll():
    tableData = Results.query.all()

    correctionResults = []
    for obj in tableData:
      id = obj.__dict__['id']
      century = obj.__dict__['century']
      originalText = obj.__dict__['inputText']
      correctedText = obj.__dict__['outputText']
      precision = obj.__dict__['precision']
      recall = obj.__dict__['recall']
      createdAt = obj.__dict__['createdAt']

      tempObj = {
         "id": id,
         "century": century, 
         "originalText": originalText, 
         "correctedText": correctedText,
         "precision": precision,
         "recall": recall,
         "createdAt": createdAt
      }
      
      correctionResults.append(tempObj)

    return correctionResults

@bp.route('/correction/process', methods=['POST'])
def correct():  
    requestData = request.json
    if "century" not in requestData:
      return 'Missing request parameter (century)!', 400
    if requestData["century"] not in VALID_CENTURIES:
      return 'Century has to be between 7 and 8!', 400
    if "text" not in requestData:
      return 'Missing request parameter (text)!', 400
    
    if requestData["century"] == 7:
      tableData = centuryXVIIWords.query.all()
    else:
      tableData = centuryXVIIIWords.query.all()

    WORDS = {}
    for obj in tableData:
      key = obj.__dict__['word']
      value = obj.__dict__['counter']
      WORDS[key] = value


    def words(text):
      return re.findall(r'[a-zA-ZăĂâÂîÎșȘțȚ&]+', text.lower())

    def P(word, N=sum(WORDS.values())):
        if word not in WORDS:
           return 0
        return WORDS[word] / N
    

    def correctWord(word):
        return max(candidates(word), key=P)


    def candidates(word):
        return (known([word]) or known(checkForSingleError(word)) or known(checkForDoubleErrors(word)) or [word])


    def known(words):
        return set(w for w in words if w in WORDS)

    def checkForSingleError(word):
        letters = letterStr
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)


    def checkForDoubleErrors(word):
        return (e2 for e1 in checkForSingleError(word) for e2 in checkForSingleError(e1))

    data = requestData["text"]

    converted = words(data)
    newData = data

    for word in converted:
        correctedWord = correctWord(word)
        if word != correctedWord:
            newData = newData.replace(word, correctedWord, 1)

    def correct_punctuation(text):
      punctuation = set(string.punctuation)
      text = re.sub(r'([' + re.escape(''.join(punctuation)) + r'])\1+', r'\1', text)
      text = re.sub(r'([' + re.escape(''.join(punctuation)) + r'])(?!\s)', r'\1 ', text)
      return text

    newData = correct_punctuation(newData)
    
    precision_score = 0
    recall_score = 0
    if "correctedText" in requestData:
      correctText = requestData["correctedText"]
      tokens1 = set(nltk.word_tokenize(correctText.lower()))
      tokens2 = set(nltk.word_tokenize(newData.lower()))
      precision_score = precision(tokens1, tokens2)
      recall_score = recall(tokens1, tokens2)

    id = str(uuid.uuid4())

    resultsData = Results(
       id = id,
       century = requestData["century"], 
       inputText = requestData["text"], 
       outputText=newData, 
       precision=precision_score, 
       recall=recall_score
    )
    db.session.add(resultsData)
    db.session.commit()

    return({"id": id, "outputText": newData, "precision": precision_score, "recall": recall_score})
