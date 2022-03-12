class UserLogin():
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    ##Берём все атрибуты пользователя
    def get_user(self, table, user_id):
        self.__user = table.query.filter_by(id=user_id).first()
        print(self.__user, type(self.__user), sep="\n\n")
        return self

    ##Берём айди пользователя
    def get_id(self):
        return str(self.__user.id)

    ##Для дальнейшей авторизации пользователя
    def create_user(self, user):
        self.__user = user
        return self