
import pandas as pd
import nltk
import json
from nltk.stem import PorterStemmer

from difflib import SequenceMatcher

def sim(row):
    return SequenceMatcher(None, row.entity.lower(), row.list.lower()).ratio()

porter_stemmer=PorterStemmer()
#
#def stem_sentences(sentence):
#    tokens = sentence.split()
#    stemmed_tokens = [porter_stemmer.stem(token) for token in tokens]
#    return ' '.join(stemmed_tokens)

dic_df=pd.read_csv('dic_df.csv')


input_text='worst performing categories by sales in new york that are shipped the same day'
#input_text='expenditure per capita of india'

n=len(input_text)

from sklearn.feature_extraction.text import CountVectorizer

vec=CountVectorizer(ngram_range=(1,n))

ngrams=vec.fit_transform([input_text])

vocab=vec.vocabulary_

to_find=list(vocab)

from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

to_find=list(set(to_find)-stop)

to_find.sort(key=len, reverse=True)

#############get dic_df from data prep



all_entities={}

found_entities=pd.DataFrame(columns=['entity','col_name', 'list'])
#    looping through all the n grams 
for entity in to_find:
#    entity='category'
    flag=0
    search_term_itr=entity.strip().split()
    
    dic_df['flag']=False
    
    for search_term in search_term_itr:
        search_term=porter_stemmer.stem(search_term)
#        print ((dic_df['stem'].str.contains(search_term)), (dic_df['flag']))
        if flag==0:
            dic_df['flag']=(dic_df['stem'].str.contains(search_term)) | (dic_df['flag'])
            flag=1
        else:
            dic_df['flag']=(dic_df['stem'].str.contains(search_term)) & (dic_df['flag'])
        
#    print (entity)
#    print (dic_df[dic_df['flag']==True])
    temp_df=dic_df[dic_df['flag']==True].copy()
    temp_df['entity']=entity
    found_entities=found_entities.append(temp_df[['entity','col_name', 'list']])

found_entities['similarity']=found_entities.apply(lambda row:sim(row), axis=1)    

#print (found_entities)
    

keys=found_entities.entity.unique().tolist()

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

found_entities=found_entities[found_entities.entity.isin(goodkeys)]

found_entities[['list','similarity']]
found_entities=found_entities.sort_values(['entity','similarity'], ascending=[True, False])
found_entities=found_entities[found_entities.similarity>0.2]

idx = found_entities.groupby(['entity'])['similarity'].transform(max) == found_entities['similarity']

found_entities=found_entities[idx]

print (found_entities)        
        
            
            
            
            
            
            
            
            
            
