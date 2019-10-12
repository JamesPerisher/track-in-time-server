import sqlite3
import pandas as pd
import xlrd
import datetime
import time
import logging as log
from threading import Thread
import os, sys


class EmptyPlacerholder():
    def __init__(self):
        pass


class DatabaseManager(Thread):

    def __init__(self, file=":memory:", timeout=2, *arg):
        super().__init__()
        self.file = file
        self.timeout = timeout # timeout in seconds

        self.command_stack = []
        self.outvalues = {}

    def execute(self, command):
        temp_key = time.time()
        n = temp_key + self.timeout

        self.outvalues[temp_key] = EmptyPlacerholder()
        self.command_stack.append((temp_key, command))


        while type(self.outvalues[temp_key]) == type(EmptyPlacerholder()): # waits till command executed

            if time.time() > n: # it took too long
                raise TimeoutError("Timed out while waiting for serialised database interaction.")

        temp_out = self.outvalues[temp_key]
        self.outvalues.pop(temp_key) # clear value from dict

        return temp_out

    def commit(self):
        self.execute(":x:x:commit:x:x:")

    def run(self): # auto colled on Thread start
        self.conn = sqlite3.connect(self.file)
        self.crsr = self.conn.cursor()

        while True:
            for i in self.command_stack:
                try:
                    current = self.command_stack.pop(0)
                    if current[1] == ":x:x:commit:x:x:":
                        self.outvalues[current[0]] = self.conn.commit()
                        print("Commit to db")
                        return


                    print("Runing: ", end="")
                    print(current)

                    ee = None

                    try:
                        self.crsr.execute(current[1])
                    except Exception as e:
                        ee = e

                    self.outvalues[current[0]] = (self.crsr.fetchall(), ee)
                except Exception as e:
                    self.outvalues[current[0]] = e

                    raise e


class connection():
    def __init__(self, database=':memory:'):
        # print(datetime.date.today().year)
        # print(datetime.date.today().month)
        path = ("db/%s/%s"%(datetime.date.today().year ,datetime.date.today().month))
        try:
            os.makedirs(path)
        except:
            print("%s already exists"%path)


        self.log = log.basicConfig(filename='db/%s/%s/%s-%s.log'%(datetime.date.today().year ,datetime.date.today().month, datetime.date.today(), os.path.basename(__file__)[:-3]), level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        self.c = DatabaseManager(database)
        self.c.start()

        self.create_db()


    def commit(self):
        try:
            self.c.commit()
        except Exception as e:
            raise e
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

    def add_age_groups(self):
        get_dates_var = c.get_dates()

        years = list(dict.fromkeys([num for num in (get_dates_var[year][0].split("-")[0] for year in range(len(get_dates_var)))]))
        years.sort()
        # log.info(years)

        for i in years:
            if int(i) not in [x[1] for x in c.get_age_groups()]:
                data = ({"start": ("%s-1-1") % i, "name": ("%s") % (i), "end": ("%s-1-1") % str(int(i) + 1)})
                data["start"] = time.mktime(datetime.datetime.strptime(data["start"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
                data["end"] = time.mktime(datetime.datetime.strptime(data["end"].replace("-", "/"), "%Y/%m/%d").timetuple())  # looks like this 2002-11-11 convert to unix
                self.c.execute("INSERT INTO age_groups VALUES (NULL, \"%s\", \"%s\", \"%s\")" % (data["name"], data["start"], data["end"]))
            self.commit()

    def get_age_groups(self):
        return self.c.execute("SELECT * FROM age_groups")

    def add_event(self, data):
        self.c.execute("INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?)", (data))
        log.info("{0: <12} {1}".format("Event added:",str(data)))

    def get_events(self):
        return self.c.execute("SELECT * FROM events")

    def get_dates(self):
        return self.c.execute("SELECT dob FROM students")

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


        self.c.commit()

    def get_name_info(self, lookup):
        self.c.execute("SELECT * FROM students WHERE ? = name_first OR ? = name_last", (lookup, lookup))
        return self.c.execute("SELECT * FROM students WHERE ? = name_first OR ? = name_last", (lookup, lookup))



if __name__ == '__main__':
    c = connection()
    c.data_entry()

    c.add_age_groups()

    log.info(c.get_age_groups())
