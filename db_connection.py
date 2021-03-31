import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()

    return conn


def select_all_tasks(con):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = con.cursor()
    print(cur)
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(user):
    conn = None
    try:
        conn = sqlite3.connect('app.db')
        # print(sqlite3.version)
    except Error as e:
        print(e)


    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    #sql = f"INSERT INTO volunteers_users(first_name,last_name,city,mail,phone) VALUES({user['first_name']},{user['last_name']},{user['city']},{user['mail']},{user['phone']})"

    sql = f"INSERT INTO volunteers_users(first_name,last_name,city,mail,phone) VALUES(?,?,?,?,?)"
    values = (user['first_name'],user['last_name'],user['city'],user['mail'],user['phone'])

    cur = conn.cursor()
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    return cur.lastrowid


if __name__ == '__main__':
    database = r"app.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("2. Query all tasks")
        # select_all_tasks(conn)
        pass
