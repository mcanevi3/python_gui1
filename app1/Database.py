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
        return data
    
    def has_table(self,table_name:str):
        tables=self.list_tables()
        exists=False
        for item in tables:
            if item[0]==table_name:
                exists=True
        return exists            

    def delete_table(self,table_name:str):
        self.exec(f"DROP TABLE IF EXISTS {table_name}")

    def insert(self,table_name:str,columns:list,values:list):
        # INSERT INTO table (column1,column2 ,..) VALUES( value1,	value2 ,...);
        vals=[f"'{v}'" for v in values]
        sql_str=f"INSERT INTO {table_name} ({",".join(columns)}) VALUES({",".join(vals)})"
        print(sql_str)
        self.exec(sql_str)
        self.con.commit()

    def select_all(self,table_name:str):
        if self.has_table(table_name=table_name):
            res=self.exec(f"SELECT * FROM {table_name}")
            data=res.fetchall()
            return data
        else:
            return None
    def select(self,table_name:str,columns:list,values:list):
        sql_str=f"SELECT * FROM {table_name} WHERE "
        for i,col in enumerate(columns):
            val=values[i]
            if type(val) is str:
                val=f"'{val}'"

            if i<len(values)-1:
                sql_str+=f"{col}={val} AND "
            else:
                sql_str+=f"{col}={val} "
        res=self.exec(sql_str)
        data=res.fetchall()
        return data
        
    def __del__(self):
        self.con.close()

class Table:
    table_name=""
    columns=[]
    file_name:str

    def __init__(self,*arg):

        if len(arg)==1:
            file_name=arg[0]
            self.db=Database(file_name)

        elif len(arg)==2:
            file_name=arg[0]
            properties=arg[1]

            self.table_name=properties["table_name"]
            for col in properties["columns"]:
                self.columns.append(col)

            self.db=Database(file_name)

    def create(self):
        names=[]
        types=[]
        for col in self.columns:
            (name_,type_)=col
            names.append(name_)
            types.append(type_)
        self.db.create_table(self.table_name,names=names,types=types)

    def print(self):
        print(f"[{self.table_name}]")
        for col in self.columns:
            (name_,type_)=col
            print(name_,type_)

    def load(self):
        res=self.db.select_all(self.table_name)
        result=[]
        for row in res:
            result.append(row)
        return result
    
    def column_info(self):
        res=self.db.exec(f"pragma table_info({self.table_name})")
        data=res.fetchall()
        return data
    
    def column_count(self):
        data=self.column_info()
        return len(data)
    
    def load_columns(self):
        arg_types=[None,int,float,str,bytes]
        sql_types=["NULL","INTEGER","REAL","TEXT","BLOB"]

        info=self.column_info()
        self.columns=[]
        for col in info:
            i=sql_types.index(col[2])
            self.columns.append((col[1],arg_types[i]))

    def insert(self,data:dict):
        columns=list(data.keys())
        values=list(data.values())
        self.db.insert(self.table_name,columns,values)

    def update(self,vec:list,where:list):
        w_names=[]
        w_values=[]
        for col in where:
            (name_,value_)=col
            w_names.append(name_)
            w_values.append(value_)
        w_temp=[]
        for i,name in enumerate(w_names):
            val=w_values[i]
            w_temp.append(f"{name}={val} ")

        names=[]
        values=[]
        for col in vec:
            (name_,value_)=col
            names.append(name_)
            values.append(value_)

        res=self.db.select(self.table_name,w_names,w_values)
        if len(res)==0:
            print(vec)
            # self.insert()
        elif len(res)==1:
            res=res[0]

            temp=[]
            for i,name in enumerate(names):
                val=values[i]
                temp.append(f"{name}={val} ")
            
            query=f"UPDATE {self.table_name} SET {" AND ".join(temp)} WHERE {"".join(w_temp)}"
            print(query)


if __name__=="__main__":
    table1=Table("deneme.sqlite",{"table_name":"coffee","columns":[("name",str),("brand",str),("calories",int)]})
    table1.create()
    res=table1.update([("name","espresso"),("brand","starbucks"),("calories",134)],[("name","americano")])
    # print(res)
    # table1.load_columns()

    # table1.insert({"name":"latte","brand":"starbucks","calories":23})

    # db=Database("deneme.sqlite")
    # db.insert("coffee",["name","brand"],["americano","starbucks"])

    # # db.insert("test_table",["id","name"],["0","ascd"])
    # # db.insert("test_table",["id","name"],["1","cd"])
    # res=db.select_all("coffee")
    # res=db.select("test_table",["id"],[1])
    # print(res)