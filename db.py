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

# class Users:
#     def __init__(self, conn):
#         self.conn = conn

#     def check_on_table_created(self):
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             SELECT table_name
#             FROM information_schema.tables
#             WHERE table_schema = 'public';
#         """)
#         tables = cursor.fetchall()
#         if tables:
#             for t in tables:
#                 if 'users' in t: return True
#         return False

#     def create_table(self):
#         cursor = self.conn.cursor()
#         cursor.execute('''CREATE TABLE users (
#             id serial PRIMARY KEY,
#             username VARCHAR(25) NOT NULL
#         );''')
#         self.conn.commit()

#     def add_user(self, username):
#         cursor = self.conn.cursor()
#         cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
#         id = cursor.fetchone()[0]
#         self.conn.commit()
#         return id

#     def get_id(self, username):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
#         # cursor.execute("SELECT * FROM users")
#         res = cursor.fetchone()
#         if res:
#             return res[0]

#     def drop_table(self):
#         cursor = self.conn.cursor()
#         cursor.execute("DROP TABLE users;")
#         self.conn.commit()

#     def __del__(self):
#         self.conn.close()

class Base:
    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name
        self.cursor = self.conn.cursor()

    def check_on_table_created(self):
        self.cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE (table_schema = 'public') ORDER BY table_schema, table_name;
        """)
        tables = cursor.fetchone()
        if tables:
            for t in tables:
                if self.table_name in t:
                    return True
        return False

    def create_table(self):
        self.cursor.execute('''CREATE TABLE {} (
            id serial PRIMARY KEY,
            url VARCHAR(50) UNIQUE,
            completed boolean DEFAULT false
        );'''.format(self.table_name))
        self.conn.commit()

    def add_folower(self, url):
        self.cursor.execute("""INSERT INTO {} (url) VALUES (%s);""".format(self.table_name), (url,))
        self.conn.commit()

    def set_is_completed(self, follower):
        self.cursor.execute("UPDATE {} SET completed = true WHERE url = %s;".format(self.table_name), (follower,))
        self.conn.commit()

    def set_all_is_not_completed(self):
        self.cursor.execute("UPDATE {} SET completed = false;".format(self.table_name))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM {} ORDER BY id;".format(self.table_name))
        return self.cursor.fetchall()

    def get_data_from_column_param(self, column, param):
        self.cursor.execute("SELECT * FROM {} WHERE {} = %s ORDER BY id;".format(self.table_name, column), (param,))
        return self.cursor.fetchall()

    def check_follower_in_db(self, follower):
        self.cursor.execute("SELECT * FROM {} WHERE url = %s;".format(self.table_name), (follower,))
        return self.cursor.fetchone()

    def check_is_completed(self, follower):
        self.cursor.execute("SELECT * FROM {} WHERE url = %s AND completed = true;".format(self.table_name), (follower,))
        return bool(self.cursor.fetchone())

    def drop_table(self):
        self.cursor.execute("DROP TABLE {} CASCADE;".format(self.table_name))
        self.conn.commit()

    def del_all(self):
        self.cursor.execute("DELETE FROM {};".format(self.table_name))
        self.conn.commit()

    def export_data(self):
        filename = input('Введите имя выходного файла, без расширения: ') + '.csv'
        folowers = [f[1] for f in self.get_all()]
        s = '\n'.join(folowers)
        with open(filename, 'w') as file:
            file.write(s)

    def import_data(self):
        filename = input('Введите имя импортируемого csv файла: ')
        if '.csv' not in filename:
            filename += '.csv'
        arr = []
        with open(filename, 'r') as file:
            arr = [line.replace('\n', '') for line in file.readlines()]
        for a in arr:
            self.cursor.execute("""INSERT INTO {} (url) VALUES (%s) ON CONFLICT DO NOTHING;""".format(self.table_name), (a,))

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
    import settings
    conn = connect_to_db(db='insta_poster', user='postgres', password='bad')
    folowers = Base(conn, settings.table_name)
    # print(folowers.get_data_from_column_param('id', 1963))
    # print(folowers.get_not_completed())
    # folowers.add_folower('sdvsdvsdv')
    # folowers.del_all()
    # print(folowers.get_not_completed())
    # folowers.drop_table()
    # folowers.create_table()
    # id = folowers.check_on_table_created()
    # print(id)
    # folowers.set_all_is_not_completed()
    # print(folowers.check_is_completed('sonplaying'))

    # print(folowers.get_all())
    # print(res)

    # folowers.import_folowers()
    # print(folowers.get_all())
    # folowers.export_folowers()
    # print(len(folowers.get_all()))
    # print(folowers.check_follower_in_db('anton.mairee'))
