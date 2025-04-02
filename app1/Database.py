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

    def delete_table(self,table_name:str):
        self.exec(f"DROP TABLE IF EXISTS {table_name}")

    def insert(self,table_name:str,columns:list,values:str):
        # INSERT INTO table (column1,column2 ,..) VALUES( value1,	value2 ,...);
        vals=[f"'{v}'" for v in values]
        sql_str=f"INSERT INTO {table_name} ({",".join(columns)}) VALUES({",".join(vals)})"
        print(sql_str)
        self.exec(sql_str)
        self.con.commit()

    def select_all(self,table_name:str):
        res=self.exec(f"SELECT * FROM {table_name}")
        data=res.fetchall()
        print(data)

    def __del__(self):
        self.con.close()

db=Database("deneme.sqlite")
# db.create_table("test_table",["id","name"],[int,str])
# db.insert("test_table",["id","name"],["0","ascd"])
# db.insert("test_table",["id","name"],["1","cd"])
db.select_all("test_table")