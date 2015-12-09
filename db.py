# Contains code used to connect to the database

from secret import DB_DSN
from exceptions import DuplicateError, NotFoundError

import psycopg2

UNIQUE_POSTGRES_CODE = '23505'


def drop_table(name):
    ''' drops the table 'name' if it exists '''
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
        browser TEXT
    """
    sql = 'create table visits ( \
            hash TEXT, \
            ts TIMESTAMP, \
            browser TEXT \
    )'
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def create_redirect(url, hashed):
    ''' create a new redirect object in db given url and hash '''
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
    '''
    returns an url from redirects given a hash.
    Raises NotFoundError if no such hash exists
    '''
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


def delete_hash(hashed):
    '''
    removes a hash from the db
    '''
    sql = "DELETE FROM redirects WHERE hash = %s;"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed,))
    conn.commit()
    cur.close()
    conn.close()


def add_visit(hashed, browser=None):
    ''' add a visit to /hashed in analytics table '''
    sql = "INSERT INTO visits (hash, ts, browser) VALUES(%s, CURRENT_TIMESTAMP, %s)"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed, browser))
    conn.commit()
    cur.close()
    conn.close()


def get_visits(hashed):
    ''' get number of visits to /hashed '''
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


def get_browser_counts(hashed):
    ''' get browser aggregation for /hashed '''
    sql = "SELECT browser, sum(1) FROM visits WHERE hash = %s GROUP BY browser;"
    conn = psycopg2.connect(dsn=DB_DSN)
    cur = conn.cursor()
    cur.execute(sql, (hashed,))
    conn.commit()
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return dict(rs)
