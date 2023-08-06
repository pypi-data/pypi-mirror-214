import logging
from mysqlx import db
from config import DB_CONF

create_table_sql = '''
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `age` int NOT NULL,
  `birth_date` date DEFAULT NULL,
  `sex` tinyint DEFAULT NULL,
  `grade` float DEFAULT NULL,
  `point` double DEFAULT NULL,
  `money` decimal(8,4) DEFAULT NULL,
  `create_by` bigint DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_by` bigint DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `del_flag` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''


def create_truncate_table():
    cnt = db.do_get("SELECT count(1) FROM information_schema.TABLES WHERE table_schema=database() AND table_name='user'")
    if cnt == 0:
        db.execute(create_table_sql)
    else:
        db.execute('truncate user')


def drop_table():
    db.execute('DROP TABLE IF EXISTS user')


@db.with_transaction
def test_transaction(rollback: bool = False):
    db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert db.get('select count(1) from user limit 1') == 4, 'transaction'
    if rollback:
        1 / 0
    db.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)


def test_transaction2(rollback: bool = False):
    with db.transaction():
        db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
        assert db.get('select count(1) from user') == 6, 'transaction2'
        if rollback:
            1 / 0
        db.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)


def full_test():
    create_truncate_table()
    #######################################################################################################

    rowcount = db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert rowcount == 1, 'insert'
    assert db.get('select count(1) from user') == 1, 'insert'

    id2 = db.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
    assert id2 > 0, 'save'
    assert db.get('select count(1) from user') == 2, 'save'

    db.execute('update user set name=? where id=?', '王五', id2)
    assert db.get('select name from user where id=?', id2) == '王五', 'execute'

    db.execute('update user set name=:name where id=:id', name='赵六', id=id2)
    assert db.select_one('select id, name from user where id=:id', id=id2)[0] == id2, 'execute'

    db.execute('update user set name=:name where id=:id', name='赵六', id=id2)
    assert db.query_one('select name from user where id=:id', id=id2)['name'] == '赵六', 'execute'

    args = [
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56),
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56)
    ]
    db.batch_execute('insert into user(name, age, birth_date, sex, grade, point, money) values(?,?,?,?,?,?,?)', args)
    users = db.select('select id, del_flag from user')
    assert len(users) == 4, 'batch_execute'
    users = db.query('select id, del_flag from user')
    assert len(users) == 4, 'batch_execute'

    users = db.select('select id, del_flag from user where id=?', id2)
    assert len(users) == 1, 'select'
    users = db.query('select id, del_flag from user where id=?', id2)
    assert len(users) == 1, 'select'

    users = db.select('select id, del_flag from user where id=:id', id=id2)
    assert len(users) == 1, 'select'
    users = db.query('select id, del_flag from user where id=:id', id=id2)
    assert len(users) == 1, 'select'

    db.execute('delete from user where id=? limit 1', id2)
    assert db.get('select count(1) from user') == 3, 'execute delete'

    try:
        test_transaction(rollback=True)
    except Exception:
        print('Rollback.')
    assert db.get('select count(1) from user') == 3, 'transaction'

    test_transaction(rollback=False)
    assert db.get('select count(1) from user') == 5, 'transaction'

    try:
        test_transaction2(rollback=True)
    except Exception:
        print('Rollback.')
    assert db.get('select count(1) from user') == 5, 'transaction2'

    test_transaction2(rollback=False)
    assert db.get('select count(1) from user') == 7, 'transaction2'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    db.init_db(**DB_CONF, pool_size=2)
    # drop_table()
    full_test()

    # db.get('select * from user')

    for u in db.select('select * from user'):
        print(u)

    for u in db.select_page('select * from user', 2, 3):
        print(u)
