import sqlite3
import pandas as pd

class connection():
    def __init__(self, database=':memory:'):
        self.conn = sqlite3.connect(database)

    def start(self):
        self.c = connection.cursor()

    def commit(self):
        try:
            connection.commit()
        except:
            print("Database: Logging error.")

    def create_db(self):
        c = conn.cursor()
        sql_command = """CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_last TEXT,
            name_first TEXT,
            gender TEXT,
            year INTEGER,
            house TEXT,
            teacher TEXT,
            dob TEXT,
            student_id INTEGER);"""
        c.execute(sql_command)

    def insert(self):
        pass

    def data_entry():

        read_file = (pd.read_excel('C:\\Users\\JKook Studios\\Documents\\School\\carnival_system\\Book1.xlsx'))
        df = pd.DataFrame(read_file)

        index = read_file.index
        print(index)
        #print(list(list(df.iterrows())[0][1]))

        columns = (list(df.columns.values))
        for index,row in df.iterrows():

            details = []
            for i in columns:
                # print(row[i])
                details.append(row[i])
            c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (details[0],details[1],details[2],details[3],details[4].capitalize(),details[5],str(details[6]),details[7], None))


        conn.commit()



# import sqlite3
# import pandas as pd
#
#
# def start():
#     global conn, c
#     conn = sqlite3.connect(":memory:")
#     c = conn.cursor()
#
# def close():
#     global conn, c
#     conn.commit()
#     conn.close()
#
# def create_table():
#     global conn, c
#     c.execute("""CREATE TABLE IF NOT EXISTS students(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 surname TEXT,
#                 name TEXT,
#                 gender TEXT,
#                 year INTEGER,
#                 house TEXT,
#                 teacher TEXT,
#                 dob TEXT,
#                 time INTEGER,
#                 student_id INTEGER);""")
#
#
# def data_entry():
#     global conn, c
#
#     read_file = ((pd.read_excel('D:/Users/JKook Studios/Downloads/Files/School/IT/carnival_system/Book2.xlsx')))
#     df = pd.DataFrame(read_file)
#
#     index = read_file.index
#
#     #print(list(list(df.iterrows())[0][1]))
#
#     columns = (list(df.columns.values))
#     for index,row in df.iterrows():
#
#         details = []
#         for i in columns:
#             # print(row[i])
#             details.append(row[i])
#         c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (details[0],details[1],details[2],details[3],details[4].capitalize(),details[5],str(details[6]),details[7], None))
#
#
#     conn.commit()
#
#
# def update(ID, type, to):
#     global conn, c
#     c.execute("UPDATE students SET %s = ? WHERE ID = ?" %(type), (to, ID))
#
# def get_info(type, lookup):
#     global conn, c
#     (c.execute("SELECT * FROM students WHERE %s = ?" %(type),(lookup,)))
#     #print(c.fetchall())
#     return c.fetchall()
#
# def get_data_types():
#     global conn, c
#     c.execute("SELECT * FROM students")
#     col_name_list = [tuple[0] for tuple in c.description]
#
#
#
#     return (col_name_list)
#
# if __name__ == '__main__':
#     start()
#
#     create_table()
#
#     data_entry()
#     #get_data_types()
#     close()
