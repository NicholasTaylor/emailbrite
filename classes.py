class Org:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Event:
    def __init__(self, id, org_id, name, start_local, start_zulu, url):
        self.id = id
        self.org_id = org_id
        self.name = name
        self.start_local = start_local
        self.start_zulu = start_zulu
        self.url = url
    def is_future(self):
        from datetime import datetime
        if datetime.strptime(self.start_zulu, '%Y-%m-%dT%H:%M:%SZ') > datetime.utcnow():
            return True
        else:
            return False

class Contact:
    def __init__(self, first_name, email, optins):
        self.first_name = first_name
        self.email = email
        self.optins = optins
    def is_optin(self, orgid):
        return True if orgid in self.optins else False