import pymongo
import mysql.connector
import sys

import time


class Sql:
    def __init__(self, db_host, db_user, db_password, db_name=None, db_table=None):
        self.db_name = db_name
        self.db_host = db_host
        self.db_user = db_user
        self.db_table = db_table
        self.config = {
            'user': db_user,
            'password': db_password,
            'host': db_host
        }

        if db_name is not None:
            self.config['database'] = db_name
        self.db_connector = mysql.connector.connect(**self.config)

        self.cursor = self.db_connector.cursor()

    def change_data_base(self, db_name):
        data_bases = self.get_data_bases()
        if db_name in data_bases:
            self.config['database'] = db_name
            self.db_name = db_name
            self.db_connector = mysql.connector.connect(**self.config)
            self.cursor = self.db_connector.cursor()
        else:
            print("Nie ma takiej bazy danych")

    def create_database(self, db_name):
        if not self.if_db_exists(db_name):
            self.cursor.execute("CREATE DATABASE " + db_name)
        else:
            print("Baza juz istnieje")

    def if_db_exists(self, db_name):
        data_bases = self.get_data_bases()
        exists = False
        for x in data_bases:
            if x == db_name:
                exists = True
                break
        return exists

    def get_data_bases(self):
        cursor = self.cursor
        cursor.execute("SHOW DATABASES;")
        return [x[0] for x in cursor]

    def get_tables(self):
        cursor = self.cursor
        cursor.execute("SHOW TABLES;")
        try:
            return [x[0] for x in cursor]
        except:
            return None

    def create_table(self, table_name, column_name_type_dict):
        tables = self.get_tables()
        if table_name not in tables:
            string = "CREATE TABLE " + table_name + " ( "
            is_first = True
            for el in column_name_type_dict:
                if not is_first:
                    string += ", "
                else:
                    is_first = False
                string += el.get("column_name") + " " + el.get("data_type")
            string += " );"
            self.cursor.execute(string)
        else:
            print("Tablica juz istnieje")

    def change_table(self, table_name):
        tables = self.get_tables()
        if table_name not in tables:
            print("Tabela nie istnieje")
        else:
            self.db_table = table_name

    def insert_data_dict(self, data_dict):
        if self.db_table is not None and self.db_name is not None:
            for el in data_dict:
                query = "INSERT INTO " + self.db_table + " ("
                query2 = "VALUES ("
                first = True
                for val in el:
                    if not first:
                        query += ", "
                        query2 += ", "
                    else:
                        first = False
                    query += val
                    try:
                        int(el[val])
                    except ValueError:
                        query2 += "\"" + el[val] + "\""
                    else:
                        query2 += el[val]
                query2 += ");"
                query += ") " + query2
                # print(query)
                self.cursor.execute(query)
                self.db_connector.commit()
        else:
            print("Baza nie zostala ustawiona")

    def get_data_dict(self):
        query_structure = "DESC " + self.db_table + ";"
        self.cursor.execute(query_structure)
        structure = [x[0] for x in self.cursor]

        query_select = "SELECT * FROM " + self.db_table + ";"
        self.cursor.execute(query_select)
        data = [x for x in self.cursor]
        result = []
        for values in data:
            result.append(dict(zip(structure, values)))

        return result

    def delete_table(self):
        tables = self.get_tables()
        if self.db_table in tables:
            query = "DROP TABLE " + self.db_table + ";"
            self.cursor.execute(query)

    def delete_data_base(self):
        data_bases = self.get_data_bases()
        if self.db_name in data_bases:
            query = "DROP DATABASE " + self.db_name + ";"
            self.cursor.execute(query)


class Mongo:
    def __init__(self, db_host, db_name=None, db_collection=None):
        self.db_host = db_host
        self.db_name = db_name
        self.db_client = pymongo.MongoClient("mongodb://" + self.db_host + ":27017/")
        self.db = db_name
        self.collection = None
        if db_name is not None:
            self.db = self.db_client[db_name]
            if db_collection is not None:
                self.collection = self.db[db_collection]

    def if_db_exists(self, db_name):
        data_bases = self.get_data_bases()
        exists = False
        for x in data_bases:
            if x == db_name:
                exists = True
                break
        return exists

    def get_data_bases(self):
        data_bases = self.db_client.list_database_names()
        return data_bases

    def get_collections(self):
        collections = self.db.list_collection_names()
        return collections

    def get_collection_data(self):
        collection_data = None
        if self.collection is not None:
            cursor = self.collection.find()
            collection_data = [x for x in cursor]
        return collection_data

    def change_database(self, db_name):
        self.db = self.db_client[db_name]
        self.db_name = db_name

    def change_collection(self, collection_name):
        if self.db is not None:
            self.collection = self.db[collection_name]
        else:
            print("Baza nie zostala ustawiona")

    def insert_many(self, list_of_dict):
        data_bases = self.get_data_bases()
        tables = self.get_collections()
        if self.db in data_bases and self.collection in tables:
            if self.collection is not None:
                self.collection.insert_many(list_of_dict)

    def delete_database(self):
        if self.db is not None:
            self.db_client.drop_database(self.db_name)
        else:
            print("Nie ma takiej bazy danych")


if __name__ == "__main__":
    N = 10000
    sql_con = Sql("10.5.0.3", "root", "root")

    mongo_con = Mongo("10.5.0.4")
    mongo_con.change_database("test1")

    sql_con.create_database("test")
    sql_con.change_data_base("test")

    table1 = [
        {"column_name": "id", "data_type": "INT NOT NULL AUTO_INCREMENT"},
        {"column_name": "name", "data_type": "VARCHAR(255)"},
        {"column_name": "address", "data_type": "VARCHAR(255)"},
        {"column_name": "PRIMARY KEY", "data_type": "(id)"}
    ]

    my_list = [
        {"name": "Amy", "address": "Apple st 652"},
        {"name": "Hannah", "address": "Mountain 21"},
        {"name": "Michael", "address": "Valley 345"},
        {"name": "Sandy", "address": "Ocean blvd 2"},
        {"name": "Betty", "address": "Green Grass 1"},
        {"name": "Richard", "address": "Sky st 331"},
        {"name": "Susan", "address": "One way 98"},
        {"name": "Vicky", "address": "Yellow Garden 2"},
        {"name": "Ben", "address": "Park Lane 38"},
        {"name": "William", "address": "Central st 954"}
    ]
    if "osoby" not in sql_con.get_tables():
        sql_con.create_table("osoby", table1)
        sql_con.change_table("osoby")
        mongo_con.change_collection("test_col")
        for ii in range(N):
            sql_con.insert_data_dict(my_list)
    else:
        sql_con.change_table("osoby")

    with open('result.out', 'w+') as file:
        start = time.time()
        from_my_sql = sql_con.get_data_dict()
        mongo_con.insert_many(from_my_sql)
        end = time.time()
        file.writelines(str(N) + ": " + str(end - start) + "\n")
