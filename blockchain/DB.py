import os
import psycopg2


def connect(verbose=False):
    try:
        if verbose:
            print('DB Connecting')
        con = psycopg2.connect(os.environ['DATABASE_URL'])
        if verbose:
            print('DB Connected')
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise (Exception('Error while connecting to DB: ' + str(error)))

# def disconnect():
#    if conn is not None:
#        conn.close()
#        print('Database connection lost')

