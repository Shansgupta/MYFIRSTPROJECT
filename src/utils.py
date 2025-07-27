## Contain the common functionality from which the entire project can use 


import os
import sys
import numpy as np
from src.exception import CustomException
import pandas as pd
import dill  ## actually help to create the pickle file 
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path,obj):
    try :
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = True)
        with open (file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e :
        raise CustomException(e,sys)
    

def evaluate_models(X_train,y_train,X_test,y_test,models,params):

    try :
      
      report = {} 

      for i in range(len(list(models))):
        model = list(models.values())[i]

        ## model.fit(X_train, y_train) # Train model
        para=params[list(models.keys())[i]]
        gs = GridSearchCV(model,para,cv=3)
        gs.fit(X_train,y_train)

        model.set_params(gs.best_params_)  ## applies best parameter to the original model
        model.fit(X_train,y_train)

                  # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    
                   # Evaluate Train and Test dataset
        train_model_score  = r2_score (y_train, y_train_pred)

        test_model_score =  r2_score (y_test, y_test_pred)
        
        report[list(models.keys())[i]] = test_model_score

        return report 
    
    except Exception as e :
      raise CustomException(e,sys)
     
def load_object(file_path):
   try:
      with open (file_path,"rb") as file_obj:
        return dill.load(file_obj)
       
   except Exception as e :
      raise CustomException(e,sys)     
   
   
   ## print(list(models.keys())[i])
    ## model_list.append(list(models.keys())[i])    

