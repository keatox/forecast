import re

class Preprocess:
    def __init__(self):
        self.emoticons = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""
        self.regex = [
            self.emoticons,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z’\'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]
    
    def tokenize(self,s):
        tokens_re = re.compile(r'('+'|'.join(self.regex)+')', re.VERBOSE | re.IGNORECASE)
        return tokens_re.findall(s)
    
    def preprocess(self,s, lowercase=False):
        emoticon_re = re.compile(r'^'+self.emoticons+'$', re.VERBOSE | re.IGNORECASE)
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens