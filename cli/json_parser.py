import json

def json_export(DFA, filename):
    with open("USER/json/"+filename+".json","w") as fp:
        json.dump(DFA, fp, sort_keys=True, indent=4)

def json_load(filename):
    with open('USER/json/'+filename+'.json', 'r') as fp:
        data = json.load(fp)
    return data