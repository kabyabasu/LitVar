import urllib2
import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import urllib
import bs4 as bs
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
    l = (data[0])
    for i,j in l.iteritems():
        print ("PMID reference for this mutation is : "), j
        return (j)
    
def findPmcId(pmid):
    url = ("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="+str(pmid))
    data = (requests.get(url))
    empty = []
    for i in data:
        empty.append(i)
    data_string = ' '.join(empty)
    
    pattern = r"(?:=pmc).+\s"
    pmcid = re.findall("[P][M][C][\d]{7}",data_string)
    print ("We convereted PMID : "+str(pmid)+" to PMCID : "+str(pmcid[0]))
    return (pmcid[0])



def getFulltext(pmcid):
     url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="+str(pmcid)
     source = urllib.urlopen(url).read()
     soup = bs.BeautifulSoup(source,'lxml')
     body = soup.body
     for p in body.find_all("p"):
         print(p) 
        
    
    
    


mutation = raw_input("Enter mutation Name :" )
ref = lit(mutation)
pmid = pmid(ref)
pmcid = findPmcId(pmid)
getFulltext(pmcid)
