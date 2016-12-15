import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')

from wordcloud import WordCloud
from PIL import Image

import nltk
import string

import re

def tokenization_normalization(txt):
    
    mail_adress = re.compile(r"([^\s]+?)@(.+?)\.([^\s]+)")
    txt = mail_adress.sub("", txt) # Remove mail adress

    txt = txt.replace('\'', ' ')
    
    tokens = nltk.word_tokenize(txt) # Tokenization (split on spaces + ponctuation)
    
    punctuations = list(string.punctuation)
    tokenized = [token.lower() for token in tokens if token not in punctuations] # Lowercase + remove ponctuation
    
    digits = re.compile(r'[-.?!,/\*":;()<>|0-9]') # Remove punctuation within words and digits
    tokenized_nodigits = [digits.sub("", token) for token in tokenized]  
    
    token_normalized = list(filter(None, tokenized_nodigits)) # remove empty strings
    
    return token_normalized

def get_stop_words():
    stop_list = nltk.corpus.stopwords.words('english') # Pre-established stop-list
    
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", 
              "december"]
    time = ['am', 'pm', "year", "month", "week", "day", "hour", "minute", "sec", "today", "tomorrow", "yesterday"]
    mail_voc = ['unclassified', 'send', 'date', 're', "doc", "message", "b6", "original", "case", "us", "from", "sent", "to", 
                "subject", "attachments", "cc", "fw", "nt"]
    recurrent_words = ["state", "department", "call", "new", "gov", "release", "part", "in", "no", "gov", "time","say", 
                       "stategov", "would", "say", "also", "go", "want", "make", "know"]
    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    add_stopwords =  days + months + time + mail_voc + recurrent_words + numbers
    
    return stop_list + add_stopwords

def stopword_removal(tokens):
    stop_list = get_stop_words()
    filtered = [word for word in tokens if word not in stop_list] # Remove stop-words
    
    return filtered

def lemmatization(tokens):
    wnl = nltk.stem.wordnet.WordNetLemmatizer() # Generate lemmatizer
    lemmatized = [wnl.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] 
                  else wnl.lemmatize(i) 
                  for i,j in nltk.pos_tag(tokens)] # i = word, j = grammatical class
    return lemmatized

def preprocessing(words, verbose=False):

    words = words.encode('ascii', errors='ignore') # avoid some errors under windows..
    
    # Tokenization - Normalization
    if verbose:
        print("Tokenization - Normalization...")
    token_normalized = tokenization_normalization(words)
    
    # Stopword removal
    if verbose:
        print("Stopword removal...")
    filtered = stopword_removal(token_normalized)
    
    # Lemmatisation
    if verbose:
        print("Lemmatization...")
    lemmatized = lemmatization(filtered)
 
    # We remove stopwords a second time in order to remove tokens which have been lemmatized as stopwords
    filtered_2 = stopword_removal(lemmatized)
    final_processing = [word for word in filtered_2 if len(word)!=1] # Remove single-letter words
    
    return final_processing