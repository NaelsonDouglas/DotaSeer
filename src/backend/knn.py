from tables_manager import Tables
from classifier import Classifier
from sklearn.neighbors import KNeighborsClassifier

class Knn(Classifier):
        def __init__(self,k):
                super().__init__(False)
                self.k = k
                self.classifier = KNeighborsClassifier(n_neighbors=self.k)
                self.train()
                self.results()
                self.dummy = True
        
        def set_k(self, k):
                self.k = k
                self.classifier.set_params(n_neighbors=k)
        
        def print_results(self):
                print('=====================')
                print('Algorithm: knn')
                print('K= '+str(self.k))                
                super().print_results()
                