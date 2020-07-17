#https://stackoverflow.com/questions/48109956/unable-to-install-any-package-through-pip
from data_extractor import DataExtractor
from tables_manager import Tables
from knn import Knn

tables_manager = Tables()
knn = Knn()

data_extractor = DataExtractor()
data_extractor.import_matches(10000)

data = tables_manager.get_all_matches()

#knn.train(data)