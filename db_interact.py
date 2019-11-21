#!/usr/bin/python3

# This file is part of Track In Time Server.
#
# Track In Time Server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Track In Time Server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Track In Time Server.  If not, see <https://www.gnu.org/licenses/>.



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

        self.working = True
        self.doing = True
        self.paused = False

    def kill(self):
        self.working = False

    def pause(self):
        self.paused = True

        while self.doing:
            time.sleep(0.1)
        return

    def play(self):
        self.paused = False

    def execute(self, command, timeout=-99999):
        if self.paused:
            while not self.paused:
                time.sleep(0.1)

        timeout = self.timeout if timeout == -99999 else timeout
        temp_key = time.time()
        n = temp_key + self.timeout
        local_empty = EmptyPlacerholder()

        self.outvalues[temp_key] = local_empty
        self.command_stack.append((temp_key, command))


        while self.outvalues[temp_key] == local_empty: # waits till command executed
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

        while self.working:
            if len(self.command_stack) == 0:
                self.doing = False
            for i in self.command_stack:
                try:
                    current = self.command_stack.pop(0)
                    if current[1] == ":x:x:commit:x:x:":
                        self.outvalues[current[0]] = self.conn.commit()
                        log.debug("Commit to db")
                        continue

                    log.debug("{0: <12} {1} {2}".format("Running: ", current[0], current[1].replace("            ", " ").replace("\n", "\n       ")))

                    ee = None

                    try:
                        self.crsr.execute(current[1])
                    except Exception as e:
                        # print("before e.args")
                        # print(e.args)
                        if "UNIQUE constraint failed:" in e.args[0]:
                            log.error("{0: <12} {1}, {2}".format("Record not unique: ",str(e.args[0]), str(current[1])))
                        elif "FOREIGN KEY constraint failed" in e.args[0]:
                            log.error("{0: <12} {1}, {2}".format("participant or event does not exist: ",str(e.args[0]), str(current[1])))
                        else:
                            raise e

                    self.outvalues[current[0]] = self.crsr.fetchall()

                except Exception as e:
                    self.outvalues[current[0]] = e
                    raise e


        log.debug("{0: <12} {1}".format("Killed:",  str(self)))


