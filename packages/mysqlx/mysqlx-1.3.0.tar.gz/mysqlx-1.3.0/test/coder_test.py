from config import DB_CONF
from mysqlx.coder import Coder


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    code = Coder(**DB_CONF)
    code.generate_with_schema(schema='investment', path='models')
    # code.generate_with_tables('user', path='models')

