import re
import string

class Preprocess:
    def __init__(self):
        self._emoticons = r"""(?:
                              [:=;]             # Eyes
                              [oO\-]?           # Nose 
                              [D\)\]\(\]/\\OpP] # Mouth
                              )"""
        self._regex = [self._emoticons,
                       r'(?:@[\w_]+)',                   # @-mentions
                       r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
                       r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
                       r'(?:(?:\d+,?)+(?:\.?\d+)?)',     # numbers
                       r"(?:[a-z][a-z’\'\-_]+[a-z])",    # words with - and '
                       r'(?:[\w_]+)',                    # other words
                       r'(?:\S)'                         # anything else
                       ]
    
    def tokenize(self,s):    
        s = re.sub(r'<[^>]+>',"",s)
        tokens_re = re.compile(r'('+'|'.join(self._regex)+')', re.VERBOSE | re.IGNORECASE)
        return tokens_re.findall(s)
    
    def preprocess(self,s, lowercase=False):
        emoticon_re = re.compile(r'^'+self._emoticons+'$', re.VERBOSE | re.IGNORECASE)
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens
    
    def remove_stopwords(self,terms,stock=" "):
        stopword = list(string.punctuation) + [stock.lower(),'“','”']
        with open("res/english.txt", "r") as my_file:
            for line in my_file:
                stopword.append(line.strip())
        for i in range(len(terms)):
            terms[i] = " ".join([term for term in terms[i] if term.lower() not in stopword]).lower()
        return terms