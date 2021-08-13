import sqlite3


class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database=database_file)
        self.cursor=self.connection.cursor()

    def get_all_quotes(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `quotes`").fetchall()

    def get_quotes_by_user_id(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `quotes` WHERE `user_id`=?", (user_id,)).fetchall()

    def add_quote(self, user_id, quote,username):
        with self.connection:
            self.cursor.execute("INSERT INTO `quotes` (`user_id`,`quote`,`username`) VALUES(?,?,?)", (user_id, quote,username))

    def close(self):
        self.connection.close()