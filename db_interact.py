import sqlite3
import pandas as pd
import xlrd
import datetime
import time
import logging as log

class connection():
    def __init__(self, database=':memory:'):
        self.log = log.basicConfig(filename='db_interact.log', level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
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

        self.commit()
        print("%s: created databases" % __name__)


    def add_age_group(self, data):
        data["start"] = time.mktime(datetime.datetime.strptime(data["start"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
        data["end"] = time.mktime(datetime.datetime.strptime(data["end"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
        self.c.execute("INSERT INTO age_groups VALUES (NULL, \"%s\", \"%s\", \"%s\")" % (data["name"], data["start"], data["end"]))
        self.commit()

    def get_age_groups(self):
        self.c.execute("SELECT * FROM age_groups")
        return self.c.fetchall()

    # def get_year_group(self, year):
    #     self.c.execute("SELECT * FROM students WHERE year = \"%s\""%(year))
    #     return self.c.fetchall()

    def get_dates(self):
        self.c.execute("SELECT dob FROM students")
        return self.c.fetchall()

    def add_student(self, data):
        self.c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (data))

    def data_entry(self):
        read_file = (pd.read_excel('Book1.xlsx'))
        df = pd.DataFrame(read_file)

        index = read_file.index

        columns = (list(df.columns.values))
        added_students = ()
        passed_students = ()
        for index, row in df.iterrows():

            details = []

            for i in columns:
                # print(row[i])
                details.append(row[i])
            student_details = [x if str(x) != "nan" else "" for x in [details[0], details[1], details[2], details[3], details[4], str(details[6]), details[7]]]

            if tuple(student_details[:5]) not in [i[1::][:-2:] for i in self.get_name_info(details[0])]:
                added_students = (added_students+(details[1],details[0]))
                # self.c.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", ([x if str(x) != "nan" else "" for x in [details[0], details[1], details[2], details[3], details[4], str(details[6]), details[7]]]))
                self.add_student(student_details)
            else:
                passed_students = (passed_students+(tuple((details[1],details[0]))))

        log.info("{0: <12} {1}".format("Did not add:",str(passed_students)))
        log.info("{0: <12} {1}".format("Added:",str(added_students)))


        self.conn.commit()

    def get_name_info(self, lookup):
        self.c.execute("SELECT * FROM students WHERE ? = name_first OR ? = name_last", (lookup, lookup))
        return self.c.fetchall()


if __name__ == '__main__':
    c = connection("test.db")
    c.data_entry()


    # for i in range(10):
    #     c.add_age_group({"start": ("%s-1-1") % i, "name": ("Year %s %s") % (str(int(datetime.datetime.now().year) - int(i)), i), "end": ("%s-1-1") % str(int(i) + 1)})
    # test = c.get_year_group(5)
    # print(test)
    get_dates_var = c.get_dates()

    years = list(dict.fromkeys([num for num in (get_dates_var[year][0].split("-")[0] for year in range(len(get_dates_var)))]))
    years.sort()
    log.info(years)

    # for i in
    for i in years:
        if int(i) not in [x[1] for x in c.get_age_groups()]:
            c.add_age_group({"start": ("%s-1-1") % i, "name": ("%s") % (i), "end": ("%s-1-1") % str(int(i) + 1)})

    log.info(c.get_age_groups())
    # print(c.testing())

    # for i in c.get_year_groups():
    #     print(i)
    # print(c.get_name_info("Person"))
