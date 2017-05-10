import pandas
import json
import vincent
import re
 
dates_ITAvWAL = []
# f is the file pointer to the JSON data set

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


with open('IPL.json', 'r') as f:

    for line in f:
        try:
            tweet = json.loads(line)
        except Exception:
            pass
        # let's focus on hashtags only at the moment
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        # track when the hashtag is mentioned
        if '#IPL2017' in terms_hash:
            dates_ITAvWAL.append(tweet['created_at'])
     
    # a list of "1" to count the hashtags
    ones = [1]*len(dates_ITAvWAL)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_ITAvWAL)
    # the actual series (at series of 1s for the moment)
    ITAvWAL = pandas.Series(ones, index=idx)
     
    # Resampling / bucketing
    per_minute = ITAvWAL.resample('1Min').sum().fillna(0)


#Plot

time_chart = vincent.Line(ITAvWAL)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')