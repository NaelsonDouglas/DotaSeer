#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from configs import Configs
from context import Context
from api import OpenDota, Steam
import logging
from configure_logging import configure_logging
configure_logging('main.py', logging.INFO)

configs = Configs()
context = Context()
steam = Steam()
open_dota = OpenDota()

match_ids = open_dota.get_matches_ids(1000)

match_collection = context.db.get_collection('Matches')
for match_id in match_ids:        
        if match_collection.count_documents({ 'match_id': match_id }, limit = 1) == 0:
                logging.debug('Accessing Steam to get info about match '+str(match_id))
                splited_match = steam.get_match_detail(match_id)
                if splited_match != None:
                        for sp in splited_match:
                                logging.info('Match '+str(sp['match_id'])+' being inserted on database')
                                context.insert_one(sp,'Matches')
        else:
                logging.warn('Match '+str(match_id)+' already on database.')