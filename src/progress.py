import matplotlib.pyplot as plt
import pandas as pd

class ProgressChart:
    def __init__(self,data):
        self.data = data

    def plot_progress(self):
        plt.plot(self.data['Date'],self.data['Weight'])
        plt.title('Workout Progress')
        plt.xlabel('Date')
        plt.ylabel('Rep Weight')
        plt.show()
        