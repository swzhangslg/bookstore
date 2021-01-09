# bookstore

[![Build Status](https://travis-ci.com/swzhangslg/bookstore.svg?branch=master)](https://travis-ci.com/swzhangslg/bookstore)  [![codecov](https://codecov.io/gh/swzhangslg/bookstore/branch/master/graph/badge.svg?token=IF9UST4dK6)](https://codecov.io/gh/swzhangslg/bookstore)

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



将仓库克隆到本地：`git clone git@github.com:swzhangslg/bookstore.git`

新建并切换分支：`git checkout -b  <branch-name>`

在本地commit后将分支退到远程对应分支：`git push origin <branch-name>`

三个分支名为`deva`、`devb`与`devc`分别对应zsw、cy与dhy

分支合并：`git checkout master`	`git merge <branch-name>`

尽量现在自己分支上修改，不合并，商讨之后再合并

[关于分支的介绍](https://www.open-open.com/lib/view/open1328069889514.html)

[Git教程](https://www.liaoxuefeng.com/wiki/896043488029600)

其它说明见doc文件夹