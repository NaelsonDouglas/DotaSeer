import requests
from configs import Configs
from utils import prune_json
import logging
import json
from configure_logging import configure_logging
configure_logging('api.py')
class Api:        
        def __init__(self,api_base_url):                
                from configs import Configs                
                self.configs = Configs()
                self.api_base_url = self.configs.get(api_base_url)

        def get(self,resource, payload='') -> dict:
                uri = self.api_base_url+resource                
                result = requests.get(uri,params=payload)
                logging.debug(result)
                result = result.json()                
                return result

class Steam(Api):
        def __init__(self,api_base_url='steamBaseUrl'):
                Api.__init__(self,api_base_url)
                self.api_base_url = self.configs.get(api_base_url)
        
        def get_match_detail(self,match_id=5508855507):
                logging.debug('Fetching the match which match_id= '+str(match_id))
                RADIANT = 0
                DIRE = 1
                payload = {'match_id':match_id, 'KEY':self.configs.get('steamApiKey')}
                result = []
                dire_result = {'match_id':match_id,'team':'dire'}
                radiant_result = {'match_id':match_id,'team':'radiant'}
                
                response = self.get('/GetMatchDetails/V001/',payload=payload)
                matches = response['result']
                logging.debug(matches)
                #logging.warn(matches.keys())

                radiant_win = matches['radiant_win']
                radiant_result['win'] = radiant_win
                dire_result['win'] = not radiant_win
                dire_heroes = []
                radiant_heroes = []
                #print(json.dumps(matches, indent = 4))
                try: #For some reason, some matches don't have the pick_bans fields
                        picks_bans = matches['picks_bans']
                        logging.debug(matches.keys())
                except:                        
                        logging.warn('Match '+str(match_id)+' does not have the field picks_bans. Skiping it\n')
                        return None
                
                for hero in picks_bans:
                        if hero['is_pick']:
                                if hero['team'] == RADIANT:
                                        radiant_heroes.append(hero['hero_id'])
                                elif hero['team'] == DIRE:
                                        dire_heroes.append(hero['hero_id'])
                radiant_result['composition'] = radiant_heroes
                dire_result['composition'] = dire_heroes                
                result.append(radiant_result)
                result.append(dire_result)                
                return result

class OpenDota(Api):
        def __init__(self):                
                Api.__init__(self,'openDotaApiBaseUrl')
                self.steam_api_key = self.configs.get('steamApiKey')                
        
        def get_heroes(self,selected_keys = ('id', 'img', 'icon','localized_name')) -> list:
                heroes =  self.get('/heroStats')
                prunned_heroes = []
                for hero in heroes:
                        prunned_heroes.append(prune_json(hero,selected_keys))
                return prunned_heroes

        def get_matches_details(self,less_than_match_id=5508335915) -> list:
                matches =  self.get('/publicMatches', payload={'less_than_match_id':less_than_match_id})
                unitary_matches = []
                min_match_id = 999999999999999999
                for match in matches:
                        split_match = self.split_match(match,min_match_id)
                        if split_match['min_match_id'] < min_match_id:
                                min_match_id = split_match['min_match_id']
                        for m in split_match['unitary_matches']:
                                unitary_matches.append(m)
                result = {'unitary_matches':unitary_matches,'min_match_id':min_match_id}
                return result

        def get_matches_ids(self,amount=100):        
                query = self.get_sql_query(amount)        
                response = self.get('/explorer'+query)['rows']
                result = []
                for match in response:
                        result.append(match['match_id'])
                return result

        def get_sql_query(self, amount,origin='public_matches',fields='match_id',order_by='start_time'):
                query = '?sql=select {} from {} where num_mmr > 0 order by {} desc limit {}'.format(fields,origin,order_by,str(amount))
                query = query.replace(' ','%20')                
                return query
        
        def split_match(self, match, min_match_id):
                unitary_matches = []
                match_id = match['match_id']
                if match_id < min_match_id:
                        min_match_id = match_id
                radiant_match = {'match_id':match_id,'team':'radiant'}
                dire_match = {'match_id':match_id,'team':'dire'}
                if match['radiant_win']:
                        radiant_match['win'] = True
                        dire_match['win'] = False
                else:
                        radiant_match['win'] = False
                        dire_match['win'] = True
                radiant_match['composition'] = match['radiant_team'].split(',')
                dire_match['composition'] = match['dire_team'].split(',')
                radiant_match['composition'] = list(map(int,radiant_match['composition']))
                dire_match['composition'] = list(map(int,dire_match['composition']))
                unitary_matches.append(radiant_match)
                unitary_matches.append(dire_match)                
                result = { 'unitary_matches':unitary_matches,'min_match_id':min_match_id}
                return result