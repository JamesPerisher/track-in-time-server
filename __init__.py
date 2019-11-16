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


from routes import app
from threading import Thread

import time

class main(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    m = main()
    m.start()
    time.sleep(1)
    app.db.start()
    time.sleep(2)

    if input("Add users Y/N > ").strip().lower() == "y":
        app.db.data_entry()
