"""
this module contains class methods and constructers about workout types
in addition to the main method of the program to launch the gui
"""

import datetime
import pandas as pd
import os


class Workout(object):

    """ 
    a class to keep track of lifting workouts
    [exercise_name, no_of_sets, reps per set, weight per rep]  

    """
    def __init__(self, name:str = "",date = datetime.date.today(),exercises:dict={}): 

        self.name = name
        self.date = f'{date}'
        self.exercises = exercises # Dictionary maps exercise names to exercise objects within a specific instance of workout class 


    #issue here: unable to determine how to dynamically assign variable name to instances of exercise class,
    #workaround: either use exec()/eval() function or instantiate a dictionary of known exercises? 
    # Fix: uses dictionary

    def add_exercise(self,name,sets,reps,weight) -> None: 
        self.exercises[name] = Exercise(name,sets,reps,weight)  

    def get_exercises(self) -> dict:
        return self.exercises

    def clear_exercises(self) -> None:
        self.exercises.clear()
    
    def del_exercise(self,name:str) -> None:
        del(self.exercises[name]) #hope thats the right function

    def save_template(self,filename) -> None: #saves to db for later reference
        data = {'Date':[self.date],'Exercises': [(k,v) for k,v in self.exercises]}
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', header= not os.path.exists(filename), index=False)

    def load_template(self,filename) -> None:
        pass

    def show_workout(self): ## maybe for save_template
        pass

class Exercise(object):

    def __init__(self,name="",sets=0,reps=0,weight=0):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name
        
    def set_sets(self,sets: int):
        self.sets = sets

    def get_sets(self) -> int:
        return self.sets

    def set_reps(self, reps: int):
        self.reps = reps
            
    def get_reps(self) -> int:
        return self.reps

    def set_weight(self, weight: int):
        self.weight = weight

    def get_weight(self) -> int:
        return self.weight 
    
    def __str__(self):
        return f'{self.get_name()}: {self.get_weight()}kg {self.get_reps()}x{self.get_sets()}'