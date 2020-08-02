from tables_manager import Tables
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import logging
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



class Classifier:
        def __init__(self,is_dummy):
                self.tables_manager = Tables()
                self.data = self.tables_manager.get_all_matches().dropna()
                #self.data = self.tables_manager.get_all_matches().dropna()
                self.data['radiant_win'] *= 1
                logging.info(self.data.head())                
                self.x = self.data[['radiant_score', 'dire_score','duration']].values
                self.y = self.data[['radiant_win']].values
                logging.info(self.x)
                logging.info(self.y)
                self.test_size=0.3
                self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=self.test_size)
                self.classifier = None #To be filled by child class.

        def plot3D(self):                
                win = self.data[self.data.radiant_win == 1]
                loss = self.data[self.data.radiant_win == 0]                
                plot3D = plt.figure().gca(projection='3d')
                plot3D.scatter(win['radiant_score'], win['dire_score'], win['duration'],color='green',marker='<',alpha=0.5)
                plot3D.scatter(loss['radiant_score'], loss['dire_score'], loss['duration'],color='red',marker='>',alpha=0.5)
                
                plot3D.set_xlabel('radiant_score')
                plot3D.set_ylabel('dire_score')
                plot3D.set_zlabel('duration')
                plt.show()
        
        def plot2D(self,x=-1,y=-1,winner=''):
                self.data['diff'] = self.data['radiant_score'] - self.data['dire_score']
                plt.figure(figsize=(20,6))
                plt.grid(axis='both', alpha=0.2)                

                plt.scatter(self.data[self.data.radiant_win == 0]['diff'],self.data[self.data.radiant_win == 0]['duration'],marker='<',facecolor='none', edgecolors='r', alpha=0.7, label='Dire wins')                
                plt.scatter(self.data[self.data.radiant_win == 1]['diff'],self.data[self.data.radiant_win == 1]['duration'],marker='>',facecolor='none',edgecolors='g', alpha=0.3, label='Radiant wins')                
                                
                plt.xlabel('radiant_score - dire_score')
                plt.ylabel('match duration (s)')
                
                if x!=-1 or y!= -1:
                        plt.axvline(x=x,alpha=0.5)                        
                        plt.axhline(y=y,alpha=0.5)
                        plt.scatter(x,y,marker='x',facecolor='black',edgecolors='black', alpha=1,label='User data'+'('+str(x)+','+str(y)+')')
                        plt.annotate('y='+str(y), 
                                                        xy=(45, 40), 
                                                        xytext=(45,y), 
                                                        arrowprops = dict(facecolor=None, shrink=0.05))
                        if winner.find('Dire') == -1:
                                plt.title(winner,fontdict={'color':'green'})
                        else:
                                plt.title(winner,fontdict={'color':'red'})
                        plt.legend()
                        plt.savefig('../frontend/src/data.png')
                else:
                        plt.show()
                
                
        def train(self):
                self.classifier.fit(self.x_train, self.y_train.ravel())
        
        def predict(self,user_input):
                return self.classifier.predict(user_input)
        
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