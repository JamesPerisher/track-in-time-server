import routes
import db_interact
from threading import Thread

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





if __name__ == '__main__':
    db_mg = database_management(db_interact.connection(), None)
    wp_mg = web_pages(db_mg, True)
    db_mg.pages = wb_mg

    wp_mg.start()
    db_mg.start()
