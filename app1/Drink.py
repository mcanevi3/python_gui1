from Database import *

class Drink:
    amount:int
    brand:str
    name:str
    caffein:int
    calories:int
    portions:list

    def __init__(self):
        self.amount=200
        self.brand=""
        self.name="Water"
        self.caffein=0
        self.calories=0
        self.portions=[1,10,100,200,330,500,1000,1500,2500]
    
    def dict(self):
        return dict(amount=self.amount,brand=self.brand,name=self.name,caffein=self.caffein,calories=self.calories,portions=self.portions)
    
    def print(self):
        print(self.dict())

class DrinkDB:
    drink=None
    def __init__(self,file_name:str):
        self.db=Database(file_name)
    def set_drink(self,drink:Drink):
        self.drink=drink
    def set_db(self,db:Database):
        self.db=db
    def create_table(self):
        self.db.create_table("drink",names=["amount","brand","name","caffein","calories","portions"],types=[int,str,str,int,int,str])
    def load(self):
        pass
    def save(self):
        # drink to database
        d=self.drink
        db=self.db
        self.create_table()

        




db=Database("drink1.sqlite")
bridge=DrinkDB(db,Drink())

