#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
from collections import defaultdict
import re

HPO_FILE = sys.argv[1]

PHENOTYPIC_ABNORMALITY_ID = "HP:0000118"

#Given an HPO DAG and an element, returns the DAG rooted at that element (DAG is a map from parent to child)
def get_subdag(dag, key):
  returnSet = set()
  returnSet.add(key)
  for child in dag[key]:
    returnSet = returnSet | get_subdag(dag, child)
  return returnSet

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

def load_hpo_dag_bilateral():
  hpo = open(HPO_FILE)
  parent_to_children = defaultdict(list)
  child_to_parents = defaultdict(list)
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
      child_to_parents[hpoID].append(value.split(" ")[0])
  hpo.close()
  return parent_to_children, child_to_parents

#Builds and returns a phenotypic-abnormality DAG (HPO DAG starting at Phenotypic Abnormality)
def get_phenotypic_abnormalities():
  parent_to_children = get_hpo_dag()
  return get_subdag(parent_to_children, PHENOTYPIC_ABNORMALITY_ID)

#Returns a map from an HPO ID to the full list of its synonymous names
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

synMap = load_hpo_synonyms()

for hpo in synMap:
  for syn in synMap[hpo]: print(hpo + "\t" + syn)
