from Database import *

class Table:
    table_name=""
    columns=[]
    file_name:str

    def __init__(self,file_name:str,properties:dict):

        assert "table_name" in properties , "Dict needs to have field table_name!"
        assert "columns" in properties , "Dict needs to have field columns!"

        self.table_name=properties["table_name"]

        self.db=Database(file_name)
        if self.db.has_table(self.table_name):
            self.load_columns()
        else:
            for col in properties["columns"]:
                self.columns.append(col)
            self.create()
            self.load_columns()

    def create(self):
        names=[]
        types=[]
        for col in self.columns:
            (name_,type_)=col
            names.append(name_)
            types.append(type_)
        self.db.create_table(self.table_name,names=names,types=types)

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

    def print(self):
        print(f"[{self.table_name}]")
        for col in self.columns:
            (name_,type_)=col
            print(name_,type_)


    def select_all(self):
        res=self.db.select_all(self.table_name)
        result=[]
        for row in res:
            result.append(row)
        return result
    
    def insert(self,data:dict):
        columns=list(data.keys())
        values=list(data.values())
        db_col_names=[c[0] for c in self.columns]
        for col in columns:
            assert col in db_col_names , f"{col} is not in table {self.table_name}!"
        self.db.insert(self.table_name,columns,values)


if __name__=="__main__":
    table1=Table("deneme.sqlite",{"table_name":"tea","columns":[("name",str),("brand",str),("tein",int)]})
    table1.insert({"name":"tea1","brand":"starbucks","tein":30})
    print(table1.select_all())
    # db=Database("deneme.sqlite")
    # res=db.list_tables()
    # print(res)
