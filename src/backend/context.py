import logging
from configure_logging import configure_logging
configure_logging('main.py')
class Context:    
    def __init__(self):        
        from pymongo import MongoClient, ASCENDING, DESCENDING
        from configs import Configs
        import json
        configs = Configs()
        self.client = MongoClient(configs.get('databaseIP'), configs.get('databasePort'))
        self.db = self.client['DotaSeer']

        self.matches = self.db['Matches'].create_index([('match_id',DESCENDING), ('team', ASCENDING)], unique = True)
        self.heroes = self.db['Heroes'].create_index('id')
        
    def insert_one(self, data, subcollection):        
        self.db[subcollection].insert_one(data)

    def store_heroes(self):        
        from api import OpenDota
        api = OpenDota()        
        heroes = api.get_heroes()        
        for hero in heroes:            
            self.insert_one(hero,'Heroes')