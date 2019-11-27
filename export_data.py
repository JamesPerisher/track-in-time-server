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

import db_interact as db
import pandas as pd
import numpy as np
import os



class dataManager():
    def __init__(self, db):
        super().__init__()
        self.db = db

        try:
            os.mkdir("downloads")
        except FileExistsError:
            pass


    def get_champs(self):
        writer = pd.ExcelWriter('downloads/points.xlsx', engine='xlsxwriter')

        test_list = [5,4,2]

        events = self.db.get_events()
        if events == []:
            print("empty list")
        else:
            for count,i in enumerate(events):
                results = {}
                results["Students"] = []
                print(i)
                results["%s - %s"% (i[3], i[5])] = []
                event_results = self.db.get_results_from_event(i[0])
                print(event_results)
                print(event_results)
                for a,b in zip(test_list, event_results):
                    results["%s - %s"% (i[3], i[5])].append(a)
                    student = (self.db.get_participant_info(b[0], "db_id"))[0]
                    results["Students"].append("%s %s"%(student[2], student[1]))
                    # print(self.db.get_participant_info(b[0], "db_id"), a)
                for j in event_results[len(test_list)::]:
                    results["%s - %s"% (i[3], i[5])].append(1)
                    student = (self.db.get_participant_info(j[0], "db_id"))[0]
                    results["Students"].append("%s %s"%(student[2], student[1]))
                    # print(self.db.get_participant_info(j[0], "db_id"), str(1))
                # print()

                # print(results)
                all_data = pd.DataFrame(results)
                all_data.to_excel(writer, sheet_name="points", index=False, header=True, startcol=count*3)

        writer.save()


    def excel_all(self):
        # print(self.db.get_events())

        writer = pd.ExcelWriter('downloads/all.xlsx', engine='xlsxwriter')

        events = self.db.get_events()


        data_to_add = {"Student":[],"Score":[]}
        for i in events:

            data = self.db.get_results_from_event(i[0])
            event =  self.db.get_event_info(data[0][2], "id")[0]
            print(event[2])

            for j in data:
                student = self.db.get_participant_info(j[1], "db_id")[0]

                data_to_add["Student"].append(student[0])
                data_to_add["Score"].append(j)
                print(student[2], student[1], j[3])


        print(data_to_add)
        print("done")
        {'Student': ['Oli Dicer', 'Dana Atkins'], 'Score': [24.0, 1234.0]}
        # data_to_add = {198: [(3, 198, 1, 42.0)], 202: [(1, 202, 1, 356.0)], 208: [(2, 208, 1, 43.0)], 209: [(4, 209, 1, '`12')], 212: [(5, 212, 1, 43.0)], 275: [(7, 275, 2, 32.0), (10, 275, 3, 4356.0), (12, 275, 4, 1234.0)], 276: [(11, 276, 3, 12.0), (13, 276, 4, 24.0)], 277: [(9, 277, 2, 24.0)], 282: [(6, 282, 2, 134.0)], 283: [(8, 283, 2, '`1')]}


        event_ids = [x[0] for x in events]


        # NOTE: DO NOT TOUCH THIS!!! TREAT LIKE BLACK BOX.

        # lookup tables
        # NOTE: event_ids must be unique
        final = {"Name":[], "DOB":[], "House":[]}
        f = {}
        for i,x in enumerate(event_ids):
            f[x] = i

        p = list([None]*len(event_ids))


        # logic
        out = {}
        for user_id in data_to_add:
            out[user_id] = []
            for result in data_to_add[user_id]:
                out[user_id].append(result[2])

        o = {}
        for user_id in out:
            data = out[user_id]
            a = p[0::]
            for data_i in data:

                try:

                    a[f[data_i]] = [x for x in data_to_add[user_id] if x[2] == data_i][0][3]
                except IndexError:
                    print("error")

            o[user_id] = a


        for event in events:
            print(event)
            final["%s - %s"% (event[2], event[0])] = []

        for i in o:
            student_info = self.db.get_participant_info(i, "db_id")[0]
            Name = ("%s %s" %(student_info[2], student_info[1]))
            final["Name"].append(Name)
            final["DOB"].append(student_info[6])
            final["House"].append(student_info[5])
            for event, val in zip(events,o[i]):
                final["%s - %s"% (event[2], event[0])].append(val)
                # final[j].append([])
        # print(o)
        print(final)


        all_data = pd.DataFrame(final)
        print(event)
        event_data = pd.DataFrame({"should_not_be_seeing_this":event[2::]})
        event_data.to_excel(writer, sheet_name=event[2], index=False, header=False, startrow=0)
        all_data.to_excel(writer, sheet_name=event[2], index=False, startcol=2)

        writer.save()



if __name__ == '__main__':
    db = db.connection()
    db.start(5)


    data = dataManager(db)
    data.excel_winners()
    data.excel_all()
    # data.get_champs()
    db.kill()
    exit()
