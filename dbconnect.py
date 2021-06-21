import mariadb
import dbcreds
import traceback


def get_db_connection():
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    except:
        print("Error connecting to DB!")
        traceback.print_exc()
        return None


def get_db_cursor(conn):
    try:
        return conn.cursor()
    except:
        print("Error creating cursor on DB!")
        traceback.print_exc()
        return None


def close_db_cursor(cursor):
    if(cursor == None):
        return True
    try:
        cursor.close()
        return True
    except:
        print("Error closing cursor on DB!")
        traceback.print_exc()
        return False


def close_db_connection(conn):
    if(conn == None):
        return True
    try:
        conn.close()
        return True
    except:
        print("Error closing connection to DB!")
        traceback.print_exc()
        return False
