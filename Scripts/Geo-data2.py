import json

fname = '../json/Trump2.json'

with open(fname, 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        try:
            tweet = json.loads(line)
        except Exception:
            pass
        try:
            if tweet['coordinates']:
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": tweet['coordinates'],
                    "properties": {
                        "text": tweet['text'],
                        "created_at": tweet['created_at']
                    }
                }
                geo_data['features'].append(geo_json_feature)
        except Exception:
            pass
 
# Save geo data
with open('../json/geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))