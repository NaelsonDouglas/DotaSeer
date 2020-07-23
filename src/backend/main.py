#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from data_extractor import DataExtractor
from sklearn.metrics import accuracy_score,f1_score,precision_score
from tables_manager import Tables
import logging
from knn import Knn
from random_forest import RandomForest
import pandas as pd

#tables_manager = Tables()
#print(tables_manager.get_all_matches())
#knn = Knn(7)
random_forest = RandomForest()