import pandas as pd

def remove_unhelpful(data):
    '''
    Removes all columns of a dataframe which only ever have 1 value or no value
    '''
    
    #variables to be kept
    goodvariables = []
    
    #loops through all values to check that they have more than 1 value
    for col in data.columns:
        
        #set of values in a given column
        colset = set(list(data[col]))
        
        #check for more than 1 value while taking error value into account (ATM error = -1) and values having too few iterations into account
        
        remvals = set()
        for value in colset:
            if(value == -1 or len(data[col]) < 2):
                remvals.add(value)
        colset.difference(remvals)
        
        if(len(colset) > 3):
            goodvariables.append(col)
        
    return data[goodvariables]