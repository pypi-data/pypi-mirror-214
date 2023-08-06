import logging
import functools
from typing import Any, Union, Mapping, Sequence
from .support import DBCtx, ConnectionCtx, Dict, MultiColumnsError, TransactionCtx, try_commit, dynamic_sql, log, get_named_sql, get_named_args, page_log, LIMIT_1, DBError

_DB_CTX = None
_SHOW_SQL = False
_PK_SQL = 'SELECT LAST_INSERT_ID()'


def init_db(user='root', password='', database='test', host='127.0.0.1', port=3306, pool_size=8, use_unicode=True, show_sql=False, **kwargs):
    from mysql.connector import connect
    from mysql.connector.pooling import CONNECTION_POOL_LOCK
    global _DB_CTX
    global _SHOW_SQL

    with CONNECTION_POOL_LOCK:
        if _DB_CTX is not None:
            raise DBError('DB is already initialized.')

        _SHOW_SQL = show_sql
        if 'mapper_dir' in kwargs:
            del kwargs['mapper_dir']

        if pool_size >= 1:
            kwargs['pool_size'] = pool_size
            if 'pool_name' not in kwargs:
                kwargs['pool_name'] = "%s_pool" % database

        kwargs['user'] = user
        kwargs['password'] = password
        kwargs['database'] = database
        kwargs['host'] = host
        kwargs['port'] = port
        kwargs['use_unicode'] = use_unicode
        _DB_CTX = DBCtx(lambda: connect(**kwargs))

    if pool_size >= 1:
        logging.info('Init db engine <%s> ok with connection pool size: %d.' % (hex(id(_DB_CTX)), pool_size))
    else:
        logging.info('Init db engine <%s> ok without connection pool.' % hex(id(_DB_CTX)))


