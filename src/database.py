import csv 
import os
from workout import Workout, Exercise

class Database: #ok no pandas here, csv? or another database format
    def __init__(self, filename = 'data/tests.csv'):                      #'data/workouts.csv'):
        self.filename = filename
#        self.data = None
        
 #   def get_data(self,filename):
  #      pass

            

    def save_workout(self, workout: Workout) -> None: 
        exercises = ",".join([f'{exercise}' for exercise in workout.exercises.values()])
        new_row = {'Workout': workout.name,
                   'Date': workout.date, 
                   'Exercises': exercises}
        print("new_row",new_row)
        with open(f'{self.filename}','a',newline='') as csvfile:
            fieldnames = ['Workout','Date','Exercises']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) #writer?
            writer.writerow(new_row)

    def load_workout(self, text: str) -> Workout:
        with open(f'{self.filename}', newline='') as csvfile:
            reader = csv.reader(csvfile) 
            workout = text.split(" : ")
            for row in reader:
                print("db",workout)
                print("row",row)
                if row[0] == workout[0] and row[1] == workout[1]: #this order could change? gui save button?
                    print(row)
                # -> return workout object to GUI
                    name = row[0]
                    date = row[1] #k but just remember this is a str not datetime.date 
                    exercises = {} #convert str in row 2 to exercise obj and append hereeeeeeee
                    for exercise in row[2].split(","):
                        x = exercise[:exercise.index(':')]
                        nums = []
                        digit = '' 
                        for char in exercise[exercise.index(':'):]:
                            if char.isdigit():
                                digit += char
                            if not char.isdigit() and digit:
                                nums.append(digit)
                                digit = ''
                        nums.append(digit) 
                        # yeah ofc theyre in the wrong order
                        exercises[x] = Exercise(x,nums[2],nums[1],nums[0])
                    return Workout(name,date,exercises)
                    
    
    def del_workout(self, workout:Workout) -> None: #TODO
        pass

    def save_template(self, workout: Workout) -> None: #TODO: raise exception for same named templates
        exercises = ",".join(exercise.name for exercise in workout.exercises.values())
        new_row = workout.name,exercises
        print("temp:",new_row)
        self.filename = "data/templates.csv"
        with open(f'{self.filename}','a',newline='') as csvfile: #dont think db needs to be an object really
            writer = csv.writer(csvfile)
            writer.writerow(new_row)

    def load_template(self,text: str) -> Workout: #TODO: CLEAR TABLE WHEN LOAD, SET WORKOUT VALS TO 0>> MAYBE NOT HERE?
        self.filename = 'data/templates.csv'
        with open(f"{self.filename}",newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print("temp",row)
                if row[0] == text:
                    exercises = {}
                    for exercise in row[1].split(","): #can this become a dictionary comprehension
                        exercises[exercise] = Exercise(name=f"{exercise}")
                    print(f"{text}",exercises)
                    return Workout(f"{text}",exercises=exercises)

            
    def del_template(self, workout:Workout) -> None: #TODO
        pass
