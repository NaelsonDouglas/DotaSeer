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
                match_ids = self.open_dota.get_matches_ids(amount)
                match_collection = self.context.db.get_collection('Matches')
                for match_id in match_ids:
                        if match_collection.count_documents({ '_id': match_id }, limit = 1) == 0:
                                logging.debug('Accessing Steam to get info about match '+str(match_id))
                                splited_match = self.steam.get_match_detail(match_id)                
                                if splited_match != None:
                                        logging.info('Inserting match '+str(splited_match['_id'])+' on database.')
                                        self.context.insert_one(splited_match,'Matches')
                        else:
                                logging.warn('Match '+str(match_id)+' already on database.')