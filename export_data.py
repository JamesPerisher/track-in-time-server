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
        name = "TopPerEvent_%s-%s.xlsx" %(date.today().strftime("%d.%m.%y"),str(time.time()).split(".")[0].strip())
        writer = pd.ExcelWriter('downloads/%s'%name, engine='xlsxwriter')

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
                test_list = [5,4,3,2]

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

                results_list.append(results.copy())

                info = pd.DataFrame({1:[i[2]],2:[i[3]],3:[i[5]]})
                results.pop("ID")
                all_data = pd.DataFrame(results)
                info.to_excel(writer, sheet_name="points", index=False, header=False, startcol=count*5, startrow=0)
                all_data.to_excel(writer, sheet_name="points", index=False, header=True, startcol=count*5, startrow=2)



        age_champs = self.point_adder(results_list)
        pd.DataFrame()


        writer.save()

        return age_champs

    def excel_aged_champs(self):
        name = "AgedChampions_%s-%s.xlsx" %(date.today().strftime("%d.%m.%y"),str(time.time()).split(".")[0].strip())
        writer = pd.ExcelWriter('downloads/%s'%name, engine='xlsxwriter')

        results_list = []

        events = self.db.get_events()
        if events == []:
            pass
        else:
            for count,i in enumerate(events):
                results = {}
                results["Students"] = []
                results["House"] = []
                results["Score"] = []
                results["Points"] = []
                results["ID"] = []
                event_results = self.db.get_results_from_event(i[0])
                test_list = [5,4,3,2]

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
                results_list.append(results.copy())


        age_champs = self.point_adder(results_list)

        people = pd.DataFrame(columns=["name_first", "name_last", "gender", "year", "dob", "house", "points"])

        housepoints = {}

        for k,user in enumerate(age_champs):
            points = age_champs[user]
            user = self.db.get_participant_info(user, "db_id")[0]

            housepoints[user[5]] = [housepoints.get(user[5], [0])[0] + points]
            people.loc[k] = [user[2], user[1], user[3], user[4], user[6], user[5], points]


        people.to_excel(writer, sheet_name="aged champions", index=False, header=True, startcol=0, startrow=0)
        pd.DataFrame(data=housepoints).to_excel(writer, sheet_name="aged champions", index=False, header=True, startcol=8, startrow=0)

        writer.save()




# {dwdwd:[efd,fe,sdg,ef], wad:[gr,awd,wad,aw]}

    def excel_all(self):
        # print(self.db.get_events())

        name = "AllUser_%s-%s.xlsx" %(date.today().strftime("%d.%m.%y"),str(time.time()).split(".")[0].strip())

        writer = pd.ExcelWriter('downloads/%s'%name, engine='xlsxwriter')

        events = self.db.get_events()
        results = self.db.get_results()

        data_to_add = {}
        for i in results:
            try:
                data_to_add[i[1]].append(i)
            except KeyError:
                data_to_add[i[1]] = [i]

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
        event_data.to_excel(writer, sheet_name=event[2][0:30], index=False, header=False, startrow=0)
        all_data.to_excel(writer, sheet_name=event[2][0:30], index=False, startcol=2)

        writer.save()

    def point_adder(self, b):
        out = {}

        for a in b:
            for i in range(len(a["Points"])):
                try:
                    out[a["ID"][i]] += a["Points"][i]
                except KeyError:
                    out[a["ID"][i]] = a["Points"][i]
        return out


    def aged_champs_sorter(self, raw_data):
        out = {}

        for i in raw_data:
            u = self.db.get_participant_info(i, "db_id")[0]

            try:
                out[u[4]].append((u[2], u[1], u[6], u[5], raw_data[i]))
            except KeyError:
                out[u[4]] = [(u[2], u[1], u[6], u[5], raw_data[i])]

        for i in out:
            out[i].sort(key = lambda x: x[4])
            out[i] = out[i][0:5]

        return out


if __name__ == '__main__':
    db = db.connection()
    db.start(5)


    data = dataManager(db)

    data.excel_aged_champs()

    db.kill()
