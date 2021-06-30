import dbconnect
import traceback
import mariadb

def run_select_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    except mariadb.Error:
        traceback.print_exc()
        print("DB Error")

    
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_insert_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.lastrowid
    except mariadb.Error:
        traceback.print_exc()
        print("DB Error")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_delete_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except mariadb.Error:
        traceback.print_exc()
        print("DB Error")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_update_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except mariadb.Error:
        traceback.print_exc()
        print("DB Error")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result
