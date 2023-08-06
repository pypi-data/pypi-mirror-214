from mysqlx import db
from config import DB_CONF
from mysqlx.orm import Model, DelFlag
from decimal import Decimal
from datetime import date, datetime
import logging
from db_test import create_truncate_table


class BaseModel(Model):
    __pk__ = 'id'
    __update_by__ = 'update_by'
    __update_time__ = 'update_time'
    __del_flag__ = 'del_flag'

    def __init__(self, id: int = None, update_by: int = None, update_time: datetime = None, del_flag: int = None, create_by: int = None,
            create_time: datetime = None):
        self.id = id
        self.update_by = update_by
        self.update_time = update_time
        self.del_flag = del_flag
        self.create_by = create_by
        self.create_time = create_time


class User(BaseModel):
    __table__ = 'user'

    def __init__(self, id: int = None, name: str = None, age: int = None, birth_date: date = None, sex: int = None, grade: float = None,
            point: float = None, money: Decimal = None, create_by: int = None, create_time: datetime = None, update_by: int = None,
            update_time: datetime = None, del_flag: int = None):
        super().__init__(id=id, create_by=create_by, create_time=create_time, update_by=update_by, update_time=update_time, del_flag=del_flag)
        self.name = name
        self.age = age
        self.birth_date = birth_date
        self.sex = sex
        self.grade = grade
        self.point = point
        self.money = money


def full_test():
    create_truncate_table()

    # ------------------------------------------------测试实例方法 ------------------------------------------------
    u = User(name='张三', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=Decimal(854.56))
    id = u.persist()
    assert User.count(name='张三') == 1, 'Count not eq 1'
    u1 = User(id=id, sex=1)
    u2 = u1.load('name', 'age')
    print(u1)
    print(u2)
    u1.load()
    print(u1)
    assert u1 == u2, 'u1 not eq u2'

    u1.name = '李四'
    u1.update()
    u3 = User.find_by_id(id, 'id', 'name')
    assert u3.name == '李四', 'update '

    u3.delete()
    u4 = User.find_by_id(id)
    assert User.count() == 1, 'delete'
    assert u4.del_flag == 1, 'delete'

    u4.physical_delete()
    assert User.count() == 0, 'physical_delete'

    # ------------------------------------------------测试静态方法------------------------------------------------------
    rowcount = User.insert(name='张三', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert rowcount == 1, 'insert'

    id2 = User.save(name='李四', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert id2 > 0, 'save'

    User.update_by_id(id2, name='王五')
    u5 = User.find_by_id(id2, 'name')
    assert u5.name == '王五', 'update_by_id'
    u5 = User.query_by_id(id2, 'name')
    assert u5['name'] == '王五', 'query_by_id'
    u5 = User.select_by_id(id2, 'name', 'age', 'create_time')
    print(u5)

    User.delete_by_id(id2)
    u6 = User.find_by_id(id2, 'del_flag')
    assert u6.del_flag == 1, 'logic_delete_by_id'
    User.un_delete_by_id(id2)
    u6 = User.find_by_id(id2, 'del_flag')
    assert u6.del_flag == 0, 'logic_delete_by_id'

    User.update_by_id(id2, del_flag=0)
    u7 = User.find_by_id(id2, 'del_flag')
    assert u7.del_flag == 0, 'update_by_id'

    users = User.find(name='王五')
    assert len(users) == 1, 'find'
    users = User.query(name='王五')
    assert len(users) == 1, 'query'
    users = User.select(name='王五')
    assert len(users) == 1, 'select'
    users = User.find('id', 'name', limit=2)
    assert len(users) == 2, 'find'
    ids = [user.id for user in users]
    User.delete_by_ids(ids=ids, batch_size=1)
    users2 = User.find_by_ids(ids, 'del_flag')
    assert len(users2) == 2, 'logic_delete_by_ids'
    for user in users2:
        assert user.del_flag == DelFlag.DELETED.value, 'logic_delete_by_ids'

    User.un_delete_by_ids(ids=ids, update_by=11)
    users2 = User.find_by_ids(ids, 'del_flag')
    assert len(users2) == 2, 'logic_un_delete_by_ids'
    for user in users2:
        assert user.del_flag == DelFlag.UN_DELETE.value, 'logic_delete_by_ids'

    User.physical_delete_by_id(id2)
    assert User.count() == 1, 'delete_by_id'

    User.physical_delete_by_ids(ids)
    assert User.count() == 0, 'delete_by_ids'


def get_attr():
    user = User(id=1, name='张三', age=41)
    user.logic_delete_by_id(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    db.init_db(**DB_CONF)

    full_test()

    # users = User.find('id', 'name', 'grade', 'create_time', id='in(1,4)', name="like '张三%'", grade='>=1', create_time="between '2023-06-07 10:48:01' and '2023-06-07 10:48:06'")
    # for user in users:
    #     print(user)
    # users = User.find()
    # for user in users:
    #     print(user)

    # sql = 'select * from user where name=%(name)s'
    # connection = db.get_connection()
    # try:
    #     cursor = connection.cursor()
    #     cursor.execute(sql, {'name': '张三', 'age': 6})
    #     result = cursor.fetchall()
    #     for r in result:
    #         print(r)
    # finally:
    #     if cursor:
    #         cursor.close()
    #     connection.close()

    # kwargs = {
    #     'name': '张三',
    #     'age': 18,
    #     'sex': 0
    # }
    # table = 'user'
    # cols, args = zip(*kwargs.items())
    # sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['%' + '(%s)' % col + 's' for col in cols]))
    # print(sql)

    # cls = User.__class__
    # user = cls(('test', Model, kwargs))
    # print(User)

    # for user in User.find():
    #     print(user)

    # now = datetime.now()
    # User.batch_insert([{'name': '王五', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56, 'create_time': now},
    #                    {'name': '赵六', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56, 'create_time': now}])

    # for u in User.query():
    #     print(u)

    for u in User.select_by_page(2, 3, 'where name=?', '张三'):
        print(u)

    for u in User.find_by_page(2, 3, 'where name=?', '张三'):
        print(u)

    # for u in User.query_page(2,3):
    #     print(u)
    #
    # for u in User.find_page(2,3):
    #     print(u)

    # rowcount = User.physical_delete_by('where name=? and age=?', '张三', 55)
    # print(rowcount)

    cnt = User.count_by('where name=?', '李四')
    print(cnt)
