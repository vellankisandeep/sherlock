# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 18:23:51 2018

@author: svellanki
"""

import pandas as pd

data=pd.read_excel('Sample - Superstore.xls')

cols=data.columns
data.columns=cols.str.replace(" ","_")
data.head()
data.dtypes
data.select_dtypes(include=['object']).columns
len(data)
#prod=data['Customer Name'].value_counts()
prod[prod>10]

dic={}
for col in data.select_dtypes(include=['object']).columns:
    if '_id' not in col.lower():
        dic[col]={'list': data[col].unique().tolist(), 'count': len(data[col].unique())}


'Texas' in dic['State']['list']

search_term='texas'

search_term_itr=search_term.strip().split()

ite=dic.items()
all_found=[]
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
        all_found.append([needed_set, key_iden])
print (all_found)    
    
        