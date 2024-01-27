from model.user import User


class Twit:
    def __init__(self, body: str, author: User, id_twit: int):
        self.body = body
        self.author = author
        self.id_twit = id_twit
