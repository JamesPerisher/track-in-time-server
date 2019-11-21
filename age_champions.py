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

app = db.connection()
app.start()

test_list = [5,4,2]

class age_champion():
    def __init__(self):
        super().__init__()

    def get_champs(self):
        results = []
        events = app.get_events()
        if events == []:
            print("empty list")
        else:
            for i in events:
                users = app.get_results_from_event(i[0])
                print(users)
                for a,b in zip(test_list, users):
                    print(app.get_participant_info(b[0], "db_id"), a)
                for j in users[len(test_list)::]:
                    print(app.get_participant_info(j[0], "db_id"), str(1))
                print()
                




if __name__ == '__main__':
    ag = age_champion()
    ag.get_champs()
