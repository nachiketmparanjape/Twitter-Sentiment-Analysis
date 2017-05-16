import re
import json
#from nltk.tokenize import word_tokenize
import operator 
from collections import Counter
from nltk.corpus import stopwords
import string
from collections import defaultdict
#import vincent



def preprocess(s, lowercase=False):
    
    emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
    regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
     
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]
    
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    
    tokens = tokens_re.findall(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def list_all_terms(fname):
    
    with open(fname, 'r') as f:
        global terms
        terms = []
        i = 0
#        count_all = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
                 
                # Create a list with all the terms without stopwords
                terms = terms + [term for term in preprocess(tweet['text'])]
                i += 1
                print(i)
                
               
                # Update the counter
#                count_all.update(terms_all)
            
            except Exception as e:
                #print(e)
                pass
           
        return

def popular_hashtags(terms):
    """ Returns a list of top 20 hashtags """
    
    counter = Counter()

    terms_hash = [term for term in terms
                              if term.startswith('#') and len(term) > 1]
    
    counter.update(terms_hash)
        
    # Print the first 5 most frequent words
    return counter.most_common(20)


def popular_words(terms):
    """ Returns a list of top 20 hashtags """
    
    #Returns a counter object in descending order, ignores stopwords
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['https','amp','To','says','This','like','They','Here','Just','You',"I'm",'Is','rt', 'via', 'th', '…','RT','00','20','30','GMT','local','begin','scheduled','win','14','Match','50','time','The','2017','May','10,']
    
    counter = Counter()

    terms = [term for term in terms 
                              if term not in stop and
                              not term.startswith(('#', '@','http')) and len(term)>1]
    
    counter.update(terms)
        
    # Print the first 5 most frequent words
    return counter.most_common(20)

def term_cooccurances(terms):
     """ Creates a matrix of term co-occurances """
     return
   

def main():
    
#    print('\nListing the terms...\n')
#    list_all_terms(fname)
    
    print('\nCounting..\n')
    print()
    print("20 most popular hashtags - \n")
    print(popular_hashtags(terms))
    print()
    print()
    
    print("20 most popular terms - \n")
    print(popular_words(terms))
    print()
    print()
    
    print("20 most popular term cooccurances - \n")
    print(popular_words(terms))