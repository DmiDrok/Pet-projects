class UserLogin:
    def is_authenticated(self):
        '''Проверка авторизации пользователя'''
        return True

    def is_active(self):
        '''Проверка активности пользователя'''
        return True

    def is_anonymous(self):
        '''Проверка неавторизации. False - если авторизован'''
        return False

    def get_id(self):
        '''Получение id пользователя. Возвращаться должна строка обязательно!'''
        return str(self.__user["id"])