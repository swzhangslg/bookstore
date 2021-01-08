# bookstore

[![Build Status](https://travis-ci.com/swzhangslg/bookstore.svg?branch=master)](https://travis-ci.com/swzhangslg/bookstore)[![codecov](https://codecov.io/gh/swzhangslg/bookstore/branch/master/graph/badge.svg?token=IF9UST4dK6)](https://codecov.io/gh/swzhangslg/bookstore)

在init_database.py和be/db_conn.py两个文件中改连接数据库的密码

建库：`python init_database.py`

测试：

```
cd fe/test
coverage run -m pytest
coverage report
```

测试：

```
bash script/test.sh
```



