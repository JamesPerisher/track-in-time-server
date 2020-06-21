from flask import Blueprint
import activity
from activity import *

recordPages = Blueprint("reporting", __name__)
activity.recordPages = recordPages

@recordPages.record
def record(state):
    recordPages.db = state.app.config.get("database")

    if recordPages.db is None:
        raise Exception("This blueprint expects you to provide  database access through database")


recordPages.route('/add_user', methods=["GET","POST"])(add_user)
recordPages.route('/add_house', methods=["GET","POST"])(add_house)
recordPages.route('/add_gender', methods=["GET","POST"])(add_gender)
recordPages.route('/add_event', methods=["GET","POST"])(add_event)

