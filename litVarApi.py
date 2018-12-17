import urllib
import urllib2
import json
import time
import sys
import getopt
import os, re
import os.path
from os import path
import subprocess

if len (sys.argv) >= 3 :
    print ("Only one arguments is allowed! ")
    sys.exit (1)
elif len(sys.argv)==2:
    rsIdList=''
    searchQuery=sys.argv[1]
    url_Submit="https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/entity/search/{0}".format(searchQuery)
    req = (url_Submit)
    try:
        response = urllib.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        resp_text = response.read().decode('UTF-8')
#         data=response.read().decode('utf-8')
        
        dataVal= json.loads(resp_text)
        
        print (len(dataVal))
        print ("=========================\n")
        strt=0
        while strt < len(dataVal):
          print(strt)
          rsId=dataVal[strt]['rsid']
          rsIdList+=","+rsId
          print (dataVal[strt]['data'])
          gene_nameList=dataVal[strt]['data']['genes']
          if dataVal[strt]['data'].get('clinical_significance'):
              clinicalSign=dataVal[strt]['data']['clinical_significance']
          else:
              clinicalSign=''
          
          print ("========clinical_significance===========: "+clinicalSign)
          print ("========rsId===========: "+rsId)
          hgvsList=dataVal[strt]['hgvs']
          for hgvsName in hgvsList:
              print ("====hgvs name===============: "+hgvsName)
          for gName in gene_nameList:
              print ("========gene name===========: "+gName['name'])
          print ("=========================\n")
          strt += 1
        rsIdList=rsIdList.lstrip(',')
#         params = dict(rsids=rsIdList)
#         paramData = urllib.parse.urlencode(params).encode("utf-8")
#         print (paramData)
        rsid_url_Submit="https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids={0}".format(rsIdList)
        print (rsid_url_Submit)
        responseRsid = (rsid_url_Submit)
        responseRsid_val = urllib.urlopen(responseRsid)
        rsid_text = responseRsid_val.read().decode('UTF-8')
    #   data=response.read().decode('utf-8')
        pmidTextVal= json.loads(rsid_text)
        strt1=0
        print (len(pmidTextVal))
        while strt1 < len(pmidTextVal):
#             rsId=pmidTextVal[strt1]['rsid']
#             pmId=pmidTextVal[strt1]['pmids']
            print (pmidTextVal[strt1]['rsid'])
            print (pmidTextVal[strt1]['pmids'])
            strt1 += 1
            print ("=========================\n")
            
          
#         for res in dataVal:
#             for res1 in res:
#                 print (dataVal[strt])
#                 print ("%%%%%%%%%%%%%%%%%%%%%\n\n")
#             
#         strt=strt+1





#           print (dataVal[strt]['id'])
#           url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/publications'
#           values = {'facets' : {'page':1},
#                   'query' : {'variant':[rsId]}
#                    }
#           json_data = json.dumps(values).encode('utf8')
#           request = urllib.request.Request(url, data=json_data, method='POST',
#                                  headers={'Content-Type': 'application/json'})
#           print (request.read().decode('utf8'))
