import re, sys

# line = "Q03154	PF07687;PF01546;	ACY1	VARIANT 179 179 N -> S (in dbSNP:rs887540). /FTId=VAR_051805.; VARIANT 197 197 R -> W (in ACY1D; loss of activity; dbSNP:rs121912700). {ECO:0000269|PubMed:17562838, ECO:0000269|PubMed:21414403}. /FTId=VAR_043113.; VARIANT 233 233 E -> D (in ACY1D; loss of activity; dbSNP:rs121912699). {ECO:0000269|PubMed:16465618, ECO:0000269|PubMed:21414403}. /FTId=VAR_026104.; VARIANT 353 353 R -> C (in ACY1D; loss of activity; dbSNP:rs121912698). {ECO:0000269|PubMed:16274666, ECO:0000269|PubMed:16465618, ECO:0000269|PubMed:17562838, ECO:0000269|PubMed:21414403}. /FTId=VAR_026105.; VARIANT 378 378 R -> Q (in ACY1D; dbSNP:rs150480963). {ECO:0000269|PubMed:21414403}. /FTId=VAR_065562.; VARIANT 378 378 R -> W (in ACY1D; slightly reduced activity; dbSNP:rs148346337). {ECO:0000269|PubMed:21414403}. /FTId=VAR_065563.; VARIANT 381 381 E -> D (in a breast cancer sample; somatic mutation). {ECO:0000269|PubMed:16959974}. /FTId=VAR_036076.; VARIANT 386 386 R -> C (in ACY1D; loss of activity; dbSNP:rs2229152). {ECO:0000269|PubMed:21414403}. /FTId=VAR_020452.; VARIANT 393 393 R -> H (in ACY1D; dbSNP:rs121912701). {ECO:0000269|PubMed:17562838}. /FTId=VAR_043114."
# line = "Q9P0K7	PF00023;PF12796;	RAI14	VARIANT 44 44 A -> T (in dbSNP:rs17521570). /FTId=VAR_026673.; VARIANT 45 45 S -> N (in dbSNP:rs35941954). /FTId=VAR_055517.; VARIANT 499 499 V -> L (in dbSNP:rs10472941). /FTId=VAR_055518.; VARIANT 870 870 A -> S (in dbSNP:rs1048944). {ECO:0000269|PubMed:14702039, ECO:0000269|PubMed:15489334}. /FTId=VAR_055519."
# pattern = re.compile('VARIANT(\w+)\)\.')
# [('393', '393', 'R', 'H', 'in ACY1D; dbSNP:rs121912701', 'ECO:0000269', '17562838')]

# g_pattern=re.compile('\;(A-Z]+\d+)VARIANT')
# pattern = re.compile('(\w+)\tVARIANT (\d+) (\d+) ([A-Z]+) \-\> ([A-Z]+) \((.*)\)\. \{?(ECO:\d+)\|PubMed\:(\d+)\}?')
# pattern = re.compile('\w*\;*\t*VARIANT (\d+) (\d+) ([A-Z]+) \-\> ([A-Z]+) \((.*)\)\.* \{*(.*)\|(.*)\}*')
global pmid_pattern
pmid_pattern = re.compile('ECO\:\d+\|(.*)')
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

def fetch_pmid(word):
    d = word.split(',')
    r_value = ""
    for ref in d:
        # 		print("reading word : {}".format(ref))
        actual_ref = pmid_pattern.findall(ref)
        new_ref = str(actual_ref[0])
        final_ref = new_ref.replace("PubMed:", ",")
        r_value = r_value + final_ref
    r_value = r_value.replace(",", "", 1)
    r_value = r_value.replace("}", "", 1)
    return r_value


noise_list = ["is", "a", "this", "of", ",","..."]



def _remove_noise(input_text):
    words = input_text.split()
    for word in words:
        word.replace(",","",1)
    noise_free_words = [word for word in words if word not in noise_list]
    noise_free_text = " ".join(noise_free_words)
    return noise_free_text

def lof_check(final_description):
    functionality = ""
    lof_main_list = ["loss", "decrease", "reduc", "abolish", "dominant-negative", 'impair',' inactivation']
    #     supplementary_keywords=['activity','function','phosphorylation','stability','degradation']

    supplementary_keywords = [' activity', ' function', ' phosphorylation', ' stability',
                              ' degradation']

    for l in lof_main_list:
        match_count = 0
        m = re.search(l, final_description)
        without_noise_description=_remove_noise(final_description)
        if m:
            print("Matched {} at position -- {} till -- {}".format(l, m.start(), m.end()))
            main_sp = m.end()
            for sup in supplementary_keywords:
                m2 = re.search(sup, final_description)
                if m2:
                    # if (re.search(r'(decrease[d])',final_description)) :
                    print("Supplementary keyword Matched {} at position -- {} till -- {}".format(sup, m2.start(),
                                                                                                 m2.end()))
                    sup_sp = m2.end()
                    match_count = 1
        if match_count == 1:
            #             if sup_sp > main_sp :
            print("Correct order")
            functionality = "LOF"
            break
    return functionality


