class input_element():
    def __init__(self, display_name, var_name, value="", required=True):
        self.template = "input_empty.html"
        self.display_name = display_name
        self.var_name = var_name
        self.value = value
        self.reqired = required
        self.custom = {}

class input_text(input_element):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)

        self.template = "input_text.html"

class input_gender(input_element):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.template = "input_gender.html"


class input_yearGroup(input_element):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.custom["data"] = {"7":"Seven", "10":"ten"} # get data
        self.template = "input_class.html"


class input_house(input_yearGroup):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.custom["data"] = {"earth":"Earth", "fire":"Fire"} # get data


class input_age_group(input_yearGroup):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.custom["data"] = {"2142153-452214123":"date1-date2", "452214123-65435675624":"date2-date3"} # get data

class input_event_type(input_yearGroup):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.custom["data"] = {"timed":"Timed", "placed":"Placed", "placed_timed":"Placed and Timed", "novalty":"Novalty"} # get data

class input_dob(input_element):
    def __init__(self, *args, **kwords):
        super().__init__(*args, **kwords)
        self.template = "input_dob.html"

class input_submit(input_element):
    def __init__(self, display_name, **kwords):
        super().__init__(display_name, None, None, **kwords)
        self.template = "input_submit.html"


def check_data(data):
    form_data = data.form
    if len(form_data) == 0:
        return (False, "No data Values.")

    m = []
    for i in form_data:
        if form_data.get(i) == None or form_data.get(i) == "":
            m.append(i)
    if len(m) == 0:
        return (True,)

    return (False, "missing values for: %s" %m)