def connection():
    """
    Return _ConnectionCtx object that can be used by 'with' statement:
    with connection():
        pass
    """
    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.
    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    """

    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:
    with transaction():
        pass
    with transaction():
         insert(...)
         update(... )
    """
    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.
    @with_transaction
    def update_profile(id, name, rollback):
         u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
         insert('user', **u)
         r = update('update user set passwd=? where id=?', name.upper(), id)
    """
    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)
    return _wrapper


# ----------------------------------------------------------Update function------------------------------------------------------------------
def insert(table: str, **kwargs):
    """
    Execute insert SQL, return effect rowcount.
    :param table: table name
    :param kwargs: name='张三', age=20}
    return: Effect rowcount
    """
    logging.debug("Exec func 'mysqlx.db.%s' \n\t\t Table: '%s', kwargs: %s" % ('insert', table, kwargs))
    sql, args = _insert_sql_args(table.strip(), **kwargs)
    return do_execute(sql, *args)


@with_connection
def save(table: str, **kwargs):
    """
    Execute insert SQL, return primary key.
    :param table: table name
    :param kwargs: name='张三', age=20}
    :return: Primary key
    """
    logging.debug("Exec func 'mysqlx.db.%s' \n\t\t Table: '%s', kwargs: %s" % ('save', table, kwargs))
    global _DB_CTX
    cursor = None
    sql, args = _insert_sql_args(table.strip(), ** kwargs)
    sql = _before_execute('save', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        cursor.execute(_PK_SQL)
        result = cursor.fetchone()
        try_commit(_DB_CTX)
        return result[0]
    finally:
        if cursor:
            cursor.close()


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    log('db.execute', sql, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_execute(sql, *args)


def batch_insert(table: str, args: Sequence[Mapping[str, Any]]):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logging.debug("Exec func 'mysqlx.db.%s' \n\t\t Table: '%s', args: %s" % ('batch_insert', table, args))
    assert len(args) > 0, 'args must not be empty.'
    sql, args = _batch_insert_sql_args(table, args)
    return batch_execute(sql, args)


def batch_execute(sql: str, args: Union[Sequence[Sequence[Any]], Sequence[Mapping[str, Any]]]):
    """
    Batch execute
    :param sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
                INSERT INTO user(name, age) VALUES(:name,:age)  -->  args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :param args: All number must have same size.
    :return: Effect row count
    """
    logging.debug("Exec func 'mysqlx.db.%s' \n\t\t sql: '%s' \n\t\t args: %s" % ('batch_execute', sql, args))
    assert len(args) > 0, 'args must not be empty.'
    if isinstance(args[0], dict):
        sql, args = _batch_named_sql_args(sql, args)

    return do_batch_execute(sql, args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    log('db.get', sql, *args, **kwargs)
    global _DB_CTX
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    log('db.query', sql, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    log('db.query_one', sql, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    log('db.select', sql, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    log('db.select_one', sql, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_select_one(sql, *args)


def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('db.query_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('db.select_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = dynamic_sql(sql, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


# ----------------------------------------------------------Do function------------------------------------------------------------------
@with_connection
def do_execute(sql: str, *args):
    """
    Execute sql return effect rowcount
    sql: insert into user(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = _before_execute('do_execute', sql.strip(), *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_batch_execute(sql: str, args: Sequence[Sequence[Any]]):
    """
    Batch execute sql return effect rowcount
    :param sql: insert into user(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
    :param args: All number must have same size.
    :return: Effect rowcount
    """
    global _DB_CTX
    cursor = None
    sql = _before_execute('do_batch_execute', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    logging.debug("Exec func 'mysqlx.db.%s' \n\t\t sql: %s \n\t\t  args: %s" % ('do_get', sql, args))
    result = do_select_one(sql, *args)
    if result:
        if len(result) == 1:
            return result[0]
        msg = "Exec func 'mysqlx.db.%s' expect only one column but %d." % ('do_get', len(result))
        logging.error('%s  \n\t\t sql: %s \n\t\t args: %s' % (msg, sql, args))
        raise MultiColumnsError(msg)
    return None


@with_connection
def do_query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = _before_execute('do_select', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
            return [Dict(names, x) for x in cursor.fetchall()]
        else:
            return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict). Automatically add 'limit ?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql, args = _limit_one_sql_args(sql, *args)
    sql = _before_execute('do_query_one', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
            result = cursor.fetchone()
            return Dict(names, result) if result else result
        else:
            return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = _before_execute('do_select', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple). Automatically add 'limit ?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql, args = _limit_one_sql_args(sql, *args)
    sql = _before_execute('do_select_one', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()


def do_query_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = _page_sql_args(sql, page_num, page_size, *args)
    sql = _before_execute('do_query_page', sql.strip(), *args)
    return do_query(sql, *args)


def do_select_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = _page_sql_args(sql, page_num, page_size, *args)
    sql = _before_execute('do_select_page', sql.strip(), *args)
    return do_select(sql, *args)


def get_connection():
    global _DB_CTX
    if _DB_CTX.is_not_init():
        _DB_CTX.init()
    return _DB_CTX.connection


def prepare(prepared=True):
    global _DB_CTX
    _DB_CTX.prepared = prepared


def _before_execute(function: str, sql: str, *args):
    global _SHOW_SQL
    if _SHOW_SQL:
        logging.info("Exec func 'mysqlx.db.%s' \n\t\tSQL: %s \n\t\tARGS: %s" % (function, sql, args))
    return sql.replace('?', '%s')


def _insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = _create_insert_sql(table, cols)
    return sql, args


def _batch_insert_sql_args(table: str, args: Sequence[Mapping[str, Any]]):
    args = [zip(*arg.items()) for arg in args]  # [(cols, args)]
    cols, args = zip(*args)
    sql = _create_insert_sql(table, cols[0])
    return sql, args


def _batch_named_sql_args(sql: str, args: Sequence[Mapping[str, Any]]):
    args = [get_named_args(sql, **arg) for arg in args]
    sql = get_named_sql(sql)
    return sql, args


def _create_insert_sql(table: str, cols: Sequence[str]):
    return 'INSERT INTO `%s` (%s) VALUES (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['?' for _ in range(len(cols))]))


def _page_sql_args(sql: str, page_num=1, page_size=10, *args):
    if _require_limit(sql):
        sql = '%s limit ?,?' % sql
        start = (page_num - 1) * page_size
        args = [*args, start, page_size]
    return sql, args


def _limit_one_sql_args(sql: str, *args):
    if _require_limit(sql):
        return '%s limit ?' % sql, [*args, LIMIT_1]

    return sql, args


def _require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True

    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True

    return False
