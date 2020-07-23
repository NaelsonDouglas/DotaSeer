from tables_manager import Tables
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import logging
import pandas as pd

class Classifier:
        def __init__(self,is_dummy):
                self.tables_manager = Tables()
                self.data = self.tables_manager.get_all_matches().dropna()
                logging.info(self.data.head())                
                self.x = self.data[['radiant_score', 'dire_score','duration']].values
                self.y = self.data[['radiant_win']].values
                logging.info(self.x)
                logging.info(self.y)
                self.test_size=0.3
                self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=self.test_size)
                self.classifier = None #To be filled by child class.
                
        def train(self):
                self.classifier.fit(self.x_train, self.y_train.ravel())
        
        def results(self):                
                self.result = self.classifier.predict(self.x_test)                
                self.confusion_matrix = pd.crosstab(self.y_test.ravel(),self.result, rownames=['Real'], colnames=['Predito'], margins=True)
                print(self.confusion_matrix)                
                self.fscore = f1_score(self.y_test.ravel(),self.result,average='macro')
                self.overview = {'F-score': self.fscore, 'Confusion-matrix': self.confusion_matrix}                                
                self.print_results()
                return self.overview
        
        def print_results(self):    
                print('Dataset size: '+str(len(self.data.index)))
                print('Training percentage: '+str(100*self.test_size)+"%")            
                print('_____________________')                
                print('Confusion-matrix: \n'+str(self.overview['Confusion-matrix']))
                print('_____________________')
                print('F-score: '+str(self.overview['F-score']))
                print('_____________________')
                print('=====================')