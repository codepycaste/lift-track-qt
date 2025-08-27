from PySide6.QtWidgets import QMainWindow, QComboBox, QHBoxLayout, QVBoxLayout, QToolBar, QTreeWidget, QTableWidget, QTableWidgetItem, QLineEdit, QWidget,QPushButton, QInputDialog
from PySide6.QtCore import Slot, QSize
from workout import Workout
from database import Database as db


#TODO add splash page?

class WorkoutTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Tracker V.0.01')
        self.initUI()
        self.filename = 'data/templates.csv' #
        self.workout = None # temp here?
        
    def initUI(self):
        layout = QHBoxLayout()
        
        central = QWidget()

        #layout history structure here: toolbar options placed at top to do
        left_layout = QVBoxLayout()
        left = QWidget()
        history = QTreeWidget()
        left_toolbar = QToolBar("Workout History Toolbar")
        #left_toolbar.setIconSize(QSize(16,16))
        new_workout = QPushButton("New Workout") 
        new_workout.clicked.connect(self.new_workout_dialogue)
        left_toolbar.addWidget(new_workout)
        self.load_workout = QComboBox(placeholderText="Load Workout") 
        #needs to populate from csv on startup, could limit size and then add..a search widget at bottom
        self.load_workout.activated.connect(self.load_workout_slot)
        #revert to placeholder?
        left_toolbar.addWidget(self.load_workout)
        save_workout = QPushButton("Save Workout")
        save_workout.clicked.connect(self.save_workout_slot)
        left_toolbar.addWidget(save_workout)
        del_workout = QComboBox(placeholderText="Delete Workout")
        left_toolbar.addWidget(del_workout)
        left_layout.addWidget(left_toolbar)
        left_layout.addWidget(history)
        left.setLayout(left_layout)
        history.setColumnCount(4)
        history.setHeaderLabels(["Exercise","Sets","Reps","Weight"])
        
        #layout template/current structure here:
        right_layout = QVBoxLayout()
        right = QWidget()
        self.current = QTableWidget(0,4) #TODO: ALLOW IN TABLE EDITING OF EXERCISE VALS
        self.current.setHorizontalHeaderLabels(["Exercise","Sets","Reps","Weight"])
        right_toolbar = QToolBar("Templates Toolbar")
        #right_toolbar.setIconSize(QSize(16,16))
        
        save_template_button = QPushButton("Save Template") #maybe this should be widget? guess this can define as function later, 2 options?
        save_template_button.clicked.connect(self.save_template_slot)
        self.load_template_button = QComboBox(placeholderText="Load Template")
        self.load_template_button.activated.connect(self.load_template_slot)
        del_template = QComboBox(placeholderText="Delete Template")
        right_toolbar.addWidget(save_template_button)
        right_toolbar.addWidget(self.load_template_button)
        right_toolbar.addWidget(del_template)
        #right_toolbar.insertSeparator(new_template)
        right_layout.addWidget(right_toolbar)
        right_layout.addWidget(self.current)
        #need..4 entry boxes?
        entry = QWidget()
        entry_layout = QHBoxLayout()
        #save_template_button.clicked.connect(self.new_template()) #needs lambda func?

        self.exercise_line = QLineEdit(placeholderText="Enter Exercise Name")
        self.sets_line = QLineEdit(placeholderText="Enter Sets")
        self.reps_line = QLineEdit(placeholderText="Enter Reps")
        self.weight_line = QLineEdit(placeholderText="Enter Weight")
        add_button = QPushButton("Add to Workout")
        add_button.clicked.connect(self.add_exercise_slot)
        entry_layout.addWidget(self.exercise_line)
        entry_layout.addWidget(self.sets_line)
        entry_layout.addWidget(self.reps_line)
        entry_layout.addWidget(self.weight_line)
        entry_layout.addWidget(add_button) #change to icon?
        
        entry.setLayout(entry_layout)
        right_layout.addWidget(entry)
        right.setLayout(right_layout)

        #finishing touches
        layout.addWidget(left)
        layout.addWidget(right)
        central.setLayout(layout)
        self.setCentralWidget(central)

        #new_workout.clicked.connect(self.new_workout())


