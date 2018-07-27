import pandas as pd
import numpy as np
import nltk
import json
from nltk.stem import PorterStemmer
import re

#declaring a porter stemmer to use in all place. we are stemming the words in dictionary to stems
#to make apples to apples comparision i.e. at root words. 
porter_stemmer=PorterStemmer()

#function to stem sentences at a time as most of the dictionary would be having more than one word
def stem_sentences(sentence):
    sentence=str(sentence)  # to make sure we are converting any IDs or intgers in text to strings as re.split will fail otherwise
    tokens = re.split('\s|/|-',sentence)    #splitting the sentences by space, '/' and '-'. to deal with URLs we included '/' and '-'
    stemmed_tokens = [porter_stemmer.stem(token.lower()) for token in tokens] 
    return ' '.join(stemmed_tokens) #joining back as a sentence

# load of dataset
data=pd.read_excel('digital.xlsx')

#load of date finder keywords file
dates=pd.read_csv('date_dic.csv')


# checking out the columns and replacing spaces with underscore for easy of use
cols=data.columns
data.columns=cols.str.replace(" ","_")
data.head()
typ_list=data.dtypes


#making sure if an id or code column is found they are typecasted as strings and not numbers.
#This is to make them avilable for search by any user as text. they should not be misintepreted as metrics.
for each_col in data.columns:
    if ('_id' in each_col.lower() ) & (('i' in data[each_col].dtype.str) | ('f' in data[each_col].dtype.str)):
        data[each_col]=data[each_col].apply(str)
data.select_dtypes(include=['object']).columns
len(data)
#prod=data['Customer Name'].value_counts()
#prod[prod>10]

# declaring an empty dataframe that we want to write at the end of the program to a text file for use in all other places as dictionary
dic_df=pd.DataFrame(columns=['col_name', 'list', 'stem'])
#dic_df.columns=['col_name', 'list', 'stem']


#adding list of columns as first set of data dictionary
l=list(data.columns) # to fill in the exact data in our data
st=[stem_sentences(item) for item in list(data.columns)] # to store the stems of the exact data
c= ['column']*len(l) #store the count of values in each column, this is useful to know difference between free text and limited list cols
temp_df=pd.DataFrame([c,l,st]).transpose() #transpose to make it in the desired df_dic form
temp_df.columns=dic_df.columns # adding column names, similar to the ones in dic_df, as it would help while appending

dic_df=dic_df.append(temp_df)

# adding date patterns as second set of data dictionary
l=dates['Date'].tolist()
st=[stem_sentences(item) for item in dates['Date'].tolist()]
c= ['date']*len(l)
temp_df=pd.DataFrame([c,l,st]).transpose()
temp_df.columns=dic_df.columns

dic_df=dic_df.append(temp_df)


# adding all columns as subsequent sets to dictionary
for col in data.select_dtypes(include=['object']).columns:
        print (col)
#    if '_id' not in col.lower():
        l=data[col].unique().tolist()
        st=[stem_sentences(item) for item in data[col].unique().tolist()]
        c= [col]*len(l)
        temp_df=pd.DataFrame([c,l,st]).transpose()
        temp_df.columns=dic_df.columns

        dic_df=dic_df.append(temp_df)
        
#print (dic_df)

# write to a csv file for future use. encoded as utf8. 
############## need to be aware about repurcurssions of utf8 encoding######################
dic_df.to_csv('dic_df.csv', encoding='utf8')     


#previous code to write into a dictionary instead of dataframe. dataframe a better solution for search.

#dic['columns']={'list':list(data.columns), 'stem':[stem_sentences(item) for item in list(data.columns)] , 'count':len(data.columns)}
#for col in data.select_dtypes(include=['object']).columns:
#    if '_id' not in col.lower():
#        dic[col]={'list': data[col].unique().tolist(), 'stem':[stem_sentences(item) for item in data[col].unique().tolist()] , 'count': len(data[col].unique())}
#
#
#with open('dic.txt', 'w') as outfile: 
#    json.dump(dic, outfile)
    
