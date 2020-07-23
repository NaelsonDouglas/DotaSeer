from api import OpenDota, Steam
import logging
from context import Context
from configure_logging import configure_logging
configure_logging('main.py', logging.INFO)

class DataExtractor:
        def __init__(self):
                self.open_dota = OpenDota()
                self.steam = Steam()
                self.context = Context()

        def import_matches(self,amount):
                matches = self.open_dota.get_matches(amount)
                match_collection = self.context.db.get_collection('Matches')
                for match in matches:
                        if match_collection.count_documents({ '_id': match['match_id'] }, limit = 1) == 0:                                
                                logging.info('Inserting match '+str(match['match_id'])+' on database.')
                                match['_id'] = match['match_id']
                                match.pop('match_id')
                                self.context.insert_one(match,'Matches')
                        else:
                                logging.warn('Match '+str(match)+' already on database.')