#input methods for templates/workouts
    @Slot()
    def new_workout_dialogue(self): #takes input string from dialogue box to creat new workout object and display it in template table:
        #create dialogue -> reciecve new workout name -> set new workout name somewhere in tableview?? todo
        self.current.clearContents()
        self.current.setRowCount(0)
        enter_name = QInputDialog(self)
        enter_name.setWindowTitle("Enter a name for this Workout")
        text, ok = enter_name.getText(self, "Workout", "Enter a name for this workout:")
        # creat temp as workout object -> 
        if ok and text: 
           temp = Workout(name= f"{text}")
           print(temp.name) # how will this object persist..
           self.workout = temp
           return 
        #need a condition for cancel button or move exec?
        enter_name.exec()   

    #TODO: display workout name in table slot somehow

    @Slot()
    def save_workout_slot(self) -> None: 
        print(self.workout.name)
        #_data = db()
        db.save_workout(db(),workout=self.workout) #creates a new database obj each time
        self.load_workout.insertItem(0,f"{self.workout.name} : {self.workout.date}")  #this is gonna get toooo long
        #needs to clear the tableview
        self.current.clearContents() #keeps header!s/revert rows count?
        self.current.setRowCount(0)

    @Slot()
    def load_workout_slot(self) -> None: 
        text = self.load_workout.itemText(self.load_workout.currentIndex()) #just text? see below
        #self.load_workout.currentText()
        workout = db.load_workout(db(),text) #returns workout obj
        self.workout = workout
        print("gui",workout) 
        #-> load into tableview
        table = self.current
        print('exercises',workout.exercises.values()) #these are exercise obj need to strip attributes from here:
        for exercise in workout.exercises.values(): #not efficient at all smh nested loops
            table.setRowCount(table.rowCount()+1)
            for i,v in zip(range(4),vars(exercise)):
                val = QTableWidgetItem(getattr(exercise,v)) #
                table.setItem(table.rowCount()-1,i,val)
        #return
        
    @Slot()
    def save_template_slot(self): #saves template to csv under workout name see above, db(filepath) and just remmeber to leave numbers blank?
        db.save_template(db(),workout=self.workout)
        self.load_template_button.insertItem(0,f"{self.workout.name}")
        self.current.clearContents()
        self.current.setRowCount(0)
        
    @Slot()
    def load_template_slot(self): #loads template from csv, options displayed in combobox. displays choice in template table(clear first?)
        text = self.load_template_button.itemText(self.load_template_button.currentIndex())
        template = db.load_template(db(),text) #returns workout object
        table = self.current
        for exercise in template.exercises.values(): #
            table.setRowCount(table.rowCount()+1)
            for i,v in zip(range(4),vars(exercise)):
                val = QTableWidgetItem(getattr(exercise,v))
                table.setItem(table.rowCount()-1,i,val)

    def del_template(): #deletes template from data/templates.csv choices shown in combobox
        pass

    @Slot()
    def add_exercise_slot(self): #adds current strings from lineedits as exercise to current template using add button.clicked, remove row indexes?
        if self.workout:
            table = self.current
            exercise_name = self.exercise_line.text()
            exercise_sets = self.sets_line.text()
            exercise_reps = self.reps_line.text()
            exercise_weight = self.weight_line.text()
            if exercise_name and exercise_sets and exercise_reps and exercise_weight:
                self.workout.add_exercise(exercise_name,exercise_sets,exercise_reps,exercise_weight)
                table.setRowCount(table.rowCount()+1)
                for i, v in enumerate(vars(self.workout.exercises[exercise_name]).values()): #smh theres gotta be a better way...
                    print(i,v)
                    val = QTableWidgetItem(v)
                    table.setItem(table.rowCount()-1,i,val) 
                # add every exercise to table each time or just update table?
            else: #dialogue error
                pass
        else: #dialogue error
            pass
        self.exercise_line.clear()
        self.sets_line.clear()
        self.reps_line.clear()
        self.weight_line.clear()

    def del_exercise(): #way to interact with table directly or does it need a seperate button? maybe smth about set rowcount as well as..workout obj manipulation
        pass


