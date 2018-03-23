class LeftChatMember:

    def __init__(self, uid, first_name, last_name, date):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.date = date

    def __repr__(self):
        return "uid: {}, first_name: {}, last_name: {}, date: {}"\
            .format(self.uid, self.first_name, self.last_name, self.date)