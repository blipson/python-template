from collections import OrderedDict
from config import CONF, SCHEMA
from datetime import datetime
import sqlalchemy
import time

#gross global module state
DEBUG = CONF['app']['debug']

# helpful sql munging functions
null_or_empty = lambda x: x is None or len(str(x)) == 0
non_null_items = lambda xs: filter(lambda i: not null_or_empty(i[0]) and
                                   not null_or_empty(i[1]), xs)
all_empty = lambda xs: len(non_null_items(xs)) == 0
is_empty = lambda table, items: null_or_empty(table) or all_empty(items)
stringy = lambda s: any(type(s) == x for x in [str, unicode])
esc = lambda s: s.replace("'", '"')
sqlquotewrap = lambda x: "'"+esc(x)+"'" \
    if stringy(x) and not x == 'CURRENT_TIMESTAMP' else str(x)
like_or_eq = lambda s: ' like ' if stringy(s) and '%' in s else ' = '
histhandler = lambda hist: {} if hist is None else hist
now = lambda: 'T'.join(str(datetime.now()).split(' '))

__SCHEMA = SCHEMA['schema']
create_connection_string = lambda env: ''.join(
    [env['prefix'], env['username'], ':',
     env['password'], '@', env['url']] if 'oracle' in env['prefix'] else
    [env['prefix']])  # in-mem dbs just use the prefix

def create_db(conn_string):
    return sqlalchemy.create_engine(conn_string)

def reconfigure_db_engines(conf=CONF):
    global DBs
    DBs = create_db_engines(conf)


def create_db_engines(config):
    connectable = lambda env: reduce(lambda a, b: a and b,
                                     map(lambda x: not null_or_empty(x),
                                         env.values()))
    return {env['name']: newconn(create_db(create_connection_string(env)))
            for env in filter(connectable, config['environments'])}

def newconn(db, attempt=1, max_attempts=5, wait=5):
    try:
        print('connecting to: {}'.format(db))
        return db.connect()
    except Exception as e:
        print(str(e).strip())
        print('failed to connect to {}. Try #{}'.format(db, attempt))
        print('retrying in {} seconds...'.format(wait))
        if attempt == max_attempts:
            print('Retries exhausted. Killing self.')
            exit(1)
        else:
            time.sleep(wait)
            return newconn(db, attempt+1)

def run_query(env, query, attempt=1, max_attempts=5, wait=1):
    connection = DBs[env]
    try:
        if attempt == max_attempts:
            return []
        else:
            return connection.execute(query)
    except Exception as e:
        time.sleep(wait)
        return retryable_query(env, query)

DBs = {}
reconfigure_db_engines()