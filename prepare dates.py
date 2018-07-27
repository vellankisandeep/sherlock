# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 18:41:26 2018

@author: svellanki
"""
import preparing_entities
import datetime

text='show me visits for 3d opportunity for march of last year'

entities, suggestions=preparing_entities.get_entities(text)

def date_find(date_entities):
    now = datetime.datetime.now()
    to_year, to_month, to_day, to_hour, to_minute, to_second= now.year, now.month, now.day, now.hour, now.minute, now.second
    from_year, from_month, from_day, from_hour, from_minute, from_second= now.year, now.month, now.day, now.hour, now.minute, now.second

    


