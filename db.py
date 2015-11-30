from secret import DB_DSN
import psycopg2

UNIQUE_POSTGRES_CODE = '23505'


class DuplicateError(Exception):
    pass


class NotFoundError(Exception):
    pass


def drop_table():
    """
    drops the table 'redirects' if it exists
    """
    sql = 'drop table if exists redirects;'
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
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
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
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
        if e.pgcode == UNIQUE_POSTGRES_CODE:
            raise DuplicateError()
        else:
            raise
    else:
        cur.close()
        conn.close()


def get_redirect(hashed):
    ''' returns an url from redirects given a hash. Riases NotFoundError if no such hash exists '''
    sql = "SELECT original_url FROM redirects WHERE hash = %s;"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed,))
    conn.commit()
    rs = cur.fetchall()
    if len(rs) == 1:
        return rs[0][0]
    else:
        raise NotFoundError

    cur.close()
    conn.close()
