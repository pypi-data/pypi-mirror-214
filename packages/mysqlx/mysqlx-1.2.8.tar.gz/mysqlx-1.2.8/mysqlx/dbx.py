import os
from . import db
from jinja2 import Template
from typing import Any, Union, Sequence, Mapping
from .support import simple_sql, SqlModel, log, page_log, MapperError, is_dynamic_sql
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_SQL_CONTAINER = dict()


def init_db(user='root', password='', database='test', host='127.0.0.1', port=3306, pool_size=8, use_unicode=True, show_sql=False,
            mapper_dir='mapper', **kwargs):
    _load_mapper(mapper_dir)
    db.init_db(user, password, database, host, port, pool_size, use_unicode, show_sql, **kwargs)


def insert(table: str, **kwargs):
    """
    Execute insert SQL, return effect rowcount.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    return: Effect rowcount
    """
    return db.insert(table, **kwargs)


def save(table: str, **kwargs):
    """
    Execute insert SQL, return primary key.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    :return: Primary key
    """
    return db.save(table, **kwargs)


def execute(sql_id: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.execute', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_execute(sql, *args)


def batch_insert(table: str, args: Sequence[Mapping[str, Any]]):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    return db.batch_insert(table, args)


def batch_execute(sql_id: str, args: Union[Sequence[Sequence[Any]], Sequence[Mapping[str, Any]]]):
    """
    Batch execute
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    sql = get_sql(sql_id)
    return db.batch_execute(sql, args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.get', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_get(sql, *args)


def query(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.query', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_query(sql, *args)


def query_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.query_one', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_query_one(sql, *args)


def select(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.select', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_select(sql, *args)


def select_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    log('dbx.select_one', sql, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_select_one(sql, *args)


def query_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    page_log('dbx.query_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_query_page(sql, page_num, page_size, *args)


def select_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql = get_sql(sql_id, **kwargs)
    page_log('dbx.select_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = simple_sql(sql, *args, **kwargs)
    return db.do_select_page(sql, page_num, page_size, *args)


def get_connection():
    return db.get_connection()


# ----------------------------------------------------------Load mapper--------------------------------------------------------------------
def _get_abs_path(path: str):
    parent_flg = '../'
    current_flg = './'
    if path.startswith(parent_flg):
        idx = path.rindex(parent_flg) + 3
        parent_path = path[:idx]
        os.chdir(parent_path)
        path = path[idx:]
    elif path.startswith(current_flg):
        path = path[2:]
    return os.path.join(os.getcwd(), path)


def _load_mapper(path: str):
    if not os.path.isabs(path):
        path = _get_abs_path(path)

    for f in os.listdir(path):
        file = os.path.join(path, f)
        if os.path.isfile(file) and f.endswith(".xml"):
            _parse_mapper_file(file)
        elif os.path.isdir(file):
            _load_mapper(file)


def _parse_mapper_file(file: str):
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = root.attrib.get('namespace', '')
    results = list(map(lambda child: _load_sql(namespace, child, file), root))
    sql_ids, file_includes = zip(*results)
    invalid_includes = [include for includes in file_includes if includes for include in includes if include not in sql_ids]
    if invalid_includes:
        raise MapperError("Includes %s are not exist in mapper file: %s" % (set(invalid_includes), file))


def get_sql(sql_id: str, **kwargs):
    sql_model = _get_sql_model(sql_id)
    if sql_model.includes:
        for include in sql_model.includes:
            assert include not in kwargs, "include: '%s' in kwargs: %s" % (include, kwargs)
            kwargs[include] = get_sql(_build_sql_id(sql_model.namespace, include), **kwargs)
    return sql_model.sql.render(**kwargs) if sql_model.dynamic else sql_model.sql


def _get_sql_model(sql_id: str):
    global _SQL_CONTAINER
    return _SQL_CONTAINER[sql_id]


def _build_sql_id(namespace, _id):
    return namespace + "." + _id


def _load_sql(namespace, child, file):
    global _SQL_CONTAINER
    # child.tag = select
    includes = None
    _id = child.attrib.get('id')
    assert _id, "Mapper 'id' must be set in mapper file: %s." % file
    sql_id = _build_sql_id(namespace, _id)
    assert sql_id not in _SQL_CONTAINER, "Sql id '%s' repeat." % sql_id
    include = child.attrib.get('include')
    sql = child.text.strip()
    if include:
        includes = include.split(",")
        for include in set(includes):
            assert include != _id, "Include must not be it self, id: '%s' = include: '%s' " % (_id, include)
        _SQL_CONTAINER[sql_id] = SqlModel(sql=Template(sql), namespace=namespace, dynamic=True, includes=includes)
    elif is_dynamic_sql(sql):
        _SQL_CONTAINER[sql_id] = SqlModel(sql=Template(sql), namespace=namespace, dynamic=True)
    else:
        _SQL_CONTAINER[sql_id] = SqlModel(sql=sql, namespace=namespace)

    return _id, includes

