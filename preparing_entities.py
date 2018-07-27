""""
POS tag list:

CC	coordinating conjunction
CD	cardinal digit
DT	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW	foreign word
IN	preposition/subordinating conjunction
JJ	adjective	'big'
JJR	adjective, comparative	'bigger'
JJS	adjective, superlative	'biggest'
LS	list marker	1)
MD	modal	could, will
NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
NNPS	proper noun, plural	'Americans'
PDT	predeterminer	'all the kids'
POS	possessive ending	parent's
PRP	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB	adverb	very, silently,
RBR	adverb, comparative	better
RBS	adverb, superlative	best
RP	particle	give up
TO	to	go 'to' the store.
UH	interjection	errrrrrrrm
VB	verb, base form	take
VBD	verb, past tense	took
VBG	verb, gerund/present participle	taking
VBN	verb, past participle	taken
VBP	verb, sing. present, non-3d	take
VBZ	verb, 3rd person sing. present	takes
WDT	wh-determiner	which
WP	wh-pronoun	who, what
WP$	possessive wh-pronoun	whose
WRB	wh-abverb	where, when


'CC', 'DT', 'IN', 'PDT', 'TO', 'UH'
"""

import pandas as pd
import nltk
import json
from nltk.stem import PorterStemmer
import re
from difflib import SequenceMatcher  # gives the similarity score of 2 strings
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

#similarity cutoff score
sim_cutoff=0.3

# declared a function to get similarity score than using the whole seqence matcher code at every place
def sim(row):
    return SequenceMatcher(None, row.entity.lower(), row.list.lower()).ratio()

#porter stemmer to stem user input. to make apples to apples comparision
porter_stemmer=PorterStemmer()

#load the data dictionary created while preparing the data
dic_df=pd.read_csv('dic_df.csv', encoding='utf8')

# list of POS tags to be ignored in user input before making ngrams
waste_pos=['CC', 'DT', 'IN', 'PDT', 'TO', 'UH', 'PRP', 'PRP$']
#input_text='expenditure per capita of india'

# defining a function that can be use anywhere to retrive the entities found in the user input
# output of this function is 2 dataframes: 1. sure entities (similarity score greater than declared on top)
#                                          2. suggested entities (less probable entities), but can be used for suggesting question to user
def get_entities(input_text):
    
    #length of text entered. used to make ngrams till this size
    n=len(input_text)
    
    # removing waste POS tagged words. these tags are listed above in waste POS list
    text_woin=''
    for each in input_text.split():
        tag=nltk.pos_tag([each])
        print (tag[0][1], each)
        if tag[0][1] not in waste_pos:
            text_woin=text_woin+ " " + each
    
    
    input_text=text_woin.strip() # assigning the text stripped of waste POS tags as input text for this function
    
    #extract ngrams from the input text    
    vec=CountVectorizer(ngram_range=(1,n))    
    ngrams=vec.fit_transform([input_text])    
    vocab=vec.vocabulary_ # this gives all the combinations of n grams from user input
    to_find=list(vocab) # pushed to list for easier use

    # taking out the ngrams that are just stop words and sorting by bigger n grams to smaller
    #this is not done before making ngrams because we would miss out of ngrams that are valid when a stopword is in it
    stop = set(stopwords.words('english'))
    to_find=list(set(to_find)-stop)
    to_find.sort(key=len, reverse=True)
    
    #creating an empyt data fram of found entities. this is split at the end to make sure entities and suggested entity dataframes
    found_entities=pd.DataFrame(columns=['entity','col_name', 'list'])
    
    
    #    looping through all the n grams 
    for entity in to_find:
        #    entity='category'
        
        #optimize to skip smaller ngrams that have bigger ngrams that have already found a match
        if entity in ''.join(found_entities.entity.unique().tolist()):
            continue
        
        flag=0 # used to identify the first iteration of search term to make the first entry to
        search_term_itr=entity.strip().split() # split the entity to find each word in stems, so that, order of the words doesn't matter
        
        dic_df['flag']=False # add a column to flag the colms that found a match with the whole n gram. Also, reset for every new entity
        
        #lo0p through all words in ngram to flag the match
        for search_term in search_term_itr:
            search_term=porter_stemmer.stem(search_term)
    #        print ((dic_df['stem'].str.contains(search_term)), (dic_df['flag']))
            if flag==0:
                dic_df['flag']=(dic_df['stem'].str.contains(search_term)) | (dic_df['flag'])
                flag=1
            else:
                dic_df['flag']=(dic_df['stem'].str.contains(search_term)) & (dic_df['flag'])
            
        # write all found items to found_enties dataframe user the entity under consideration
        temp_df=dic_df[dic_df['flag']==True].copy() # getting only the matches
        temp_df['entity']=entity # adding the entity for which the match was found
        found_entities=found_entities.append(temp_df[['entity','col_name', 'list']]) # appending to final list
     
    # add similarity between actual user text and text found in columns. this is because the actual comparision happend on stems and not actual text
    found_entities['similarity']=found_entities.apply(lambda row:sim(row), axis=1)    


    # used before the optimization to eliminate search of sub string of bigger ngrams was done
#    keys=found_entities.entity.unique().tolist()
#    
#    flt = [[x, 0] for x in sorted(keys, key=len, reverse=True)]
#    
#    for i in range(len(flt)):
#        p = flt[i]
#        if p[1]:  # already removed
#            continue
#        for j in range(i + 1, len(flt)): # iterate over shorter strings
#            q = flt[j]
#            if not q[1] and q[0] in p[0]: # if not already removed and is substring
#                q[1] = 1  # remove
#    
#    goodkeys = set(x[0] for x in flt if not x[1])
#    
#    found_entities=found_entities[found_entities.entity.isin(goodkeys)]
    
    
    #to check the output
    found_entities[['list','similarity']]
    found_entities[['entity','col_name']]
    
    # sort the list by entities and then by similarity score
    found_entities=found_entities.sort_values(['entity','similarity'], ascending=[True, False]) #similarity descending, entity alphabetical
    
    # make list of sure entities and suggested entities
    sure_entities=found_entities[found_entities.similarity>=sim_cutoff]
    suggested_entities=found_entities[found_entities.similarity<sim_cutoff]
        
    
    # for dates, we need the high similarity finds only. so, just for those find just retain high similarity entities
    idx =  (sure_entities.groupby(['entity'])['similarity'].transform(max) == sure_entities['similarity']) | (sure_entities.col_name.str.lower()!='date') # filter on whole sure entities DF with an or condition to make it work only on dates
    sure_entities=sure_entities[idx]
    
    return sure_entities,suggested_entities
        
            
            
            
            
            
            
            
            
            