def cof_check(final_description):
    functionality = ""
    cof_main_list = ['retain', 'no']
    supplementary_keywords = [' effect', ' activity', ' function', ' phosphorylation', ' stability', ' degradation']

    for l in cof_main_list:
        match_count = 0
        m = re.search(l, final_description)
        if m:
            print("Matched {} at position -- {} till -- {}".format(l, m.start(), m.end()))
            main_sp = m.end()
            for sup in supplementary_keywords:
                m2 = re.search(sup, final_description)
                if m2:
                    # if (re.search(r'(decrease[d])',final_description)) :
                    print("Supplementary keyword Matched {} at position -- {} till -- {}".format(sup, m2.start(),
                                                                                                 m2.end()))
                    sup_sp = m2.end()
                    match_count = 1
        if match_count == 1:
            #             if sup_sp > main_sp :
            print("Correct order")
            functionality = "COF"
            break
    return functionality


def gof_check(final_description):
    functionality = ""
    gof_main_list = ["gain", "increase", "enhance"]
    supplementary_keywords = [' activation', ' activity', ' function', ' phosphorylation', ' stability', ' degradation']
    for l in gof_main_list:
        match_count = 0
        m = re.search(l, final_description)
        if m:
            print("Matched {} at position -- {} till -- {}".format(l, m.start(), m.end()))
            main_sp = m.end()
            for sup in supplementary_keywords:
                m2 = re.search(sup, final_description)
                if m2:
                    # if (re.search(r'(decrease[d])',final_description)) :
                    print("Supplementary keyword Matched {} at position -- {} till -- {}".format(sup, m2.start(),
                                                                                                 m2.end()))
                    sup_sp = m2.end()
                    match_count = 1
        if match_count == 1:
            #             if sup_sp > main_sp :
            print("Correct order")
            functionality = "GOF"
            break
    return functionality


pattern = re.compile('\w*\;*\t*VARIANT (\d+) (\d+) ([A-Z]+) \-\> ([A-Z]+) \((.*)\)\.*\s*\{*(.*)\|*(.*)\}*')
# lof_main_list=["loss","decrease","reduce","abolish","dominant-negative"]
# gof_main_list=["gain","increase"]
# supplementary_keywords=['activity','function','phosphorylation','stability','degradation']
# pattern = re.compile('VARIANT (.*)')
input_file = sys.argv[1]
output_file = "extracted_data.csv"
with open(input_file) as fr, open(output_file, 'w') as fw:
    fw.write("Gene\tMutation\tReference\tFunctionality\tExtractedDescription\tDescription\n")
    for l in fr:

        line = l.rstrip()
        try:
            gene = line.split('\t')[2]
        except:
            continue

        # 		print("Reading Line \033[92m{}".format(line))
        print("\033[96mGene :{}".format(gene))
        c = 0
        data = line.split('. /')
        # 		print("*****Reading Data \033[92m{}".format(data))
        for d in data:
            c += 1

            print("\033[94mCount :{} \033[91mSearching in pattern: \033[94m\n{}\033[0m".format(c, d))
            abstracted = pattern.findall(d)
            if abstracted:
                print(abstracted)
                abstracted = abstracted[0]
                mutation = str(abstracted[2]) + str(abstracted[0]) + str(abstracted[3])
                description = str(abstracted[4])
                reference = str(abstracted[5]) + str(abstracted[6])
                if reference != "":
                    reference = fetch_pmid(reference)
                print("****************Checking for Functionality *******************")
                final_description = ""
                details_description = description.split(';')
                for desc in details_description:
                    if (re.search(r'dbSNP', desc)) or (re.search(r'in allele', desc)):
                        continue
                    else:
                        final_description = final_description + "," + desc

        #                 lof_match=0
        #                 gof_match=0
        #                 cof_match=0
        #                 if (re.search(r'(increase in kinase activity)|(gain of function)|(gain of activity)|(increases level of protein)|(increase[d] protein)',final_description)) :
        #                     functionality="GOF"
        #                     gof_match=1
        #                 if (re.search(r'(decrease[d] protein abundance)|(reduction in protein)|(loss of function)|(reduce[d] activity)|(loss of activity)|(loss of enzymatic activity)|(decreased maturation)|(reduce[d] expression)|(impair)|(enzyme activity reduced)|(reduction of activity)|(loss of ATPase activity)|(abolishes enzyme activity)',final_description)) :
        # # 				if (re.search(r'(loss of [function|activity|enzymatic|expression|ATPase])|([reduc[ed|tion]|decrease[d]|] [activity|expression|protein|maturation])|(activity reduce[d])',final_description)):
        #                     functionality="LOF"
        #                     lof_match=1
        #                 if (re.search(r'retain',final_description)) :
        #                     functionality="COF"
        #                     cof_match=1
                gof_match = gof_check(final_description)
                lof_match = lof_check(final_description)
                lof_match = lof_check(final_description)
                cof_match = cof_check(final_description)
                functionality=lof_match
                print("The GOF functionality check result is : {}".format(gof_match))
                print("The LOF functionality check result is : {}".format(lof_match))
                print("The COF functionality check result is : {}".format(cof_match))
                if lof_match == "" and gof_match == "" and cof_match == "":
                    functionality = "NA"
                    print("Not predicted")
                elif lof_match == "" and gof_match == "" and cof_match != "":
                    functionality = cof_match
                    print("Predicted as COF")

                elif lof_match == "" and gof_match != "" and cof_match == "":
                    functionality = gof_match
                    print("Predicted as GOF")

                elif lof_match != "" and gof_match == "" and cof_match == "":
                    functionality = lof_match
                    print("Predicted as LOF")

                info = gene + "\t" + mutation + "\t" + reference + "\t" + functionality + "\t" + final_description + "\t" + description + "\n"

                print("Info :{}".format(info))
                fw.write(info)