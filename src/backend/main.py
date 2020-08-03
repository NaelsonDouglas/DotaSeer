#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from data_extractor import DataExtractor
from sklearn.metrics import accuracy_score,f1_score,precision_score
from tables_manager import Tables
import logging
from knn import Knn
from api import OpenDota
from data_extractor import DataExtractor
#from random_forest import RandomForest
import pandas as pd
from public_api import PublicApi



#random_forest = RandomForest()
#data_extractor = DataExtractor()
#data_extractor.import_matches(1000000)
#api = OpenDota()
#api.get_matches()
#tables_manager = Tables()
#print(tables_manager.get_all_matches())


knn = Knn(7)


#user_input = [[2,2,300]]
#print(knn.predict(user_input))
public_api = PublicApi()
public_api.start()

