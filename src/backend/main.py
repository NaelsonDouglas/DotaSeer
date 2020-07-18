#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from data_extractor import DataExtractor
from sklearn.metrics import accuracy_score,f1_score,precision_score
from tables_manager import Tables
import logging
from knn import Knn
import pandas as pd

tables_manager = Tables()
knn = Knn(7)