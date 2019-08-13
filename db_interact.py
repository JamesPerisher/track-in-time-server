import sqlite3
import pandas as pd
import xlrd
import datetime
import time


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

        sql_command = """CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            name TEXT,
            track_feild TEXT,
            timed_score_distance INTEGER,
            gender TEXT);"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS age_groups(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name STRING,
            start INTEGER,
            end INTEGER);"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS year_groups(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER);"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS house(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            house TEXT
            color TEXT);"""
        self.c.execute(sql_command)

        self.commit()
        print("%s: created databases" % __name__)

    def add_age_group(self, data):
        data["start"] = time.mktime(datetime.datetime.strptime(data["start"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
        data["end"] = time.mktime(datetime.datetime.strptime(data["end"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
        sql_command_1 = "INSERT INTO age_groups VALUES (NULL, \"%s\", \"%s\", \"%s\")" % (data["name"], data["start"], data["end"])
        self.c.execute(sql_command_1)
        self.c.execute("SELECT id FROM age_groups ORDER BY id DESC LIMIT 1")
        sql_command = """CREATE TABLE IF NOT EXISTS table_{table_id}(student_id INTEGER);""".replace("{table_id}", str(self.c.fetchall()[0][0]))

        self.c.execute(sql_command)
        self.commit()

    def get_age_groups(self):
        self.c.execute("SELECT * FROM age_groups")
        return self.c.fetchall()

    def get_dates(self):
        self.c.execute("SELECT dob FROM students")
        return self.c.fetchall()

    def add_house(self, data):
        pass

    def data_entry(self):
        read_file = (pd.read_excel('Book1.xlsx'))
        df = pd.DataFrame(read_file)

        index = read_file.index

        columns = (list(df.columns.values))
        for index, row in df.iterrows():

            details = []
            for i in columns:
                # print(row[i])
                details.append(row[i])
            self.c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (details[0], details[1], details[2], details[3], details[4], details[5], str(details[6]), details[7]))

        self.conn.commit()

    def get_name_info(self, lookup):
        lookup = (lookup, lookup,)
        self.c.execute("SELECT * FROM students WHERE ? = name_first OR ? = name_last", lookup)
        # print(c.fetchall())
        return self.c.fetchall()


if __name__ == '__main__':
    c = connection()
    c.data_entry()

    years_born = [y for y in {str(x[0]).split("-")[0]: True for x in c.get_dates()}]
    years_born.sort(reverse=True)

    # print(type(years_born))
    # for i in range(4,13):
    #     for i in years_born:

    # print([(int(datetime.datetime.now().year) - int(i) - 6) for i in years_born])
    year_group = [(int(datetime.datetime.now().year) - int(i)) for i in years_born]
    max_age = max(year_group)
    print(year_group)
    print(years_born)
    # print(max_age)
    # print(year_group)
    # print(year_group)
    while max_age > 12+6:
        year_group.remove(max_age)
        max_age = max(year_group)


    # print(max_age)
    # print(year_group)
    year_group.sort(reverse=False)
    # print(years_born)
    # print(years_born[-1])
    # print("%s\n\n"% max_age)
    years_born[-1] = (int(datetime.datetime.now().year) - max_age)
    # print(years_born)
    for (year, age) in zip(years_born, year_group):
        print(year, age)

    for i in years_born:
        pass
        # print(i)

        # if (int(datetime.datetime.now().year) - int(i)) - 6 <= 12:
        #     c.add_age_group({"start": ("%s-1-1") % i, "name": ("Year %s %s") % (str(int(datetime.datetime.now().year) - int(i) - 6), i), "end": ("%s-1-1") % str(int(i) + 1)})
            # print("Test")
    # for i in c.get_age_groups():
    #     print(i[1], datetime.datetime.fromtimestamp(i[2]), datetime.datetime.fromtimestamp(i[3]))
    # print(c.get_name_info("Person"))
