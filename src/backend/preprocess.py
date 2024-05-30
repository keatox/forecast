import re
import string

class Preprocess:
    def __init__(self):
        self.__emoticons = r"""(?:
                              [:=;]             # Eyes
                              [oO\-]?           # Nose 
                              [D\)\]\(\]/\\OpP] # Mouth
                              )"""
        self.__regex = [self.__emoticons,
                       r'(?:@[\w_]+)',                   # @-mentions
                       r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
                       r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
                       r'(?:(?:\d+,?)+(?:\.?\d+)?)',     # numbers
                       r"(?:[a-z][a-z’\'\-_]+[a-z])",    # words with - and '
                       r'(?:[\w_]+)',                    # other words
                       r'(?:\S)'                         # anything else
                       ]
        self.__stopwords = self.init_stopwords()

    # returns list of processed terms
    def preprocess(self,s):
        tokens = [self.tokenize(phrase) for phrase in s]
        return self.remove_stopwords(tokens)
    
    # creates a token of certain phrases e.g. @s, links, or URLs
    def tokenize(self,s):    
        s = re.sub(r'<[^>]+>',"",s)
        tokens_re = re.compile(r'('+'|'.join(self.__regex)+')', re.VERBOSE | re.IGNORECASE)
        return tokens_re.findall(s)
    
    # loads stopwords from .txt file
    def init_stopwords(self):
        stopword = list(string.punctuation)
        with open("res/stopwords.txt", "r") as my_file:
            for line in my_file:
                stopword.append(line.strip())
        return stopword
    
    # iterates through each term in terms list and removes stopwords
    def remove_stopwords(self,terms):
        for i in range(len(terms)):
            terms[i] = " ".join([term for term in terms[i] if term.lower() not in self.__stopwords]).lower()
        return terms