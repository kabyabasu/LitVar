import urllib2
import requests
import json
ref = ""
def lit(mut):
    url = ("https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/entity/search/"+mut)
    data = requests.get(url).json()
    dataF = json.dumps(data)
    dataD = json.loads(dataF) 
    dataL = (data[0])
    print(type(dataL)) 
    ref = str(dataL['name'])
    return ref

def pmid(ref):
    query = {"variant":["litvar@rs121913527##"]}
    url = ("https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/pmids?query=%7B%22variant%22%3A%5B%22litvar%40"+ref+"%23%23%22%5D%7D")
    data = requests.get(url).json()
    print (data[0])
    





ref = lit("A146T")
pmid(ref)
