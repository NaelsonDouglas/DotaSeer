import requests
from utils import prune_json
class Api:
        import requests
        def __init__(self):
                from configs import Configs
                configs = Configs()
                self.open_dota_api_base_url = configs.get('openDotaApiBaseUrl')
                self.steam_api_base_url = configs.get('steamBaseUrl')
                self.steam_api_key = configs.get('steamApiKey')

        def get(self,resource, api_base_url, payload='') -> list:
                uri = api_base_url+resource
                result = requests.get(uri,params=payload)
                return result.json()

        def get_open_dota(self,resource,payload=''):
                url = self.open_dota_api_base_url                
                return self.get(resource,url,payload=payload)

        def get_steam(self,resource,payload='') -> list:
                url = self.open_dota_api_base_url
                payload['KEY'] = self.steam_api_key
                return self.get(resource,url,payload=payload)

        def get_heroes(self,selected_keys = ('id', 'img', 'icon','localized_name')) -> list:
                heroes =  self.get_open_dota('/heroStats')
                prunned_heroes = []
                for hero in heroes:
                        prunned_heroes.append(prune_json(hero,selected_keys))
                return prunned_heroes

        def get_match_details(self) -> list:
                matches =  self.get_open_dota('/publicMatches')                
                unitary_matches = []
                for match in matches:
                        radiant_match = {'team':'radiand'}
                        dire_match = {'team':'dire'}
                        if match['radiant_win']:
                                radiant_match['win'] = True
                                dire_match['win'] = False
                        else:
                                radiant_match['win'] = False
                                dire_match['win'] = True
                        radiant_match['composition'] = match['radiant_team'].split(',')
                        dire_match['composition'] = match['dire_team'].split(',')
                        unitary_matches.append(radiant_match)
                        unitary_matches.append(dire_match)
                return unitary_matches