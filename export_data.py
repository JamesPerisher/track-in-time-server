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
import time

from datetime import date


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
        results_list = []

        events = self.db.get_events()
        if events == []:
            print("empty list")
        else:
            for count,i in enumerate(events):
                results = {}
                results["Students"] = []
                results["House"] = []
                results["Score"] = []
                results["Points"] = []
                results["ID"] = []
                event_results = self.db.get_results_from_event(i[0])

                for amount in test_list[0:len(event_results)]:
                    results["Points"].append(amount)

                for _ in event_results[len(test_list)::]:
                    results["Points"].append(1)

                for result in event_results:
                    student = (self.db.get_participant_info(result[1], "db_id"))[0]
                    results["ID"].append(student[0])
                    results["House"].append(student[5])
                    results["Students"].append("%s %s"%(student[2], student[1]))
                    results["Score"].append(result[3])

                # print(results)
                results_list.append(results.copy())

                info = pd.DataFrame({1:[i[2]],2:[i[3]],3:[i[5]]})
                results.pop("ID")
                all_data = pd.DataFrame(results)
                info.to_excel(writer, sheet_name="points", index=False, header=False, startcol=count*5, startrow=0)
                all_data.to_excel(writer, sheet_name="points", index=False, header=True, startcol=count*5, startrow=2)


        age_champs = (self.point_adder(results_list))
        print(age_champs)
        pd.DataFrame()


        writer.save()


# {dwdwd:[efd,fe,sdg,ef], wad:[gr,awd,wad,aw]}

    def excel_all(self):
        # print(self.db.get_events())

        name = "EventResults_%s-%s.xlsx" %(date.today().strftime("%d.%m.%y"),str(time.time()).split(".")[0].strip())

        writer = pd.ExcelWriter('downloads/%s'%name, engine='xlsxwriter')

        events = self.db.get_events()
        results = self.db.get_results()

        data_to_add = {}
        for i in results:
            try:
                data_to_add[i[1]].append(i)
            except KeyError:
                data_to_add[i[1]] = [i]


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


        all_data = pd.DataFrame(final)
        event_data = pd.DataFrame({"should_not_be_seeing_this":event[2::]})
        event_data.to_excel(writer, sheet_name=event[2], index=False, header=False, startrow=0)
        all_data.to_excel(writer, sheet_name=event[2], index=False, startcol=2)

        writer.save()

    def point_adder(self, b):
        out = {}

        for a in b:
            print(a)
            for i in range(len(a["Points"])):
                try:
                    out[a["ID"][i]] += a["Points"][i]
                except KeyError:
                    out[a["ID"][i]] = a["Points"][i]

if __name__ == '__main__':
    db = db.connection()
    db.start(5)


    data = dataManager(db)
    data.excel_winners()
    data.excel_all()
    # data.get_champs()
    db.kill()
    exit()
