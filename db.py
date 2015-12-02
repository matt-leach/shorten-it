from secret import DB_DSN
import psycopg2

UNIQUE_POSTGRES_CODE = '23505'


class DuplicateError(Exception):
    pass


class NotFoundError(Exception):
    pass


def drop_table(name):
    """
    drops the table 'name' if it exists
    """
    sql = 'drop table if exists {};'.format(name)
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def create_redirects_table():
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


def create_visits_table():
    """
    creates a postgres table 'visits' with columns
        hash TEXT,
        ts TIMESTAMP
    """
    sql = 'create table visits ( \
            hash TEXT, \
            ts TIMESTAMP \
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
    ''' returns an url from redirects given a hash. Raises NotFoundError if no such hash exists '''
    sql = "SELECT original_url FROM redirects WHERE hash = %s;"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed,))
    conn.commit()
    rs = cur.fetchall()
    cur.close()
    conn.close()
    if len(rs) == 1:
        return rs[0][0]
    else:
        raise NotFoundError


def add_visit(hashed):
    sql = "INSERT INTO visits (hash, ts) VALUES(%s, CURRENT_TIMESTAMP)"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed, ))
    conn.commit()
    cur.close()
    conn.close()


def get_visits(hashed):
    sql = "SELECT count(*) FROM visits WHERE hash = %s;"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed,))
    conn.commit()
    rs = cur.fetchall()
    count = rs[0][0]

    cur.close()
    conn.close()
    return count
