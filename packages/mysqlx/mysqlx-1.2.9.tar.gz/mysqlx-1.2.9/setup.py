import os
from setuptools import setup, find_packages

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='mysqlx',
    packages=find_packages(),
    description="MySqlx is a simple python sql executor for MySQL like iBatis.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Jinja2>=3.0.3',
        'mysql-connector-python>=8.0.20',
    ],
    version='1.2.9',
    url='https://gitee.com/summry/mysqlx',
    author='summry',
    author_email='xiazhongbiao@126.com',
    keywords=['sql', 'MySQL', 'iBatis', 'MyBatis', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6.0',
    zip_safe=False
)

