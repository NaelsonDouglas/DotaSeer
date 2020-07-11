import requests
from utils import prune_json
class Api:
        import requests
        def __init__(self):                
                from configs import Configs
                configs = Configs()
                self.api_base_url = configs.get('apiBaseUrl')

        def get(self,resource, payload='') -> list:
                uri = self.api_base_url+resource
                result = requests.get(uri,params=payload)                
                return result.json()
        
        def get_heroes(self,selected_keys = ('id', 'img', 'icon','localized_name')):
                heroes =  self.get('/heroStats')                
                prunned_heroes = []
                for hero in heroes:
                        prunned_heroes.append(prune_json(hero,selected_keys))
                return prunned_heroes

                
        
