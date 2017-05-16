""" Import Packages """
import re
import json
#from nltk.tokenize import word_tokenize
import operator 
from collections import Counter
from nltk.corpus import stopwords
import string
from collections import defaultdict
import math

""" Manual Preprocessing """

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
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens



""" Calculate Term Cooccurances """

com = defaultdict(lambda : defaultdict(int))

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['https','amp','To','says','This','like','They','Here','Just','You',"I'm",'Is','rt', 'via', 'th', '…','RT','00','20','30','GMT','local','begin','scheduled','win','14','Match','50','time','v','2','The','2017','6','May','8','10,','1','A']

fname = '../json/Trump2.json'
with open(fname, 'r') as f:
    count_stop_single = Counter() #Counting Non-stop single words
    
    for line in f:
        try:
            tweet = json.loads(line)
        except Exception as e:
            #print(e)
            pass
        
        
        # Count terms only (no hashtags, no mentions)
        try:
            terms_only = [term for term in preprocess(tweet['text']) 
                      if term not in stop and
                      not term.startswith(('#', '@','http'))]
        except Exception:
            pass
        
        terms_only = [term for term in terms_only if len(term) > 1]
        
        count_stop_single.update(terms_only)
        
          
        # Build co-occurrence matrix
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                
                w1, w2= sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1
                       

""" Compute Probabilities """

# n_docs is the total n. of tweets
p_t = {}
p_t_com = defaultdict(lambda : defaultdict(int))
 
for term, n in count_stop_single.items():
    p_t[term] = n
    for t2 in com[term]:
        p_t_com[term][t2] = com[term][t2]
               
              
""" Sample Vocab """

positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding','win','won','amazing','beautiful','century','Thanks', 'highest','Best','best',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love','triumph', 'triumphal', 'triumphant', 'victory','best','alive','top','like',
    'brilliant','Safe','qualified','chased','successfully','Good'
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(','defeat','loss','Poor','OUT','lose',':/'
]
    
    
""" Semantic Orientation """

pmi = defaultdict(lambda : defaultdict(int))
for t1 in p_t:
    for t2 in com[t1]:
        denom = p_t[t1] * p_t[t2]
        pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)
 
semantic_orientation = {}
for term, n in p_t.items():
    positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
    negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
    semantic_orientation[term] = positive_assoc - negative_assoc
                        
                        
semantic_sorted = sorted(semantic_orientation.items(), 
                         key=operator.itemgetter(1), 
                         reverse=True)
top_pos = semantic_sorted[:10]
top_neg = semantic_sorted[-10:]
 
print(top_pos)
print()
print()
print(top_neg)
                      

