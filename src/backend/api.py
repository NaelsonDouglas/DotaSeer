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
                result = result.json()                
                logging.debug(result)
                return result

class Steam(Api):
        def __init__(self,api_base_url='steamBaseUrl'):
                Api.__init__(self,api_base_url)
                self.api_base_url = self.configs.get(api_base_url)
        
        def get_match_detail(self,match_id): #=5508855507
                logging.debug('Fetching the match which match_id= '+str(match_id))
                RADIANT = 0
                DIRE = 1
                payload = {'match_id':match_id, 'KEY':self.configs.get('steamApiKey')}
                result = {'_id':match_id}                
                
                response = self.get('/GetMatchDetails/V001/',payload=payload)                
                matches = response['result']
                logging.debug(matches)
                
                if matches['radiant_win']:
                        result['radiant_win'] = True
                else:
                        result['radiant_win'] = False

                try: #For some reason, some matches don't have the pick_bans fields
                        picks_bans = matches['picks_bans']                        
                except:                        
                        logging.warn('Match '+str(match_id)+' does not have the field picks_bans. Skiping it\n')
                        return None
                
                dire_heroes = []
                radiant_heroes = []
                for hero in picks_bans:
                        if hero['is_pick'] and hero['hero_id'] != None:
                                if hero['team'] == RADIANT:
                                        radiant_heroes.append(hero['hero_id'])
                                elif hero['team'] == DIRE:
                                        dire_heroes.append(hero['hero_id'])
                if (len(radiant_heroes) != 5 and len(dire_heroes) != 5):
                        logging.warn('Match '+str(match_id)+' has unbalanced number of picks. Skiping it\n')
                        return None
                
                radiant_heroes.sort()
                dire_heroes.sort()
                # result['teams'] = [radiant_heroes, dire_heroes]
                #for suffix in ['-1', '-2','-3','-4','-5']:
                if (len(radiant_heroes) == 5 and len(dire_heroes) == 5):
                        for radiant_suffix in range(1,len(radiant_heroes)+1):
                                result['R'+str(radiant_suffix)] = radiant_heroes[radiant_suffix-1]
                        for dire_suffix in range(1,len(dire_heroes)+1):
                                result['D'+str(dire_suffix)] = dire_heroes[dire_suffix-1]                
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
        

        def get_matches(self,amount=1000):        
                query = self.get_sql_query(amount)        
                response = self.get('/explorer'+query)['rows']                
                return response

        def get_sql_query(self, amount,origin='matches',duration=3000,fields='match_id, radiant_score, dire_score, radiant_win, duration',order_by='start_time'):
                #query = '?sql=select {} from {} where num_mmr > 0 order by {} desc limit {}'.format(fields,origin,order_by,str(amount))                
                query = '?sql=select {} from {} WHERE duration>{} order by {} desc limit {}'.format(fields,origin,duration,order_by,str(amount))
                query = query.replace(' ','%20')                
                return query
        