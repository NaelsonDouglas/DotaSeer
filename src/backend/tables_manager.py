import numpy as np
import pandas as pd
import logging
import pymongo
from context import Context
import json

class Tables:
        def __init__(self):
                self.context  = Context()                
        
        def get_all_matches(self):
                matches_collection = self.context.db['Matches']
                matches_cursor = matches_collection.find({})                
                cursor_list = list(matches_cursor)                
                result = pd.DataFrame(cursor_list)
                result['diff'] = result['radiant_score'] - result['dire_score']
                return result[result.dire_score + result.radiant_score !=0][result.duration > 700][result['diff']>=-40][result['diff']<=40]