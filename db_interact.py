import sqlite3
import pandas as pd


class connection():
    def __init__(self, database=':memory:'):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()
        self.create_db()

    def commit(self):
        try:
            self.conn.commit()
        except:
            print("Database: Commit error.")

    def create_db(self):
        # c = conn.cursor()

        sql_command = """CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_last TEXT,
            name_first TEXT,
            gender TEXT,
            year INTEGER,
            house TEXT,
            teacher TEXT,
            dob INTEGER,
            student_id INTEGER);"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS teachers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_last TEXT,
            name_first TEXT,
            gender TEXT,
            year INTEGER,
            dob INTEGER);"""
        self.c.execute(sql_command)

        self.c.execute(sql_command)
        sql_command = """CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            name TEXT,
            track_feild TEXT,
            timed_score_distance INTEGER,
            gender TEXT);"""
        self.c.execute(sql_command)

    def insert(self, data):
        pass

    def data_entry(self):

        read_file = (pd.read_excel('Book1.xlsx'))
        df = pd.DataFrame(read_file)

        index = read_file.index
        print(index)
        # print(list(list(df.iterrows())[0][1]))

        columns = (list(df.columns.values))
        for index, row in df.iterrows():

            details = []
            for i in columns:
                # print(row[i])
                details.append(row[i])
            self.c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (
                details[0], details[1], details[2], details[3], details[4], details[5], str(details[6]), details[7]))

        self.conn.commit()

    def get_name_info(self, lookup):
        lookup = (lookup, lookup,)
        self.c.execute(
            "SELECT * FROM students WHERE ? = name_first OR ? = name_last", lookup)
        # print(c.fetchall())
        return self.c.fetchall()
