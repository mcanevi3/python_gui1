import webview
import sqlite3

class Database:
    file_name:str
    def __init__(self,file_name:str):
        self.file_name=file_name
        self.con = sqlite3.connect(self.file_name)

    def exec(self,string:str):
        cur = self.con.cursor()
        return cur.execute(string)
    
    def create_table(self,table_name:str,names:list,types:list):
        # CREATE TABLE movie(title, year, score)
        arg_types=[None,int,float,str,bytes]
        data_types=["NULL","INTEGER","REAL","TEXT","BLOB"]

        cols=[]
        for i,name in enumerate(names):
            type_i=arg_types.index(types[i])
            type_str=data_types[type_i]
            cols.append(f"{name} {type_str}")
        
        sql_str=f"CREATE TABLE IF NOT EXISTS {table_name}({",".join(cols)})"
        self.exec(sql_str)

    def list_tables(self):
        res=self.exec("SELECT name FROM sqlite_master WHERE type = 'table'")
        data=res.fetchall()
        print(data)

    def __del__(self):
        self.con.close()

class Api:
    def test(self,arg):
        print(f"test arg: {arg}")

def main_loop(window):
    pass
def on_closing():
    print("Window is about to close")

db=Database("deneme.sqlite")
db.create_table("test_table",["id","name"],[int,str])
db.list_tables()

# window=webview.create_window('TestApp', 'assets/index.html',min_size=(400,300),js_api=Api())
# window.events.closing+=on_closing
# webview.start(func=main_loop,args=window,ssl=True)
# pass
