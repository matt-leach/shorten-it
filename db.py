from secret import DB_DSN
import psycopg2


def drop_table():
    """
    drops the table 'redirects' if it exists
    """
    try:
        sql = 'drop table if exists redirects;'
        conn = psycopg2.connect(dsn=DB_DSN)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as e:
        print e.message
    else:
        cur.close()
        conn.close()


def create_table():
    """
    creates a postgres table 'redirects' with columns
        original_url TEXT,
        hash TEXT UNIQUE,
    """
    sql = 'create table redirects ( \
            original_url TEXT, \
            hash TEXT UNIQUE \
    )'
    try:
        conn = psycopg2.connect(dsn=DB_DSN)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as e:
        print e.message
    else:
        cur.close()
        conn.close()


def create_redirect(url, hashed):
    try:
        sql = "INSERT INTO redirects (original_url, hash) VALUES(%s, %s)"
        conn = psycopg2.connect(dsn=DB_DSN)
        cur = conn.cursor()
        cur.execute(sql, (url, hashed))
        conn.commit()

    except psycopg2.Error as e:
        print e.message
    else:
        cur.close()
        conn.close()
