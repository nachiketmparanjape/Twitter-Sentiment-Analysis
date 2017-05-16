# Tweets are stored in "fname"
import json
import pandas as pd
import seaborn as sns

fname = '../json/IPL.json'
count = 0
count2 = 0

with open(fname, 'r') as f:
    citydf = pd.DataFrame(columns=['city','created_at'])
    for line in f:
        count2 += 1
        try:
            tweet = json.loads(line)
        except Exception:
            pass
        if tweet['user']['location']:
            
            
            citydf.set_value(count,'city',tweet['user']['location'])
            citydf.set_value(count,'created_at',tweet['created_at'])
            count += 1
 
# Save geo data
#with open('../json/geo_data.json', 'w') as fout:
#    fout.write(json.dumps(geo_data, indent=4))
    
print (count)
print (count2)


df = pd.DataFrame(citydf.city.value_counts())
df = df[df['city'] > 2]
df.reset_index(level=0, inplace=True)
#citylist = list(df.index)
#citydf = citydf[citydf['city'] in citylist]

sns.factorplot(y='city',x='index', data=df, kind = 'bar')
    

