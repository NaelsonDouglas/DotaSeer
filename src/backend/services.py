#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from configs import Configs
from context import Context
from api import Api
configs = Configs()
context = Context()
api = Api()


for p in api.get_match_details():
        print(p)
#context.store_heroes()
#data = {'match_id':'1', 'team': 'B'}
#data = {'match_id':'1', 'team': 'C'}
#context.insert_one(data,'Matches')      


