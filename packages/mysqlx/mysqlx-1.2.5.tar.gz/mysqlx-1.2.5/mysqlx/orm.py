import sys
import logging
from . import db
from enum import IntEnum
from typing import Any, Mapping, Sequence
from datetime import datetime
from .support import LIMIT_1, DBError

NO_LIMIT = 0
DEFAULT_PK_FIELD = 'id'
SYMBOLS = ['=', '>', '<']
BETWEEN, LIKE, IN = 'between', 'like', 'in'
PK, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG = '__pk__', '__table__', '__update_by__', '__update_time__', '__del_flag__'


class DelFlag(IntEnum):
    UN_DELETE = 0
    DELETED = 1


class Model:
    """
    Use db.init_db(...) or dbx.init_db(...) init db first, then create a class extends Model:

    class User(Model):
        __pk__ = 'id'
        __table__ = 'user'
        __update_by__ = 'update_by'
        __update_time__ = 'update_time'
        __del_flag__ = 'del_flag'

        def __init__(self, id: int = None, name: str = None, age: int = None, update_by: int = None, update_time: datetime = None, del_flag: int = None):
            self.id = id
            self.update_by = update_by
            self.update_time = update_time
            self.del_flag = del_flag
            self.name = name
            self.age = age
    """

    def __str__(self):
        kv = {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
        return str(kv)

    def __getattr__(self, name):
        if PK == name:
            return self._get_pk()
        elif TABLE == name:
            return self._get_table()
        elif UPDATE_BY == name:
            return self._get_update_by_field()
        elif UPDATE_TIME == name:
            return self._get_update_time_field()
        else:
            return None

    def persist(self):
        """
        user = User(name='张三', age=55)
        id = user.persist()
        :return: Primary key
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % ('persist', self.__class__.__name__))
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        self.id = db.save(self._get_table(), **kv)
        return self.id

    def update(self):
        """
        user = User(id=1, name='李四', age=66)
        rowcount = user.update()
        :return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % ('update', self.__class__.__name__))
        pk, table = self._get_pk_and_table()
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        if pk not in kv:
            raise KeyError("Not primary key.")

        update_kv = {k: v for k, v in kv.items() if k != pk}
        if update_kv:
            return self.update_by_id(kv[pk], **update_kv)
        else:
            logging.warning("Exec func 'mysqlx.orm.Model.%s' not set fields, Class: '%s:'\n\t\t   %s" % ('update', self.__class__.__name__, self))
            return 0

    def load(self, *fields):
        """
        Return new object from database and update itself.
        :param fields: Default select all fields with 'select *' if not set. like: ('id', 'name', 'age')
        user = User(id=1)
        user2 = user.load()
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s', fields: %s" % ('load', self.__class__.__name__, fields))
        pk = self._get_pk()
        kv = self.__dict__
        _id = kv.get(pk)
        if _id is not None:
            if not fields:
                fields, _ = zip(*kv.items())
            m = self.query_by_id(_id, *fields)
            if m:
                self.__dict__.update(m)
                return self
            else:
                msg = "Exec func 'mysqlx.orm.Model.%s' load none, Class: '%s', %s=%d." % ('load', self.__class__.__name__, self._get_pk(), _id)
                logging.error(msg)
                raise DBError(msg)
        else:
            raise KeyError("Not primary key.")

    def delete(self):
        """
        Logic delete only update the del flag
        user = User(id=1)
        rowcount = user.delete()
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % ('delete', self.__class__.__name__))
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        update_by = self.__dict__.get(self._get_update_by_field())
        if _id is None:
            raise KeyError("Not primary key.")

        return self.delete_by_id(_id, update_by)

    def un_delete(self):
        """
        Logic un delete only update the del flag
        user = User(id=1)
        rowcount = user.un_delete()
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % ('un_delete', self.__class__.__name__))
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        update_by = self.__dict__.get(self._get_update_by_field())
        if _id is None:
            raise KeyError("Not primary key.")

        return self.un_delete_by_id(_id, update_by)

    def physical_delete(self):
        """
        Physical delete
        user = User(id=1)
        rowcount = user.physical_delete()
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % ('physical_delete', self.__class__.__name__))
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        if _id is None:
            raise KeyError("Not primary key.")

        return self.physical_delete_by_id(_id)

    # ----------------------------------------------------------Class method------------------------------------------------------------------
    @classmethod
    def insert(cls, **kwargs):
        """
        rowcount = User.insert(name='张三', age=20)
        return: Effect rowcount
        """
        _insert_log('insert', cls.__name__, **kwargs)
        table = cls._get_table()
        return db.insert(table, **kwargs)

    @classmethod
    def save(cls, **kwargs):
        """
        id = User.save(name='张三', age=20)
        :return: Primary key
        """
        _insert_log('save', cls.__name__, **kwargs)
        table = cls._get_table()
        return db.save(table, **kwargs)

    @classmethod
    def update_by_id(cls, _id: int, **kwargs):
        """
        rowcount = User.update_by_id(id=1, name='王五')
        return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, kwargs: %s" % ('update_by_id', cls.__name__, _id, kwargs))
        assert kwargs, 'Must set update kv'
        pk = cls._get_pk()
        where = '`%s`=?' % pk
        cols, args = zip(*kwargs.items())
        sql, update_time_arg = cls._update_sql(where, *cols)
        if update_time_arg:
            args = [*args, update_time_arg]
        return db.do_execute(sql, *args, _id, LIMIT_1)

    @classmethod
    def delete_by_id(cls, _id: int, update_by: int = None):
        """
        Logic delete only update the del flag
        rowcount = User.delete_by_id(id=1, update_by=100)
        return: Effect rowcount
        """
        _delete_by_id_log('delete_by_id', cls.__name__, _id, update_by)
        return cls._delete_by_id_op(_id, update_by, DelFlag.DELETED)

    @classmethod
    def un_delete_by_id(cls, _id: int, update_by: int = None):
        """
        Logic delete only update the del flag
        rowcount = User.un_delete_by_id(id=1, update_by=100)
        return: Effect rowcount
        """
        _delete_by_id_log('un_delete_by_id', cls.__name__, _id, update_by)
        return cls._delete_by_id_op(_id, update_by, DelFlag.UN_DELETE)

    @classmethod
    def delete_by_ids(cls, ids: Sequence[int], update_by: int = None, batch_size=128):
        """
        Logic delete only update the del flag
        rowcount = User.delete_by_ids(id=[1,2], update_by=100)
        return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, update_by: %s, batch_size: %s" % (
            'delete_by_ids', cls.__name__, ids, update_by, batch_size))
        return cls._delete_by_ids_op(ids, update_by=update_by, batch_size=batch_size, del_status=DelFlag.DELETED)

    @classmethod
    def un_delete_by_ids(cls, ids: Sequence[int], update_by: int = None, batch_size=128):
        """
        Logic delete only update the del flag
        rowcount = User.un_delete_by_ids(id=[1,2], update_by=100)
        return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, update_by: %s, batch_size: %s" % (
            'un_delete_by_ids', cls.__name__, ids, update_by, batch_size))
        return cls._delete_by_ids_op(ids, update_by=update_by, batch_size=batch_size, del_status=DelFlag.UN_DELETE)

    @classmethod
    def physical_delete_by(cls, where: str, *args):
        """
        Physical delete
        rowcount = User.physical_delete_by('where name=? and age=?', '张三', 55)
        return: Effect rowcount
        """
        _by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args)
        table = cls._get_table()
        sql = 'DELETE FROM `%s` %s' % (table, where)
        return db.do_execute(sql, *args)

    @classmethod
    def physical_delete_by_id(cls, _id: int):
        """
        Physical delete
        rowcount = User.physical_delete_by_id(id=1)
        return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d" % ('physical_delete_by_id', cls.__name__, _id))
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s`=? limit ?' % (table, pk)
        return db.do_execute(sql, _id, LIMIT_1)

    @classmethod
    def physical_delete_by_ids(cls, ids: Sequence[int], batch_size=128):
        """
        Physical delete
        rowcount = User.physical_delete_by_ids(id=[1,2])
        return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, batch_size: %s" % (
            'physical_delete_by_ids', cls.__name__, ids, batch_size))
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        if ids_size == 1:
            return cls.physical_delete_by_id(ids[0])
        elif ids_size <= batch_size:
            return cls._physical_delete_by_ids(ids)
        else:
            split_ids = _split_ids(ids, batch_size)
            with db.transaction():
                results = list(map(cls._physical_delete_by_ids, split_ids))
            return sum(results)

    @classmethod
    def batch_insert(cls, args: Sequence[Mapping[str, Any]]):
        """
        Batch insert
        rowcount = User.batch_insert([{'name': '张三', 'age': 55},{'name': '李四', 'age': 66}])
        :param args: All number must have same key.
        :return: Effect rowcount
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', args: %s" % ('batch_insert', cls.__name__, args))
        table = cls._get_table()
        return db.batch_insert(table, args)

    # ------------------------------------------------Class query method--------------------------------------------------------
    @classmethod
    def count(cls, **kwargs):
        """
        count = User.count(name='张三', age=55)
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', kwargs: %s" % ('count', cls.__name__, kwargs))
        where, args, _ = _get_where_arg_limit(**kwargs)
        fields = 'count(1)'
        sql = cls._select_sql(where, LIMIT_1, fields)
        return db.do_get(sql, *args, LIMIT_1)

    @classmethod
    def count_by(cls, where: str, *args):
        """
        Automatically add 'limit ?' where if not.
        count = User.count_by('where name=?', '李四')
        """
        _by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args)
        table = cls._get_table()
        sql = "SELECT count(1) FROM `%s` %s" % (table, where)
        return db.do_get(sql, *args)

    @classmethod
    def find(cls, *fields, **kwargs):
        """
        Return list(object) or empty list if no result.
        users = User.find('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', fields: %s, kwargs: %s" % ('find', cls.__name__, fields, kwargs))
        return [cls._dict2obj(d) for d in cls.query(*fields, **kwargs)]

    @classmethod
    def find_by(cls, where: str, *args):
        """
        Return list(dict) or empty list if no result.
        rows = User.find_by('where name=?', '李四')
        """
        _by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args)
        return [cls._dict2obj(d) for d in cls.query_by(where, *args)]

    @classmethod
    def find_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(object) or empty list if no result.
        users = User.find_page(1, 10, 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields with 'select *' if not set
        """
        _page_log('find_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        result = cls.query_page(page_num, page_size, *fields, **kwargs)
        return [cls._dict2obj(d) for d in result]

    @classmethod
    def find_by_page(cls, page_num: int, page_size: int, where: str, *args):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = User.find_by_page(1, 10, 'where name=?', '李四')
        """
        _page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args)
        return [cls._dict2obj(d) for d in cls.query_by_page(page_num, page_size, where, *args)]

    @classmethod
    def find_by_id(cls, _id: int, *fields):
        """
        Return one class object or None if no result.
        user = User.find_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, fields: %s" % ('find_by_id', cls.__name__, _id, fields))
        result = cls.query_by_id(_id, *fields)
        return cls._dict2obj(result) if result else None

    @classmethod
    def find_by_ids(cls, ids: Sequence[int], *fields):
        """
        Return list(class object) or empty list if no result.
        users = User.find_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, fields: %s" % ('find_by_ids', cls.__name__, ids, fields))
        return [cls._dict2obj(d) for d in cls.query_by_ids(ids, *fields)]

    @classmethod
    def query(cls, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        users = User.query('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', fields: %s, kwargs: %s" % ('query', cls.__name__, fields, kwargs))
        where, args, limit = _get_where_arg_limit(**kwargs)
        if not limit:
            limit = 1000

        sql = cls._select_sql(where, limit, *fields)
        return db.do_query(sql, *args, limit) if limit else db.do_query(sql, *args)

    @classmethod
    def query_by(cls, where: str, *args):
        """
        Return list(dict) or empty list if no result.
        rows = User.query_by('where name=?', '李四')
        """
        _by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args)
        table = cls._get_table()
        sql = "SELECT * FROM `%s` %s" % (table, where)
        return db.do_query(sql, *args)

    @classmethod
    def query_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        users = User.query_page(1, 10, 'id', 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields with 'select *' if not set
        """
        _page_log('query_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        where, args, _ = _get_where_arg_limit(**kwargs)
        sql = cls._select_sql(where, NO_LIMIT, *fields)
        return db.do_query_page(sql, page_num, page_size, *args)

    @classmethod
    def query_by_page(cls, page_num: int, page_size: int, where: str, *args):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = User.query_by_page(1, 10, 'where name=?', '李四')
        """
        _page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args)
        table = cls._get_table()
        sql = "SELECT * FROM `%s` %s" % (table, where)
        return db.do_query_page(sql, page_num, page_size, *args)

    @classmethod
    def query_by_id(cls, _id: int, *fields):
        """
        Return one row(dict) or None if no result.
        user = User.query_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, fields: %s" % ('query_by_id', cls.__name__, _id, fields))
        pk = cls._get_pk()
        where = 'WHERE `%s`=?' % pk
        sql = cls._select_sql(where, LIMIT_1, *fields)
        return db.do_query_one(sql, _id, LIMIT_1)

    @classmethod
    def query_by_ids(cls, ids: Sequence[int], *fields):
        """
        Return list(dict) or empty list if no result.
        users = User.query_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, fields: %s" % ('query_by_ids', cls.__name__, ids, fields))
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk = cls._get_pk()
        where = 'WHERE `%s` in (%s)' % (pk, ','.join(['?' for _ in range(ids_size)]))
        sql = cls._select_sql(where, ids_size, *fields)
        return db.do_query(sql, *ids, ids_size)

    @classmethod
    def select(cls, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = User.select('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', fields: %s, kwargs: %s" % ('select', cls.__name__, fields, kwargs))
        where, args, limit = _get_where_arg_limit(**kwargs)
        if not limit:
            limit = 1000

        sql = cls._select_sql(where, limit, *fields)
        return db.do_select(sql, *args, limit) if limit else db.do_select(sql, *args)

    @classmethod
    def select_by(cls, where: str, *args):
        """
        Return list(dict) or empty list if no result.
        rows = User.select_by('where name=?', '李四')
        """
        _by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args)
        table = cls._get_table()
        sql = "SELECT * FROM `%s` %s" % (table, where)
        return db.do_select(sql, *args)

    @classmethod
    def select_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = User.select_page('id', 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields with 'select *' if not set
        """
        _page_log('select_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        where, args, _ = _get_where_arg_limit(**kwargs)
        sql = cls._select_sql(where, NO_LIMIT, *fields)
        return db.do_select_page(sql, page_num, page_size, *args)

    @classmethod
    def select_by_page(cls, page_num: int, page_size: int, where: str, *args):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = User.select_by_page(1, 10, 'where name=?', '李四')
        """
        _page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args)
        table = cls._get_table()
        sql = "SELECT * FROM `%s` %s" % (table, where)
        return db.do_select_page(sql, page_num, page_size, *args)

    @classmethod
    def select_by_id(cls, _id: int, *fields):
        """
        Return one row(dict) or None if no result.
        row = User.select_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, fields: %s" % ('select_by_id', cls.__name__, _id, fields))
        pk = cls._get_pk()
        where = 'WHERE `%s`=?' % pk
        sql = cls._select_sql(where, LIMIT_1, *fields)
        return db.do_select_one(sql, _id, LIMIT_1)

    @classmethod
    def select_by_ids(cls, ids: Sequence[int], *fields):
        """
        Return list(dict) or empty list if no result.
        rows = User.select_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields with 'select *' if not set
        """
        logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, fields: %s" % ('select_by_ids', cls.__name__, ids, fields))
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk = cls._get_pk()
        where = 'WHERE `%s` in (%s)' % (pk, ','.join(['?' for _ in range(ids_size)]))
        sql = cls._select_sql(where, ids_size, *fields)
        return db.do_select(sql, *ids, ids_size)

    # ------------------------------------------------Private class method------------------------------------------------------------------
    @classmethod
    def _delete_by_id_op(cls, _id: int, update_by: int = None, del_status=DelFlag.DELETED):
        pk, table = cls._get_pk_and_table()
        del_flag_field = cls._get_del_flag_field()
        update_by_field = cls._get_update_by_field()

        where = '`%s`=?' % pk
        if update_by is not None and update_by_field is not None:
            sql, update_time_arg = cls._update_sql(where, del_flag_field, update_by_field)
            if update_time_arg:
                return db.do_execute(sql, del_status.value, update_by, update_time_arg, _id, LIMIT_1)
            return db.do_execute(sql, del_status.value, update_by, _id, LIMIT_1)
        else:
            sql, update_time_arg = cls._update_sql(where, del_flag_field)
            if update_time_arg:
                return db.do_execute(sql, del_status.value, update_time_arg, _id, LIMIT_1)
            return db.do_execute(sql, del_status.value, _id, LIMIT_1)

    @classmethod
    def _delete_by_ids_op(cls, ids: Sequence[int], update_by: int = None, batch_size=128, del_status=DelFlag.DELETED):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        if ids_size == 1:
            return cls._delete_by_id_op(ids[0], update_by, del_status)
        elif ids_size <= batch_size:
            return cls._do_delete_by_ids(ids, update_by, del_status)
        else:
            split_ids = _split_ids(ids, batch_size)
            with db.transaction():
                results = [cls._do_delete_by_ids(ids, update_by, del_status) for ids in split_ids]
            return sum(results)

    @classmethod
    def _do_delete_by_ids(cls, ids: Sequence[int], update_by: int = None, del_status=DelFlag.DELETED):
        ids_size = len(ids)
        pk = cls._get_pk()
        del_flag_field = cls._get_del_flag_field()
        update_by_field = cls._get_update_by_field()

        where = '`%s` in (%s)' % (pk, ','.join(['?' for _ in range(ids_size)]))
        if update_by is not None and update_by_field is not None:
            sql, update_time_arg = cls._update_sql(where, del_flag_field, update_by_field)
            if update_time_arg:
                return db.do_execute(sql, del_status.value, update_by, update_time_arg, *ids, ids_size)
            return db.do_execute(sql, del_status.value, update_by, *ids, ids_size)
        else:
            sql, update_time_arg = cls._update_sql(where, del_flag_field)
            if update_time_arg:
                return db.do_execute(sql, del_status.value, update_time_arg, *ids, ids_size)
            return db.do_execute(sql, del_status.value, *ids, ids_size)

    @classmethod
    def _physical_delete_by_ids(cls, ids: Sequence[int]):
        ids_size = len(ids)
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM `%s` WHERE `%s` in (%s) limit ?' % (table, pk, ','.join(['?' for _ in range(ids_size)]))
        return db.do_execute(sql, *ids, ids_size)

    @classmethod
    def _get_pk(cls):
        if hasattr(cls, PK):
            return cls.__pk__
        logging.warning("%s not set attribute '%s'" % (cls.__name__, PK))
        return DEFAULT_PK_FIELD

    @classmethod
    def _get_table(cls):
        if hasattr(cls, TABLE):
            return cls.__table__
        logging.warning("%s not set attribute '%s'" % (cls.__name__, TABLE))
        return _get_table_name(cls.__name__)

    @classmethod
    def _get_pk_and_table(cls):
        return cls._get_pk(), cls._get_table()

    @classmethod
    def _dict2obj(cls, dictionary):
        m = cls.__new__(cls)
        m.__init__(**dictionary)
        return m

    @classmethod
    def _get_update_by_field(cls):
        if hasattr(cls, UPDATE_BY):
            return cls.__update_by__
        return None

    @classmethod
    def _get_update_time_field(cls):
        if hasattr(cls, UPDATE_TIME):
            return cls.__update_time__
        return None

    @classmethod
    def _get_del_flag_field(cls):
        assert hasattr(cls, DEL_FLAG), "%s not set attribute '%s'" % (cls.__name__, DEL_FLAG)
        return cls.__del_flag__

    @classmethod
    def _select_sql(cls, where, limit, *fields):
        table = cls._get_table()
        if not fields:
            fields = '*'
        else:
            fields = ','.join(['%s' % col if '(' in col else '`%s`' % col for col in fields])

        if limit:
            return 'SELECT %s FROM `%s` %s limit ?' % (fields, table, where)
        else:
            return 'SELECT %s FROM `%s` %s' % (fields, table, where)

    @classmethod
    def _update_sql(cls, where, *update_fields):
        update_time_arg = None
        table = cls._get_table()
        update_time_field = cls._get_update_time_field()
        if update_time_field is not None and update_time_field not in update_fields:
            update_fields = [*update_fields, update_time_field]
            update_time_arg = datetime.now()

        update_fields = ','.join(['`%s`=?' % col for col in update_fields])
        return 'UPDATE `%s` SET %s WHERE %s limit ?' % (table, update_fields, where), update_time_arg


# ----------------------------------------------------------Private function------------------------------------------------------------------
def _get_condition_arg(k, v):
    if not isinstance(v, str):
        return "`%s`=?" % k, v

    v_lower = v.lower()
    if any([symbol in SYMBOLS for symbol in v_lower]):
        return "`%s`%s" % (k, v), None
    elif BETWEEN in v_lower or LIKE in v_lower or IN in v_lower:
        return "`%s` %s" % (k, v), None
    else:
        return "`%s`=?" % k, v


def _get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.get('limit')
        del kwargs['limit']

    if kwargs:
        conditions, args = zip(*[_get_condition_arg(k, v) for k, v in kwargs.items()])
        args = [arg for arg in args if arg is not None]
        where = 'WHERE %s' % ' and '.join(conditions)

    return where, args, limit


def _split_ids(ids: Sequence[int], batch_size):
    ids_size = len(ids)
    mod = ids_size % batch_size
    n = ids_size // batch_size
    if mod != 0:
        n += 1

    return [ids[i:i + batch_size] for i in range(0, ids_size, batch_size)]


def _get_table_name(class_name):
    for i in range(1, len(class_name) - 1)[::-1]:
        if class_name[i].isupper():
            class_name = class_name[:i] + '_' + class_name[i:]
    return class_name.lower()


def _page_log(function, page_num, page_size, class_name, where, *args):
    logging.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t\t Class: '%s', where: %s, args: %s" % (
        function, page_num, page_size, class_name, where, args))


def _by_page_log(function, page_num, page_size, class_name, *fields, **kwargs):
    logging.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t\t Class: '%s', fields: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, fields, kwargs))


def _insert_log(function, class_name, **kwargs):
    logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def _delete_by_id_log(function, class_name, _id, update_by):
    logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, update_by: %s" % (function, class_name, _id, update_by))


def _by_log(function, class_name, where, *args):
    logging.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', where: %s, args: %s" % (function, class_name, where, args))
