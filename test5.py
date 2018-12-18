import urllib2
import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import urllib
import bs4 as bs
import nltk
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
             searched_text = []
             for i in tt:
                 if mut in i:
                     searched_text.append(i)
             print searched_text
             return searched_text  
          
 
         text1 = open("Outallput.txt","r")
         text = text1.read() 
         txt = remove_tag(text)
         tokenize(txt)
             #print s
             #for i in s:
                 #if mut in i:
                     #print i
         #print ("root")            
         #tree = ET.parse(source)
         #root = tree.getroot()
         #for i in root.iter("p"):
           #  print (i.text)
pmcid_list = ["PMC5513919","PMC5606956","PMC5482736","PMC5440149","PMC5348988","PMC5312443","PMC5722514","PMC5293722","PMC5058686","PMC4924686","PMC5731886","PMC5685224","PMC3394966","PMC5746083","PMC4404337","PMC4336936","PMC5630340","PMC6056937","PMC3964313","PMC5904111","PMC4239073","PMC5103950","PMC5837474","PMC5527457","PMC5978263","PMC4198623","PMC3774610","PMC4177034","PMC6029483","PMC4558179","PMC2647674","PMC5023838","PMC4906127","PMC4744099","PMC6113428","PMC5403533","PMC5519811","PMC5537494","PMC4716245","PMC4134735","PMC5122332","PMC4618462","PMC3969235","PMC4999563","PMC4037834","PMC5672930","PMC4978128","PMC5920233","PMC4332779","PMC5537488","PMC4557483","PMC5780472","PMC3844320","PMC5522202","PMC5342719","PMC5923365","PMC5341940","PMC6030971","PMC3623853","PMC5008380","PMC5656456","PMC4171587","PMC5522060","PMC4827807","PMC2837563","PMC4506514","PMC5536012","PMC5471055","PMC2943514","PMC5945530","PMC3927413","PMC4527087","PMC4424481","PMC5817792","PMC5106330","PMC5945518","PMC5047012","PMC4482484","PMC4049792","PMC5129933","PMC5829675","PMC5998651","PMC4051153","PMC4655812","PMC6053835","PMC5685774","PMC4377644","PMC5243866","PMC4039802","PMC5739515","PMC4687048","PMC4951343","PMC4518505","PMC4695154","PMC5963609","PMC5042411","PMC5764779","PMC4970882","PMC4741554","PMC4673229","PMC5015815","PMC5845515","PMC4832337","PMC4393591","PMC4114707","PMC3142798","PMC5437268","PMC4062050","PMC4968864","PMC5129956","PMC4721683","PMC5008360","PMC4486202","PMC4600465","PMC5880263","PMC5362218","PMC6089851"]
getFulltext(pmcid_list,"A146T")
