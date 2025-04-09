from Database import *

class Table:
    table_name=""
    columns=[]
    file_name:str

    def __init__(self,file_name:str,properties:dict):

        assert "table_name" in properties , "Dict needs to have field table_name!"
        self.table_name=properties["table_name"]

        self.db=Database(file_name)
        if self.db.has_table(self.table_name):
            pass
        else:
            assert "columns" in properties , "Dict needs to have field columns!"
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
    
    def has_columns(self,column_names):
        res=True
        db_col_names=[c[0] for c in self.columns]
        for col in column_names:
            res=res and (col in db_col_names)
        return res

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

    def delete(self,where:dict):
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
    table1=Table("deneme.sqlite",{"table_name":"tea"})
    print(table1.columns)
    print(table1.select_all())

    print(table1.has_columns(["name","brand"]))
    # db=Database("deneme.sqlite")
    # res=db.list_tables()
    # print(res)
