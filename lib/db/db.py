from os.path import isfile
from sqlite3 import connect

DB_PATH = './data/db/database.db'
BUILD_PATH = './data/db/build.sql'

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    
    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

def commit():
    cxn.commit()

def close():
    cxn.close()

def field(cmd, *values):
    cur.execute(cmd, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]

def record(cmd, *values):
    cur.execute(cmd, tuple(values))

    return cur.fetchone()

def records(cmd, *values):
    cur.execute(cmd, tuple(values))

    return cur.fetchall()

def column(cmd, *values):
    cur.execute(cmd, tuple(values))

    return [item[0] for item in cur.fetchall()]

def execute(cmd, *values):
    cur.execute(cmd, tuple(values))

def multiexec(cmd, valueset):
    cur.executemany(cmd, valueset)

def scriptexec(path):
    with open (path, 'r', encoding='utf-8') as script:
        cur.executescript(script.read())