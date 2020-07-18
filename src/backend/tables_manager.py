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
                p = list(matches_cursor)
                result = pd.DataFrame(p)
                #result['teams'] = result['teams'].map(lambda x :np.concatenate((x[0],x[1])))
                #result['radiant_win'] = result['radiant_win'] * 1                
                return result               
        