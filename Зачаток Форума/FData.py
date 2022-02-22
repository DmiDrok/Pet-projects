import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash

class FData:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    ##Регистрация пользователя
    def RegUser(self, login, password):

        try:
            ##Проверка на уникальность логина
            sql = f"""SELECT login FROM users WHERE login == '{login}';"""
            self.__cursor.execute(sql)
            print("-------------------------", self.__cursor.fetchone())
            if self.__cursor.fetchone() != None: ##Если нашёлся такой же логин - возвращаем False
                return False

            ##Дата регистрации пользователя
            date_reg = datetime.now().strftime('%Y-%m-%d')

            sql = f"""INSERT INTO users (login, password, date_reg) VALUES ('{login}', '{password}', '{date_reg}');"""
            self.__cursor.execute(sql)
            self.__db.commit() ##Сохраняем изменения в БД
        except Exception as err:
            print(err)
            return False

        return True

    ##Добавление статей в БД
    def AddPost(self, title, content, tag, author):

        try:

            tag = tag.strip()

            if len(tag) < 2:
                tag = "Без тега"
            else:
                if "." in tag:
                    tag = tag.replace(".", "")
                elif "," in tag:
                    tag = tag.split(",")[0]
                elif " " in tag:
                    tag = tag.split(" ")[0]
                
                

            sql = F"""INSERT INTO posts (title, content, tag, author) VALUES ('{title}', '{content}', '{tag.lower()}', '{author}');"""
            self.__cursor.execute(sql)
            self.__db.commit() 
        except:
            return False

        return True

    ##Взятие всех статей из БД
    def GetPosts(self):

        try:
            sql = f"""SELECT * FROM posts ORDER BY id DESC"""
            self.__cursor.execute(sql)
            response = self.__cursor.fetchall()

            if response: ##Если есть ответ
                return response
        except:
            return False

        return []

    ##Взятие одной статьи из БД
    def GetPost(self, id):

        try:
            sql = f"""SELECT title, content, author FROM posts WHERE id == {id} LIMIT 1;"""
            self.__cursor.execute(sql)

            response = self.__cursor.fetchone()

            if response:
                return response

        except:
            return False
        
        return []

    ##Взятие определённых статей по тегу
    def GetOnTag(self, tag):

        try:

            sql = f"SELECT tag FROM posts WHERE tag == '{tag}'"
            self.__cursor.execute(sql)
            response = self.__cursor.fetchone()
            
            if response == None:
                return False

            sql = f"SELECT title, content, author, tag, id FROM posts WHERE tag == '{tag}'"
            self.__cursor.execute(sql)
            response = self.__cursor.fetchall()

            sql = f"SELECT count(id) FROM posts WHERE tag == '{tag}'"
            self.__cursor.execute(sql)
            count_posts = self.__cursor.fetchone()[0]
            
            if count_posts > 0:
                return response, count_posts

        except:
            return False

        return False

    ##Удаление статьи из БД
    def DeletePost(self, int:id):

        try:
            sql = f"DELETE FROM posts WHERE id == {{ id }}"

        except Exception as err:
            print(err)

    ##Проверка: есть ли учётная запись в БД
    def GetUser(self, login, password):

        try:
            sql = f"SELECT password FROM users WHERE login == '{login}' LIMIT 1;"
            self.__cursor.execute(sql)
            db_pass = self.__cursor.fetchone()[0]

            ##Проверка на равенство пароля пользователя из формы и пароля из БД


            return check_password_hash(db_pass, password)

        except:
            return False

        return False

    ##Кол-во постов от пользователя
    def GetNumPost(self, username):

        try:
            sql = f"""SELECT COUNT('{username}') FROM posts WHERE author == '{username}';"""

            self.__cursor.execute(sql)
            num_posts = self.__cursor.fetchone()[0]

        except Exception as err:
            print(err)
            return False

        return num_posts

    ##Дата регистрации пользователя
    def GetUserReg(self, username):
        
        try:
            sql = f"""SELECT date_reg FROM users WHERE login == '{username}';"""

            self.__cursor.execute(sql)
            date_reg = self.__cursor.fetchone()[0]

            if date_reg:
                return date_reg

        except Exception as err:
            print(err)
            return False

    ##Последняя выложенная статья пользователя
    def GetLatePost(self, username):

        try:
            sql = f"""SELECT max(ROWID), title, id FROM posts WHERE author == '{username}'"""

            self.__cursor.execute(sql)
            late_post = self.__cursor.fetchone()[1::]
            if late_post:
                return late_post

        except Exception as err:
            print(err)
            return False

