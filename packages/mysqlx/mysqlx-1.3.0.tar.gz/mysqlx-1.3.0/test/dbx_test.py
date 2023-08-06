from config import DB_CONF
from mysqlx import dbx
import logging
from test.db_test import create_truncate_table
from test import user_mapper


def full_test():
    create_truncate_table()
    #######################################################################################################

    rowcount = dbx.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert rowcount == 1, 'insert'
    assert dbx.get(user_mapper.user_count) == 1, 'insert'

    id2 = dbx.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert id2 > 0, 'save'
    assert dbx.get(user_mapper.user_count) == 2, 'save'

    dbx.execute(user_mapper.user_update, '王五', id2)
    assert dbx.get(user_mapper.select_name, id2) == '王五', 'execute'

    dbx.execute('user.user_update2', name='赵六', id=id2)
    assert dbx.query_one('user.named_select', id=id2)['name'] == '赵六', 'execute'

    print(dbx.select_one('user.named_select', id=id2))

    args = [
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56),
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56)
    ]
    dbx.batch_execute('user.batch_insert', args)
    users = dbx.select('user.select_all')
    assert len(users) == 4, 'batch_execute'
    users = dbx.query('user.select_all')
    assert len(users) == 4, 'batch_execute'

    users = dbx.select('user.named_select', id=id2)
    assert len(users) == 1, 'select'
    users = dbx.query('user.named_select', id=id2)
    assert len(users) == 1, 'query'

    users = dbx.select('user.select_name', id2)
    assert len(users) == 1, 'select'
    users = dbx.query('user.select_name', id2)
    assert len(users) == 1, 'query'

    users = dbx.select('user.named_select', id=id2)
    assert len(users) == 1, 'select'
    users = dbx.query('user.named_select', id=id2)
    assert len(users) == 1, 'query'

    dbx.execute('user.delete', id2)
    assert dbx.get('user.user_count') == 3, 'execute delete'

    args = [
        {'name': '李四', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56},
        {'name': '李四', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56}
    ]
    dbx.batch_insert('user', args)
    assert dbx.get('user.user_count') == 5, 'batch_insert'

    dbx.batch_execute('user.batch_insert2', args)
    assert dbx.get('user.user_count') == 7, 'batch_execute'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    dbx.init_db(**DB_CONF)

    full_test()

    for u in dbx.select_page('user.select_all', page_num=2, page_size=3):
        print(u)

    for u in dbx.query_page('user.select_all', page_num=2, page_size=3):
        print(u)


