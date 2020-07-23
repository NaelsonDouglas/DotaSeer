from tables_manager import Tables
from classifier import Classifier
from sklearn.ensemble import RandomForestRegressor

class RandomForest(Classifier):
        def __init__(self):
                super().__init__(True)
                #self.y_test = self.y_test
                #self.y_train = self.y_train
                self.classifier = RandomForestRegressor(max_depth=2, random_state=0)                
                self.train()                
                self.results()
        
        def print_results(self):
                print('=====================')
                print('Algorithm: random-forest')
                #print('K= '+str(self.k))                
                super().print_results()
                