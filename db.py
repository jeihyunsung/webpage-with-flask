import pandas as pd
import os.path

class Database:
    def __init__(self):
        if os.path.isfile('Database.csv'):
            self.openDB()
        else:
            self.db = pd.DataFrame({})

    def openDB(self):
        self.db = pd.read_csv('Database.csv', index_col=0)

    def saveDB(self):
        self.db.to_csv("Database.csv")

    def getID(self, id):
        if id in self.db.keys():
            str_data = self.db[id]
        else:
            str_data = ['','']
        
        return str_data[0], str_data[1]
    
    def deleteID(self, id):
        if id in self.db:
            self.db.drop(id, axis=1, inplace=True)
            self.saveDB()
        else:
            return
    
    def saveID(self, id, data):
        self.db[id] = data
        self.saveDB()

    def updateID(self, id, data):
        self.db[id] = data
        self.saveDB()



    

