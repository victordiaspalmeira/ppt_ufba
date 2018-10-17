from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, articles):
        output = [self.wnl.lemmatize(t, 'v') for t in word_tokenize(articles)]
        output = filter_output(output)
        return output
          
class StemTokenizer(object):
    def __init__(self, lang):
        self.sbs = SnowballStemmer(lang)
    def __call__(self, articles):
        output = [self.sbs.stem(word) for word in word_tokenize(articles)]  
        output = filter_output(output)
        return output
    
def filter_output(output):
    #Filtra pontuação e outros caracteres indesejaveis
    target_tokens = ["'", '-', ')', '(',',', '?', '!', '.', "''", "\\", "/"]
    filtered_output = set(output).difference(target_tokens)
    return filtered_output