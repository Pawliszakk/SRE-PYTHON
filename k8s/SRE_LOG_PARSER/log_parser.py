import json
def parser(log):
    
    
    entry = json.loads(log)

    clientHost = entry["ClientHost"]

    print(entry)
    
    