class connection():
    def __init__(self, database='test.db', app=None):
        super().__init__()
        self.database = database
        self.app = app
        self.last_update = time.time()
        path_for_logs = ("db/logs/%s/%s"%(datetime.date.today().year ,datetime.date.today().month))
        try:
            os.makedirs(path_for_logs)
        except:
            pass


        self.log = log.basicConfig(filename='db/logs/%s/%s/%s-%s.log'%(datetime.date.today().year ,datetime.date.today().month, datetime.date.today(), os.path.basename(__file__)[:-3]), level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        # self.start()

    def start(self):
        self.c = DatabaseManager(self.database, timeout=2)
        self.c.start()
        log.info("started db thread")
        self.c.execute("PRAGMA foreign_keys = ON;")
        self.create_db()
        print("Started database")
        log.debug("Started database")

    def kill(self):
        return self.c.kill()

    def pause(self):
        return self.c.pause()

    def play(self):
        return self.c.play()

    def update(self):
        if time.time() > self.last_update:
            self.pause()
            self.app.form_update()
            self.play()
            self.last_update = time.time() + 5


    def commit(self):
        try:
            self.c.commit()
        except Exception as e:
            raise e
            log.error("Database: Commit error.")

    def create_db(self):

        sql_command = """CREATE TABLE IF NOT EXISTS participants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_last TEXT,
            name_first TEXT,
            gender TEXT,
            year INTEGER,
            house TEXT,
            dob INTEGER,
            participant_id INTEGER DEFAULT NULL,
            UNIQUE(participant_id));"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            name TEXT,
            age_group TEXT,
            event_type INTEGER,
            gender TEXT);"""
        self.c.execute(sql_command)

        sql_command = """CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER,
            event_id INTEGER,
            result REAL DEFAULT NULL,
            UNIQUE(participant_id, event_id),
            FOREIGN KEY (participant_id) REFERENCES participants (id),
            FOREIGN KEY (event_id) REFERENCES events (id));"""
        self.c.execute(sql_command)

        self.commit()
        log.info("%s: created databases" % __name__)

    def get_data_types(self, type="year"):
        return self.c.execute("SELECT DISTINCT \"%s\" FROM participants"%(type))

    def insert_into_results(self, data):
        self.c.execute("INSERT INTO results VALUES (NULL, \"%s\", \"%s\", \"%s\")" % data)
        self.commit()

    def get_results_from_event(self, event_id):
        order_type = {
        "timed" : "ASC",
        "score" : "ASC",
        "distance" : "DESC"
        }
        return self.c.execute("SELECT * FROM results WHERE event_id = %s ORDER BY results %s" % (event_id, order_type[self.get_event_info_by_id(event_id)[0][4]]))

    def get_winners_from_event(self, event_id, amount=5):
        order_type = {
        "timed" : "ASC",
        "score" : "ASC",
        "distance" : "DESC"
        }
        return self.c.execute("SELECT * FROM results WHERE event_id = %s ORDER BY result %s LIMIT %s" % (event_id, order_type[self.get_event_info_by_id(event_id)[0][4]], amount))

    def update_participant(self, data, user_id):
        data.append(user_id)
        self.c.execute("UPDATE participants SET name_last=\"%s\", name_first=\"%s\", gender=\"%s\", year=\"%s\", house=\"%s\", dob=\"%s\", participant_id=\"%s\" WHERE id=\"%s\""%tuple(data))
        self.commit()
        self.update()

    def update_results(self, user_id, event_id, db_id, result):
        self.c.execute("UPDATE results SET participant_id=\"%s\" event_id=\"%s\" result=\"%s\" WHERE id=\"%s\""%tuple(user_id, event_id, result, db_id))


    def add_event(self, data):
        self.c.execute("INSERT INTO events VALUES (NULL, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % tuple(data))
        log.info("{0: <12} {1}".format("Event added:", str(data)))
        self.commit()
        self.update()


    def get_events(self):
        return self.c.execute("SELECT * FROM events")

    def get_event_info(self, data, search_type="name"): # name, track_field, gender
        return self.c.execute("SELECT * FROM events WHERE \"%s\" = \"%s\" COLLATE NOCASE" %(search_type, data))

    def get_dates(self):
        return self.c.execute("SELECT dob FROM participants")

    def add_participant(self, data):
        sql_command = "INSERT INTO participants VALUES (NULL, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % tuple(data)
        self.c.execute(sql_command)
        self.commit()
        self.update()


    def data_entry(self, file_location="db/Book1.xlsx"):

        # “The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places
        # and at the wrong times; premature optimization is the root of all evil (or at least most of it) in programming.” - Donald Knuth
        read_file = (pd.read_excel("db/Book1.xlsx"))
        df = pd.DataFrame(read_file)
        index = read_file.index
        columns = (list(df.columns.values))
        convert = {
            '"M"' : '"Male"',
            '"m"' : '"Male"',
            '"F"' : '"Female"',
            '"f"' : '"Female"'}
        for index, row in df.iterrows():
            details = []
            for i in columns:
                if str(row[i]) != "nan":
                    details.append(row[i])
                else:
                    details.append("NULL")
            details = [details[0], details[1], convert.get(details[2].strip(),details[2]), details[3], details[4].lower(), details[6], details[7]]
            self.add_participant(details)

        log.info("{0: <12} {1}".format("Added participants from:", file_location))
        self.commit()
        self.update()


    def get_participant_info(self, lookup, search_type="first_name"):  # search from names
        search = {
        "db_id" : "id",
        "name_first" : "name_first",
        "name_last" : "name_last",
        "gender" : "gender",
        "year" : "year",
        "house" : "house",
        "dob" : "dob",
        "participant_id" : "participant_id"
        }

        return self.c.execute("SELECT * FROM participants WHERE \"%s\" = \"%s\" COLLATE NOCASE"% (lookup, search[search_type]))


if __name__ == '__main__':

    try:
        os.remove("test.db")
    except Exception as e:
        print(e)

    c = connection()
    c.start()


    c.data_entry()

    print(c.get_data_types())
    c.add_event(("10am", "test_1", "track", "timed", "M"))
    c.add_event(("12am", "test_2", "track", "score", "F"))
    c.add_event(("11am", "test_3", "field", "distance", "M"))

    c.insert_into_results(("140", "1", "400"))
    c.insert_into_results(("5", "1", "100"))
    c.insert_into_results(("14", "1", "200"))
    c.insert_into_results(("173", "1", "300"))


    c.insert_into_results(("233", "2", "2"))
    c.insert_into_results(("11", "2", "1"))
    c.insert_into_results(("161", "2", "4"))
    c.insert_into_results(("241", "2", "3"))

    c.insert_into_results(("295", "3", "1000"))
    c.insert_into_results(("80", "3", "20"))
    c.insert_into_results(("135", "3", "500"))
    c.insert_into_results(("214", "3", "100"))

    winners = (c.get_winners_from_event("1"))
    for i in winners:
        print(c.get_participant_info(i[1], "db_id")[0], i[3])
    winners = (c.get_winners_from_event("2"))
    for i in winners:
        print(c.get_participant_info(i[1], "db_id")[0], i[3])
    winners = (c.get_winners_from_event("3"))
    for i in winners:
        print(c.get_participant_info(i[1], "db_id")[0], i[3])

    # print(self.update_participant(["1", "2", "3", "4", "5", "6", "7"], "100"))
    # """UPDATE participants SET name_last=\"%s\", name_first=\"%s\", gender=\"%s\", year=\"%s\", house=\"%s\", dob=\"%s\", participant_id=\"%s\" WHERE id=\"%s\""""%(data)
    # c.add_age_groups()

    # log.info(c.get_age_groups())
