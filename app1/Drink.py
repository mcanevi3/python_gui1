from Database import *

class Drink:
    amount:int
    brand:str
    name:str
    caffein:int
    calories:int
    portions:list

    def __init__(self,*arg):
        if len(arg)==0:
            self.amount=200
            self.brand=""
            self.name="Water"
            self.caffein=0
            self.calories=0
            self.portions=[1,10,100,200,330,500,1000,1500,2500]
        elif len(arg)==1 and type(arg[0])==dict:
            val=arg[0]
            self.amount=val['amount']
            self.brand=val['brand']
            self.name=val['name']
            self.caffein=val['caffein']
            self.calories=val['calories']
            self.portions=val['portions']
        else:
            assert False , "Zero or one argument expected!"
    
    def dict(self):
        return dict(amount=self.amount,brand=self.brand,name=self.name,caffein=self.caffein,calories=self.calories,portions=self.portions)
    
    def print(self):
        print(self.dict())

class DrinkDB:
    table_name="drink"
    def __init__(self,file_name:str):
        self.db=Database(file_name)

    def create_table(self):
        self.db.create_table(self.table_name,names=["amount","brand","name","caffein","calories","portions"],types=[int,str,str,int,int,str])

    def load(self):
        res=self.db.select_all(self.table_name)
        result=[]
        for row in res:
            portions_str=row[5]
            portions_vec=[int(val) for val in str.split(portions_str,",")]

            drink=Drink(dict(amount=int(row[0]),brand=row[1],name=row[2],caffein=int(row[3]),calories=int(row[4]),portions=portions_vec))
            result.append(drink)
        return result
    
    def update(self,drink:Drink):
        # UPDATE employees SET lastname = 'Smith' WHERE employeeid = 3;
        
        res=self.db.select(self.table_name,["name","brand"],[drink.name,drink.brand])
        if len(res)==0:
            self.save(drink)
        elif len(res)==1:
            res=res[0]
            
            temp=[]
            keys=list(drink.dict().keys())
            values=list(drink.dict().values())

            for i,key in enumerate(keys):
                val=values[i]
                if key=="portions":
                    portions_str=[str(v) for v in val]
                    val=",".join(portions_str)

                if res[i]!=val:
                    temp.append(f"{key}={val} ")
            
            query=f"UPDATE {self.table_name} SET {" AND ".join(temp)} WHERE name='{drink.name}' AND brand='{drink.brand}'"
            self.db.exec(query)

        else:
            assert False,"Multiple records found!"
        return
    
    def save(self,drink:Drink):
        # drink to database
        db=self.db
        if not db.has_table(self.table_name):
            self.create_table()
        # search for this one
        res=db.select(self.table_name,["name","brand"],[drink.name,drink.brand])
        if len(res)==0:
            # insert this
            drink.print()
            portions_str=[str(v) for v in drink.portions]
            db.insert(self.table_name,["amount","brand","name","caffein","calories","portions"],[drink.amount,drink.brand,drink.name,drink.caffein,drink.calories,",".join(portions_str)])
        elif len(res)==1:
            # need to update
            drink.print()
            pass
        else:
            # something went wrong
            pass

        
if __name__=="__main__":
    bridge=DrinkDB("drink1.sqlite")
    d=Drink({'amount': 200, 'brand': 'starbucks', 'name': 'mocha', 'caffein': 20, 'calories': 550, 'portions': [100, 200, 500, 750, 1000]})
    bridge.update(d)
    # bridge.save(d)

    res=bridge.load()
    for r in res:
        r.print()
