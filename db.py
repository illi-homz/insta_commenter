import psycopg2
from contextlib import closing

def connect_to_db(db, user, password):
    return psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host='localhost',
        port="5432"
    )

class Users:
    def __init__(self, conn):
        self.conn = conn

    def check_on_table_created(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        if tables:
            for t in tables:
                if 'users' in t: return True
        return False

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE users (
            id serial PRIMARY KEY,
            username VARCHAR(25) NOT NULL
        );''')
        self.conn.commit()

    def add_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        id = cursor.fetchone()[0]
        self.conn.commit()
        return id

    def get_id(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
        # cursor.execute("SELECT * FROM users")
        res = cursor.fetchone()
        if res:
            return res[0]

    def drop_table(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE users;")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class Folowers:
    def __init__(self, conn):
        self.conn = conn

    def check_on_table_created(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE (table_schema = 'public') ORDER BY table_schema, table_name;
        """)
        tables = cursor.fetchone()
        if tables:
            for t in tables:
                if 'folowers' in t: return True
        return False

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE folowers (
            id serial PRIMARY KEY,
            url VARCHAR(50) NOT NULL,
            completed boolean DEFAULT false
        );''')
        self.conn.commit()

    def add_folower(self, url):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO folowers (url)
            VALUES (%s);""", (url,)
        )
        self.conn.commit()

    def set_is_completed(self, follower):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE folowers SET completed = true WHERE url = %s;", (follower,))
        self.conn.commit()

    def set_all_is_not_completed(self):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE folowers SET completed = false;")
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM folowers;")
        return cursor.fetchall()

    def get_data_from_column_param_user(self, column, param):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM folowers WHERE {} = %s;".format(column), (param,))
        return cursor.fetchall()

    def check_follower_in_db(self, follower):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM folowers WHERE url = %s;", (follower,))
        # return bool(cursor.fetchone())
        return cursor.fetchone()

    def check_is_completed(self, follower):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM folowers WHERE url = %s AND completed = true;", (follower,))
        return bool(cursor.fetchone())
        # return cursor.fetchone()

    def drop_table(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE folowers CASCADE;")
        self.conn.commit()

    def del_all(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM folowers;")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


def get_data_from_table(conn, table):
    cursor = conn.cursor()
    cursor.execute("SELECT * from {}".format(table))
    return cursor.fetchall()

def drop_table(conn, table):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE {}".format(table))



if __name__ == '__main__':
    conn = connect_to_db(db='insta_poster', user='postgres', password='bad')

    # users = Users(conn)
    # print(users.get_id('Ilya'))
    # id = users.check_on_table_created()
    # print(id)
    # users.create_table()
    # users.drop_table()

    folowers = Folowers(conn)
    # print(folowers.get_data_from_column('completed', False))
    # print(folowers.get_not_completed())
    # folowers.add_folower(4, 'alla_gogaeva')
    # print(folowers.get_all())
    # folowers.del_all()
    # print(folowers.get_not_completed())
    # folowers.drop_table()
    # folowers.create_table()
    # id = folowers.check_on_table_created()
    # print(id)
    # folowers.set_all_is_not_completed()
    # print(folowers.check_is_completed('ellada_ioanidi.psy'))

    # print(folowers.check_follower_in_db('tattoo_darya_vl'))
