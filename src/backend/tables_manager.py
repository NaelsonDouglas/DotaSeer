import numpy as np
import pandas as pd
import logging
import pymongo
from context import Context
import json

class Tables:
        def __init__(self,is_dummy = False):
                self.context  = Context()
                self.dummy = is_dummy
        
        def get_all_matches(self):
                matches_collection = self.context.db['Matches']
                matches_cursor = matches_collection.find({})                
                cursor_list = list(matches_cursor)
                result = None
                if self.dummy:
                        dummy_cursor = []
                        heroes_range = ['_id', 'win']
                        heroes_range = heroes_range+list(range(1,130))
                        for match in cursor_list:                                
                                radiant_row = dict.fromkeys(heroes_range,0)
                                dire_row = dict.fromkeys(heroes_range,0)
                                radiant_row['_id'] = match['_id']
                                dire_row['_id'] = match['_id']                                
                                for r in  ['R1','R2','R3','R4','R5']:                                       
                                        radiant_row[match[r]] = 1                                        
                                        radiant_row['win'] = match['radiant_win']
                                for d in  ['D1','D2','D3','D4','D5']:
                                        dire_row[match[d]] = 1
                                        dire_row['win'] = not match['radiant_win']
                                dummy_cursor.append(dire_row)
                                dummy_cursor.append(radiant_row)
                        result = pd.DataFrame(dummy_cursor)
                else:
                        result = pd.DataFrame(cursor_list)
                #result['teams'] = result['teams'].map(lambda x :np.concatenate((x[0],x[1])))
                #result['radiant_win'] = result['radiant_win'] * 1                
                return result               
        