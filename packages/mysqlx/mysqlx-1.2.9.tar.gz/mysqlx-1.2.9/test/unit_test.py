import unittest
import logging
from mysqlx import dbx
from config import DB_CONF
from db_test import full_test as db_test
from dbx_test import full_test as dbx_test
from orm_test import full_test as orm_test

logging.basicConfig(level=logging.INFO, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
dbx.init_db(**DB_CONF)


class MyTestCase(unittest.TestCase):

    def test_db(self):
        db_test()
        self.assertEqual(True, True)

    def test_dbx(self):
        dbx_test()
        self.assertEqual(True, True)

    def test_orm(self):
        orm_test()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
