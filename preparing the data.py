import pandas as pd
import nltk
import json
from nltk.stem import PorterStemmer

porter_stemmer=PorterStemmer()

def stem_sentences(sentence):
    tokens = sentence.split()
    stemmed_tokens = [porter_stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)

data=pd.read_excel('Sample - Superstore.xls')

cols=data.columns
data.columns=cols.str.replace(" ","_")
data.head()
data.dtypes
data.select_dtypes(include=['object']).columns
len(data)
#prod=data['Customer Name'].value_counts()
#prod[prod>10]

dic={}

dic_df=pd.DataFrame(columns=['col_name', 'list', 'stem'])
#dic_df.columns=['col_name', 'list', 'stem']

l=list(data.columns)
st=[stem_sentences(item) for item in list(data.columns)]
c= ['column']*len(l)
temp_df=pd.DataFrame([c,l,st]).transpose()
temp_df.columns=dic_df.columns

dic_df=dic_df.append(temp_df)

for col in data.select_dtypes(include=['object']).columns:
    if '_id' not in col.lower():
        l=data[col].unique().tolist()
        st=[stem_sentences(item) for item in data[col].unique().tolist()]
        c= [col]*len(l)
        temp_df=pd.DataFrame([c,l,st]).transpose()
        temp_df.columns=dic_df.columns

        dic_df=dic_df.append(temp_df)
        
print (dic_df)
        


#dic['columns']={'list':list(data.columns), 'stem':[stem_sentences(item) for item in list(data.columns)] , 'count':len(data.columns)}
#for col in data.select_dtypes(include=['object']).columns:
#    if '_id' not in col.lower():
#        dic[col]={'list': data[col].unique().tolist(), 'stem':[stem_sentences(item) for item in data[col].unique().tolist()] , 'count': len(data[col].unique())}
#
#
#with open('dic.txt', 'w') as outfile: 
#    json.dump(dic, outfile)
    
