class User:

    def __init__(self, id_, username, password):
        self.id_ = id_
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User(id_={self.id_}, username="{self.username}", password="{self.password}")'

    def __str__(self):
        return f'User[id_={self.id_}, username="{self.username}", password="{self.password}"]'