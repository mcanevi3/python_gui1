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
    table_name="drink"
    def __init__(self,file_name:str):
        self.db=Database(file_name)
        self.drink=Drink()
    def set_drink(self,drink:Drink):
        self.drink=drink
    def set_db(self,db:Database):
        self.db=db
    def create_table(self):
        self.db.create_table(self.table_name,names=["amount","brand","name","caffein","calories","portions"],types=[int,str,str,int,int,str])
    def load(self):
        pass
    def save(self):
        # drink to database
        d=self.drink
        db=self.db
        if not db.has_table(self.table_name):
            self.create_table()
        # search for this one
        res=db.select(self.table_name,["name","brand"],[d.name,d.brand])
        if len(res)==0:
            # insert this
            d.print()
            portions_str=[str(v) for v in d.portions]
            db.insert(self.table_name,["amount","brand","name","caffein","calories","portions"],[d.amount,d.brand,d.name,d.caffein,d.calories,",".join(portions_str)])
        elif len(res)==1:
            # need to update
            d.print()
            pass
        else:
            # something went wrong
            pass

        
if __name__=="__main__":
    bridge=DrinkDB("drink1.sqlite")
    bridge.save()
