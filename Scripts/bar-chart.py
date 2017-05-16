import re
import json
#from nltk.tokenize import word_tokenize
#import operator 
from collections import Counter
#from nltk.corpus import stopwords
#import string
#from collections import defaultdict
import plotly.graph_objs as go
from plotly.offline import plot

#init_notebook_mode()

"""Manual Preprocessing"""

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

""" Returns a list of top 20 hashtags """
    
fname = '../json/IPL2.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
        except Exception as e:
            #print(e)
            pass
            
        # Count hashtags only
        try:
            terms_hash = [term for term in preprocess(tweet['text']) 
                      if term.startswith('#') and len(term) > 1]
        except Exception:
            pass
        
        #Update counter
        count_all.update(terms_hash)
        
    # Print the first 5 most frequent words
    word_freq = count_all.most_common(20)
    

""" Plotting """

labels, freq = zip(*word_freq)
data = [go.Bar(
            x=list(labels),
            y=list(freq)
    )]
                
layout = go.Layout(
    title='Bar Chart for #TRUMP',
    yaxis=dict(title='Count'),
    xaxis=dict(title='Hashtag')
)

fig = go.Figure(data=data, layout=layout)

plot(fig, filename='Hashtag-Barplot-Trump.html')