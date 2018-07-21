# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 23:52:09 2018

@author: vellanki
"""

import pandas as pd
import nltk
import json

with open('dic.txt', 'r') as infile: 
    dic=json.load(infile)


input_text='worst performing category in new york'

n=len(input_text)

from sklearn.feature_extraction.text import CountVectorizer

vec=CountVectorizer(ngram_range=(1,n), stop_words='english')

ngrams=vec.fit_transform([input_text])

vocab=vec.vocabulary_

to_find=list(vocab)

to_find.sort(key=len, reverse=True)

all_entities={}
for entity in to_find:
#    search_term='new york'
#    print (entity)
    search_term_itr=entity.strip().split()

    ite=dic.items()
    all_keys={}
    for key, values in ite:
        flag=1
        for search_term in search_term_itr:
            if search_term.lower() in ''.join(values['list']).lower():
                key_iden=key
            c_set=set(filter(lambda x: search_term.lower() in x.lower(), values['list']))
            if flag==1:
                needed_set=c_set
                flag=0
            else:            
                needed_set=needed_set.intersection(c_set)
        if not len(needed_set)==0:
            all_keys[key_iden]=needed_set
            
    all_entities[entity]=all_keys
        
#            all_found.append([needed_set, key_iden])
#print (all_found)  

keys = all_entities.keys()

keys=[k for k in keys if len(all_entities[k])!=0]

#keys = ['low', 'el', 'helloworld', 'something', 'ellow', 'thing', 'blah', 'thingy']

# flt is [[key, is_substring],...] sorted by key length reversed
flt = [[x, 0] for x in sorted(keys, key=len, reverse=True)]

for i in range(len(flt)):
    p = flt[i]
    if p[1]:  # already removed
        continue
    for j in range(i + 1, len(flt)): # iterate over shorter strings
        q = flt[j]
        if not q[1] and q[0] in p[0]: # if not already removed and is substring
            q[1] = 1  # remove

goodkeys = set(x[0] for x in flt if not x[1])
print (goodkeys) # e.g ['helloworld', 'something', 'thingy', 'blah']

newdict = {k:all_entities[k] for k in goodkeys}

print (newdict)