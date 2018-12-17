import urllib2
import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import urllib
import bs4 as bs

with open("OutPut.txt","w+") as f:
    f.write("***************SUMMARY REPORT*******************")
    f.close

def Summary(mut):
    url1 = "https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/entity/search/{0}".format(mut)
    response = urllib.urlopen(url1)
    resp_text = response.read().decode('UTF-8')
    dataVal= json.loads(resp_text)
    ref_iD_data = dataVal[0]
    hgvsList=ref_iD_data['hgvs']
    rsId=ref_iD_data['rsid']
    CliniCalSig=(ref_iD_data['data']['clinical_significance'])
    GeneNameList = ref_iD_data['data']['genes']
    GeneName = [i['name'] for i in GeneNameList]
    with open("OutPut.txt","a+") as f:
        f.write("\n\nRSiD associated with %s mutation is : " %mut)
        f.write(rsId)
        f.write("\n\nClinical Significance of %s : " %mut)
        f.write(CliniCalSig)
        f.write("\n\nGene associated with %s mutation is : " %mut)
        f.write(GeneName[0])
        f.write("\n\nhgvs associated with %s mutation is : " %mut)
        for item in hgvsList:
        
            f.write("\n"+item)
        f.close
        return rsId

def PMID(rsId):
    url = "https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids={0}".format(rsId)
    response = urllib.urlopen(url)
    resp_text = response.read().decode('UTF-8')
    dataVal= json.loads(resp_text)
    print type(dataVal)

















rsId = Summary("A146T")
    
