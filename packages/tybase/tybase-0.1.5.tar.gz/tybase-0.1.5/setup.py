from setuptools import setup, find_packages

setup(
    name='tybase',
    version='0.1.5',
    include_package_data=True,
    description='新增获取当天日期字符串的代码',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # 版本描述
    author='Tuya',
    author_email='353335447@qq.com',
    url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'requests',
        "retrying",
        "pymysql",
        "mysql-connector-python",
        "sqlalchemy",
        "pandas",
        "langchain",
        "openai"
        # List your package dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
