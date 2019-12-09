from __future__ import print_function
import sys
import os
from collections import defaultdict
from re import sub

mapFile = sys.argv[1]

id_syn_map = defaultdict(set)

dumb_words = set(["congenital", "unspecified", "of", "in", "the", "and"])

for line in open(mapFile):
  lineData = line.strip().split("\t")
  termid = lineData[0]
  syn = lineData[1]
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
  syn = list(set(syn.split(" ")) - set([""]) - dumb_words)
  syn.sort()
  syn = " ".join(syn)
  if len(syn) < 5: continue
  id_syn_map[termid].add(syn)

for termid in id_syn_map.keys():
  for syn in id_syn_map[termid]: print(termid + "\t" + syn)



