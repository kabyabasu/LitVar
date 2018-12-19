import urllib2
import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import urllib
import bs4 as bs
from nltk import tokenize

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
        return rsId,hgvsList

def PMID(rsId,mut):
    url = "https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids={0}".format(rsId) 
    response = urllib.urlopen(url)
    resp_text = response.read().decode('UTF-8')
    dataVal= json.loads(resp_text)
    pmid_list = dataVal[0]['pmids']
    with open("OutPut.txt","a+") as f:
        f.write("\n\n*******************************************")
        f.write("\n\nprinting the list of PMIDs for  %s" %mut)
        f.write("\n")
        f.seek(0)
        for item in pmid_list:
            f.write("%s,"%str(item))
        f.write("\n")
        f.write("\n\n*******************************************")
        f.close
        return pmid_list
        
def PMCID(pmid_list,mut):
    pmcid_list = []
    for i in pmid_list:
        s =0
        url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={0}".format(i)
        response = urllib.urlopen(url)
        resp_text = response.read().decode('UTF-8')
        dataVal = bs.BeautifulSoup(resp_text,'xml')
        soup = dataVal.body
        for i in dataVal.find_all("record"):
            if i.has_attr('pmcid'):
                pmcid_list.append(i['pmcid'])
                print "Sit Tight while Ultron converting your PMID to PMCID"
                print "Converting......"
            else:
                pass
    with open("OutPut.txt","a+") as f:
        f.write("\n\n*******************************************")
        f.write("\n\nprinting the list of PMCID for  %s" %mut)
        f.write("\n")
        f.seek(0)
        for item in pmcid_list:
            f.write("%s,"%item)
        f.write("\n")
        f.write("\n\n*******************************************")
        f.close
        return pmcid_list


with open("Outallput.txt","w+") as f:
    f.close()
def getFulltext(pmcid_list,mut):
     for i in pmcid_list:
      
         url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="+str(i)
         source = urllib.urlopen(url).read()
         soup = bs.BeautifulSoup(source,'lxml')
         body = soup.body
         with open("Outallput.txt","w+") as f:
             f.write("\n\n*******************************************")
             f.write("\n\nTest matching to PMCID :"+i)
             for p in body.find_all("p"):
                     f.write("\n"+str(p))
             f.close()
         def remove_tag(text):
             with open("Clean_Out.txt","a+") as t:
                  clean = re.compile('<.*?>')
                  txt = re.sub(clean,'',text)
                  t.write(txt)
                  return txt 
             
         def tokenize(txt):
             tt = re.split(r' *[\.\?!][\'"\)\]]* *', txt) 
             return tt
         
         def serachItem(tt):
             searched_text = [i for i in tt if mut in i]
             with open("OutPut.txt","a+") as f:
                  
                      f.write("\n\n*******************************************")
                      f.write("\n\nTest matching to PMCID :"+i)
                      for item in searched_text:
                          f.write("%s,"%str(item))
                      f.write("\n\n*******************************************")
                      f.close()
             #print searched_text
            # return searched_text  
          
 
         text1 = open("Outallput.txt","r")
         text = text1.read() 
         txt = remove_tag(text)
         tt = tokenize(txt)
         serachItem(tt)





















rsId,hgvsList = Summary("A146T")
pmid_list = PMID(rsId,"A146T")
pmcid_list = PMCID(pmid_list,"A146T")
getFulltext(pmcid_list,"A146T")
getFulltext(pmcid_list,"A146T")
