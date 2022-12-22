from datetime import date
from config import host, user, password
import pymysql


class Database:
    def __init__(self, db_name):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit(True)

    def cbdt(self):
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS users
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        telegram_id INT UNIQUE NOT NULL ,
                        full_name TEXT,
                        username TEXT,
                        pay_end TEXT,
                        is_all_chats INT DEFAULT 1
                        );"""
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS keywords
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    word VARCHAR(512) UNIQUE NOT NULL
                    );
                """
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS unex_words
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    word VARCHAR(512) UNIQUE NOT NULL
                    );
                """
            cursor.execute(create)
            self.connection.commit()
        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS chats
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    chat VARCHAR(512) UNIQUE NOT NULL,
                    chat_num INT,
                    chat_title TEXT);
                """
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS users_chats
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    chat_id INT UNIQUE NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(chat_id) REFERENCES chats(id)
                    );
                """
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS users_keywords
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    keyword_id INT UNIQUE NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(keyword_id) REFERENCES keywords(id)
                    );
                """
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS users_unex_words
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    unex_word_id INT UNIQUE NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(unex_word_id) REFERENCES unex_words(id)
                    )"""
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS admins
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(512) UNIQUE NOT NULL
                    );
                    """
            cursor.execute(create)
            self.connection.commit()

    def create_user(self, telegram_id: int, full_name: str, username: str, pay_end):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''INSERT IGNORE INTO users (telegram_id, full_name, username,pay_end) VALUES(%s,%s,%s,%s) ''', (telegram_id, full_name, username, pay_end))
            self.connection.commit()

    def add_keyword(self, telegram_id: int, word: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''INSERT IGNORE INTO keywords(word) VALUES(%s)''', (word,))
            self.connection.commit()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id =(%s)", (telegram_id,))
            user_id = cursor.fetchall()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM keywords WHERE word =(%s)", (word,))
            keyword_id = cursor.fetchone()[0]
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT IGNORE INTO users_keywords(user_id, keyword_id) VALUES (%s,%s)', (user_id, keyword_id))
            self.connection.commit()
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT word
                    FROM keywords
                    WHERE id IN (SELECT keyword_id FROM users_keywords WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def add_unex_word(self, telegram_id: int, word: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT IGNORE INTO unex_words(word) VALUES(%s)', (word,))
            self.connection.commit()
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id = (%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "SELECT id FROM unex_words WHERE word = (%s)", (word,))
            keyword_id = cursor.fetchone()[0]
            cursor.execute(
                'INSERT IGNORE INTO users_unex_words(user_id, unex_word_id) VALUES (%s,%s)', (user_id, keyword_id))
            self.connection.commit()
            cursor.execute(
                '''SELECT word
                    FROM unex_words
                    WHERE id IN (SELECT unex_word_id FROM users_unex_words WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def add_chat(self, telegram_id: int, chat: str, chat_num: int = 1, chat_title=str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''INSERT IGNORE INTO chats(chat,chat_num,chat_title) VALUES(%s,%s,%s)''', (chat, chat_num, chat_title))
            self.connection.commit()
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id=(%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "SELECT id FROM chats WHERE chat=(%s)", (chat,))
            keyword_id = cursor.fetchone()[0]
            print(keyword_id)
            cursor.execute(
                'INSERT INTO users_chats(user_id, chat_id) VALUES (%s,%s)', (user_id, keyword_id))
            self.connection.commit()
            keywords = cursor.execute(
                '''SELECT chat_title
                    FROM chats
                    WHERE id IN (SELECT chat_id FROM users_chats WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            self.connection.commit()
            return [i[0] for i in keywords]

    def delete_all(self, telegram_id: int, table: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id = (%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                f'DELETE FROM {table} WHERE user_id = {user_id} ')
            self.connection.commit()

    def all_words(self, telegram_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT word
                    FROM keywords
                    WHERE id IN (SELECT keyword_id FROM users_keywords WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def all_unex_words(self, telegram_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT word
                    FROM unex_words
                    WHERE id IN (SELECT unex_word_id FROM users_unex_words WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def all_chats(self, telegram_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT chat_num
                    FROM chats
                    WHERE id IN (SELECT chat_id FROM users_chats WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def all_user_chats(self, telegram_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT chat_title
                    FROM chats
                    WHERE id IN (SELECT chat_id FROM users_chats WHERE user_id in (SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            chats = cursor.fetchall()
            return [i[0] for i in chats]

    def remove_keyword(self, telegram_id: int, keyword: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id = (%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "SELECT id FROM keywords WHERE word = (%s)", (keyword,))
            keyword_id = cursor.fetchone()[0]
            cursor.execute(
                f'DELETE FROM users_keywords WHERE user_id = {user_id} AND keyword_id ={keyword_id}')
            self.connection.commit()
            keywords = cursor.execute(
                '''SELECT word
                    FROM keywords
                    WHERE id IN (SELECT keyword_id FROM users_keywords WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0][:20] for i in keywords]

    def remove_keyword_(self,  keyword: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM keywords WHERE word = (%s)", (keyword,))
            self.connection.commit()

    def remove_unex_word(self, telegram_id: int, unex_word: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id = (%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "SELECT id FROM unex_words WHERE word = (%s)", (unex_word,))
            keyword_id = cursor.fetchone()[0]
            cursor.execute(
                'DELETE FROM users_unex_words WHERE user_id =%s AND unex_word_id =%s', (user_id, keyword_id))
            self.connection.commit()
            cursor.execute(
                '''SELECT word
                    FROM unex_words
                    WHERE id IN (SELECT unex_word_id FROM users_unex_words WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def remove_chat(self, telegram_id: int, chat: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE telegram_id = (%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "SELECT id FROM chats WHERE chat LIKE '%s'", (chat,))
            chat_id = cursor.fetchone()[0]
            cursor.execute(
                'DELETE FROM users_chats WHERE user_id = %s AND chat_id =%s', (user_id, chat_id))
            self.connection.commit()
            cursor.execute(
                '''SELECT chat
                        FROM chats
                        WHERE id IN (SELECT chat_id FROM users_chats WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            return [i[0] for i in keywords]

    def all_words_(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT word FROM keywords")
            words = cursor.fetchall()
            return [i[0] for i in words]

    def all_unex_words_(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT word FROM unex_words")
            words = cursor.fetchall()
            return [i[0] for i in words]

    def mailing_users(self, keywords, unex_words=tuple()):
        key = ', '.join(["'"+key+"'" for key in keywords])
        unex = ', '.join(unex_words)
        print(key, unex)
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT telegram_id
                        FROM users WHERE id IN
                        (SELECT user_id FROM users_keywords WHERE keyword_id
                        IN
                        (SELECT id FROM keywords WHERE word IN (%s)))""", key)
            uid = cursor.fetchall()
            cursor.execute(
                """SELECT id FROM keywords WHERE word IN (%s)""", key)
            print(cursor.fetchall())
            cursor.execute("""SELECT telegram_id
                        FROM users
                        WHERE id IN (SELECT user_id FROM users_unex_words WHERE unex_word_id
                        IN
                        (SELECT id FROM unex_words WHERE word IN (%s)))
                        ;""", unex)
            unex = cursor.fetchall()
            users = [i for i in uid if i not in unex]
            print(users, key, unex)
        return [i[0] for i in users]

    def add_chat_id(self, chat_id, chat):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'UPDATE chats SET chat_num={chat_id} WHERE chat="{chat}"')
            self.connection.commit()

    def add_chat_id(self, telegram_id, status):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'UPDATE chats SET is_all_chats={str(status)} WHERE telegram_id={telegram_id}')
            self.connection.commit()

    def get_status(self, telegram_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'SELECT is_all_chats FROM users WHERE telegram_id={telegram_id}')
            is_subs = cursor.fetchone()[0]
            return is_subs

    def set_status(self, telegram_id, status):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'UPDATE users SET is_all_chats={status} WHERE telegram_id={telegram_id}')
            self.connection.commit()

    def pay(self, username: str, end_date):
        with self.connection.cursor() as cursor:
            cursor.execute(
                'UPDATE users SET pay_end=%s WHERE username=%s', (end_date, username))
            self.connection.commit()

    def is_pay(self, telegram_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''SELECT pay_end FROM users WHERE telegram_id=%s''', telegram_id)
            pay_end = cursor.fetchone()[0]
            """По хорошему 
            переписать на проверку на
            типах данных DATETIME"""
        return str(pay_end) >= str(date.today())

    def add_admin(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''INSERT IGNORE INTO admins(username) VALUES (%s)''', username)
            self.connection.commit()

    def is_admin(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT username FROM admins")
            res = cursor.fetchall()
        return username in [i[0]for i in res]

    def get_chat_link(self, chat_id):
        with self.connection.cursor() as cursor:
            chat = cursor.execute(
                "SELECT chat FROM chats WHERE chat_num=%s", chat_id)
            chat = cursor.fetchone()[0]
            return chat


if __name__ == "__main__":
    a = Database("TopLid")
    a.cbdt()
