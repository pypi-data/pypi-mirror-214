from setuptools import setup, find_packages

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='mysqlx',
    packages=find_packages(),
    description="MySqlx is a simple python sql executor for MySQL like iBatis.",
    long_description_content_type=readme,
    install_requires=[
        'Jinja2>=3.0.3',
        'mysql-connector-python>=8.0.20',
    ],
    version='1.2.5',
    url='https://gitee.com/summry/mysqlx',
    author='summry',
    author_email='xiazhongbiao@126.com',
    keywords=['sql', 'MySQL', 'iBatis', 'MyBatis', 'python'],
    package_data={
        # include json and txt files
        '': ['*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6.0',
    zip_safe=False
)

