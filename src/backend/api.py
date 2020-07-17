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
                        if hero['is_pick']:                                
                                if hero['team'] == RADIANT:
                                        radiant_heroes.append(hero['hero_id'])
                                elif hero['team'] == DIRE:
                                        dire_heroes.append(hero['hero_id'])
                if (len(radiant_heroes) != 5 and len(dire_heroes) != 5):
                        logging.warn('Match '+str(match_id)+' has unbalanced number of picks. Skiping it\n')
                        return None
                
                radiant_heroes.sort()
                dire_heroes.sort()
                result['teams'] = [radiant_heroes, dire_heroes]
                # result['radiant_heroes'] = radiant_heroes          
                # result['dire_heroes'] = dire_heroes                
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
                #query = '?sql=SELECT%0A%20%20%20%20%20%20%20%20%0Amatches.match_id%0AFROM%20matches%0AJOIN%20match_patch%20using(match_id)%0AWHERE%20TRUE%0AAND%20matches.start_time%20>%3D%20extract(epoch%20from%20timestamp%20%272017-09-01T03%3A00%3A00.000Z%27)%0AAND%20matches.start_time%20<%3D%20extract(epoch%20from%20timestamp%20%272020-06-30T03%3A00%3A00.000Z%27)%0AORDER%20BY%20matches.match_id%20NULLS%20LAST%0ALIMIT%20200'
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