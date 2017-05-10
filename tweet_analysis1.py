import re
import json
from nltk.tokenize import word_tokenize
import operator 
from collections import Counter
from nltk.corpus import stopwords
import string
from collections import defaultdict
import vincent
 
with open('IPL.json', 'r') as f:
    line = f.readline() # read only the first tweet/line
    tweet = json.loads(line) # load it as Python dict
    #print(json.dumps(tweet, indent=4)) # pretty-print
    tweet_text = (tweet['text'])
    
def nltk_tokenizer(text):
    return word_tokenize(text)

#same thing can be done manually to recognize hashtags, etc

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




def most_common():
    #Returns a counter object in descending order, ignores stopwords
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']
    
    fname = 'IPL.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
            except Exception as e:
                print(e)
            # Create a list with all the terms without stopwords
            terms_all = [term for term in preprocess(tweet['text'])]
            terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
            
            # Count terms only once, equivalent to Document Frequency
#            terms_single = set(terms_all)
#            # Count hashtags only
#            terms_hash = [term for term in preprocess(tweet['text']) 
#                          if term.startswith('#')]
#            # Count terms only (no hashtags, no mentions)
#            terms_only = [term for term in preprocess(tweet['text']) 
#                          if term not in stop and
#                          not term.startswith(('#', '@'))] 
            
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
            # Update the counter
            count_all.update(terms_stop)
        # Print the first 5 most frequent words
        return count_all.most_common(20)
    
def popular_hashtags():
    """ Returns a list of top 20 hashtags """
    
    fname = 'IPL.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
            except Exception as e:
                print(e)
                
            # Count hashtags only
            terms_hash = [term for term in preprocess(tweet['text']) 
                          if term.startswith('#')]
            
            #Update counter
            count_all.update(terms_hash)
            
        # Print the first 5 most frequent words
        return count_all.most_common(20)
    

def popular_terms():
    """ Returns a list of top 20 popular terms """
    
    #Returns a counter object in descending order, ignores stopwords
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via', 'th', '…','RT','00','20','30','GMT','local','begin','scheduled','win','14','Match','50','time','v','2','The','2017','6','May','8','10,','1','A']
    
    fname = 'IPL.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
            except Exception as e:
                print(e)
            
            
            # Count terms only (no hashtags, no mentions)
            terms_only = [term for term in preprocess(tweet['text']) 
                          if term not in stop and
                          not term.startswith(('#', '@'))] 
            
              
            # Update the counter
            count_all.update(terms_only)
        # Print the first 5 most frequent words
        return count_all.most_common(20)
    
    
def term_cooccurances():
    """ Creates a matrix of term co-occurances """
    
    com = defaultdict(lambda : defaultdict(int))
    
    #Returns a counter object in descending order, ignores stopwords
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via', 'th', '…','RT','00','20','30','GMT','local','begin','scheduled','win','14','Match','50','time','v','2','The','2017','6','May','8','10,','1','A']
    
    fname = 'IPL.json'
    with open(fname, 'r') as f:
        
        for line in f:
            try:
                tweet = json.loads(line)
            except Exception as e:
                print(e)
            
            
            # Count terms only (no hashtags, no mentions)
            terms_only = [term for term in preprocess(tweet['text']) 
                          if term not in stop and
                          not term.startswith(('#', '@'))]
            
            terms_only = [term for term in terms_only if len(term) > 1]
            
              
            # Build co-occurrence matrix
            for i in range(len(terms_only)-1):            
                for j in range(i+1, len(terms_only)):
                    for k in range(i+2,len(terms_only)):
                        w1, w2, w3 = sorted([terms_only[i], terms_only[j], terms_only[k]])                
                        if w1 != w2 and w2 != w3 and w1!= w3:
                            com[w1][w2][w3] += 1
        
            
        com_max = []
        # For each term, look for the most common co-occurrent terms
        for t1 in com:
            t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        # Get the most frequent co-occurrences
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        return terms_max[:20]

def plot_1():
    
    fname = 'IPL.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
            except Exception as e:
                print(e)
                
            # Count hashtags only
            terms_hash = [term for term in preprocess(tweet['text']) 
                          if term.startswith('#')]
            
            #Update counter
            count_all.update(terms_hash)
            
    
#        return count_all.most_common(20)
        word_freq = count_all.most_common(20)
        labels, freq = zip(*word_freq)
        data = {'data': freq, 'x': labels}
        bar = vincent.Bar(data, iter_idx='x')
        bar.to_json('term_freq.json')



