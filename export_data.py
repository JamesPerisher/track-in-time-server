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

test_list = [5,4,2]

class data():
    def __init__(self, db):
        super().__init__()
        self.db = db

    def get_champs(self):
        results = []
        events = self.db.get_events()
        if events == []:
            print("empty list")
        else:
            for i in events:
                users = self.db.get_results_from_event(i[0])
                print(users)
                for a,b in zip(test_list, users):
                    print(self.db.get_participant_info(b[0], "db_id"), a)
                for j in users[len(test_list)::]:
                    print(self.db.get_participant_info(j[0], "db_id"), str(1))
                print()


    def excel_all(self):
        # print(self.db.get_events())
        # writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
        for i in self.db.get_events():
            data = self.db.get_results_from_event(i[0])
            print()
            for j in data:
                student = self.db.get_participant_info(j[1], "db_id")[0]
                event =  self.db.get_event_info(j[2], "id")[0]
                print(student[2], student[1], event[2], j[3])


    def excel_winners(self):
        try:
            os.remove("downloads/pandas_simple.xlsx")
        except Exception as e:
            print(e)

        df = pd.DataFrame()
        writer = pd.ExcelWriter('downloads/pandas_simple.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        print("Done?")
        # exel_winners = pd.read_excel("/random.xlsx")






if __name__ == '__main__':
    db = db.connection()
    db.start()


    data = data(db)
    data.excel_all()
    data.excel_winners()
