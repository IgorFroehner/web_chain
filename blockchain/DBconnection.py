import os
import psycopg2


def connect():
    try:
        con = psycopg2.connect(os.environ['DATABASE_URL'])
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnect():
    if conn is not None:
        conn.close()
        print('Database connection lost')


conn = connect()
