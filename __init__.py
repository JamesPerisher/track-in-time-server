#!/usr/bin/env python

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

import routes
import db_interact
from threading import Thread
import os
import json

class web_pages(Thread):
    def __init__(self, database_interact, start=True):
        self.app = routes.app
        self.db = self.database_interact = database_interact

        if start:
            self.app.run()

    def start_app(self):
        self.app.run()

class database_management(Thread):
    def __init__(self, connection, pages):
        self.c = connection
        self.pages = pages

class configuration():
    def __init__(self, file_dir=os.getcwd()):
        self.file_dir = file_dir
        self.name = "config.json"
        self.fields = {"test":"testing"}

        open(os.path.join(self.file_dir, self.name), "a").close()

        with open(os.path.join(self.file_dir, self.name), "r") as f:
            try:
                self.fields.update(json.loads(f.read()))
            except json.decoder.JSONDecodeError:
                pass
        with open(os.path.join(self.file_dir, self.name), "w") as f:
            f.truncate()
            f.write(json.dumps(self.fields))

        [setattr(self, x, self.fields[x]) for x in self.fields]

    def get_all(self):
        out = ["{"]
        for i in self.fields:
            out.append("%s : %s" %(i, self.fields[i]))
        out.append("}")
        return "\n".join(out)




if __name__ == '__main__':
    config = configuration()
    print(config.test)
    print(config.get_all())

    db_mg = database_management(db_interact.connection(), None)
    wp_mg = web_pages(db_mg, True)
    db_mg.pages = wb_mg

    wp_mg.start()
    db_mg.start()
