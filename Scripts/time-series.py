import pandas
import json
import plotly.graph_objs as go
from plotly.offline import plot
import re

c = 0
c2 = 0

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


with open('../json/Trump2.json', 'r') as f:
 
    dates_ITAvWAL = []
    # f is the file pointer to the JSON data set
    for line in f:
        c += 1
        try:
            tweet = json.loads(line)
        except Exception:
            pass
        # let's focus on hashtags only at the moment
        try:
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
            c2 += 1
        except Exception:
            pass
        # track when the hashtag is mentioned
        if '#art' in terms_hash:
            dates_ITAvWAL.append(tweet['created_at'])
     
    # a list of "1" to count the hashtags
    ones = [1]*len(dates_ITAvWAL)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_ITAvWAL)
    # the actual series (at series of 1s for the moment)
    ITAvWAL = pandas.Series(ones, index=idx)
     
    # Resampling / bucketing
    per_minute = ITAvWAL.resample('1Min').sum().fillna(0)
    pdf = pandas.DataFrame(per_minute,columns=['count'])
    pdf.reset_index(level=0, inplace=True)


#Plot

data = [
    go.Scatter(
        x=pdf['index'], # assign x as the dataframe column 'x'
        y=pdf['count']
    )
]

layout = go.Layout(
    title='Timeseries for total number of tweets with #Trump',
    yaxis=dict(title='Count'),
    xaxis=dict(title='Time')
)

fig = go.Figure(data=data, layout=layout)

plot(fig, filename='Timeseries-#art.html')

print()
print((c2*100/c))