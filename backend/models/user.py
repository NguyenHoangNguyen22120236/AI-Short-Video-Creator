class UserModel:
    _users = []

    def __init__(self, username, email, avatar=None):
        self.user_id = max((user.user_id for user in UserModel._users), default=0) + 1
        self.username = username
        self.email = email
        self.avatar = avatar

        UserModel._user_id += 1
        UserModel._users.append(self)
