from __future__ import print_function
import sys
import os
from collections import defaultdict
from re import sub

myDir = "/".join(os.path.realpath(__file__).split("/")[:-1])
UMLS_FILE = myDir + "/data/umls/id_everything_map.txt"
HPO_FILE = myDir + "/data/hp.obo"
PHENOTYPIC_ABNORMALITY_ID = "HP:0000118"


hpo_syn_map = defaultdict(set)
hpo_umls_map = defaultdict(set)
umls_syn_map = defaultdict(set)

def get_hpo_dag():
  hpo = open(HPO_FILE)
  parent_to_children = defaultdict(list)
  for line in hpo:
    if "[Term]" in line:
      hpoID = ""
      continue
    lineData = line.strip().split(": ")
    if len(lineData) < 2: continue
    key = lineData[0]
    value = ": ".join(lineData[1:])
    if key == "id":
      hpoID = value
    if key == "is_a":
      parent_to_children[value.split(" ")[0]].append(hpoID)
  hpo.close()
  return parent_to_children

def get_subdag(dag, key):
  returnSet = set()
  returnSet.add(key)
  for child in dag[key]:
    returnSet = returnSet | get_subdag(dag, child)
  return returnSet

def get_phenotypic_abnormalities():
  parent_to_children = get_hpo_dag()
  return get_subdag(parent_to_children, PHENOTYPIC_ABNORMALITY_ID)

def load_hpo_synonyms():
  phenotypic_abnormalities = get_phenotypic_abnormalities()
  hpo = open(HPO_FILE)
  idToNames = defaultdict(set)
  hpoID = ""
  for line in hpo:
    if "[Term]" in line:
      hpoID = ""
      continue
    lineData = line.strip().split(": ")
    if len(lineData) < 2: continue
    key = lineData[0]
    value = ": ".join(lineData[1:])
    if key == "id": hpoID = value
    if hpoID not in phenotypic_abnormalities: continue
    if key == "name": idToNames[hpoID].add(value.lower())
    if key == "synonym": idToNames[hpoID].add(value.lower().split("\"")[1])
  hpo.close()
  return idToNames

raw_hpo_synonyms = load_hpo_synonyms()
for hpo in raw_hpo_synonyms.keys():
  for syn in raw_hpo_synonyms[hpo]:
    syn = sub('[^0-9a-zA-Z]+', ' ', syn)
    syn = syn.strip().lower()
    syn = list(set(syn.split(" ")) - set([""]))
    syn.sort()
    syn = " ".join(syn)
    hpo_syn_map[hpo].add(syn)

good_hpo_ids = hpo_syn_map.keys()

for line in open(UMLS_FILE):
  lineData = line.strip().split("|")
  umls = lineData[0]
  syn = lineData[14]
  syn = sub(" \[.*\]", "", syn)
  syn = sub(" NOS", "", syn)
  syn = sub("\(diagnosis\)", "", syn)
  syn = sub("\(finding\)", "", syn)
  syn = sub("\[Disease\/Finding\]", "", syn)
  syn = sub("\(disorder\)", "", syn)
  syn = sub("\(qualifier value\)", "", syn)
  syn = sub("\(symptom\)", "", syn)
  syn = sub("\[D\]", "", syn)
  syn = sub("\[X\]", "", syn)
  syn = sub("\(context-dependent category\)", "", syn)
  syn = sub("\-RETIRED\-", "", syn)
  syn = sub("(\& \[symptom\])", "", syn)
  syn = sub("\(situation\)", "", syn)
  syn = sub("\(physical finding\)", "", syn)
  syn = sub('[^0-9a-zA-Z]+', ' ', syn)
  syn = syn.strip()
  syn = syn.lower()
  if len(syn) < 5: continue
  syn = list(set(syn.split(" ")) - set([""]))
  syn.sort()
  syn = " ".join(syn)
  umls_syn_map[umls].add(syn)
  if lineData[11] == "HPO" and lineData[13] in good_hpo_ids: hpo_umls_map[lineData[13]].add(umls)

for hpo in hpo_umls_map.keys():
  for umls in hpo_umls_map[hpo]:
    for syn in umls_syn_map[umls]: hpo_syn_map[hpo].add(syn)

for hpo in hpo_syn_map.keys():
  for syn in hpo_syn_map[hpo]: print(hpo + "\t" + syn)



