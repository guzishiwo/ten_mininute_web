
### 项目运行方式
确保你的开发环境是 python3，如果不是，请考虑使用虚拟环境virtualenv搭建python3, 自行度娘并参照相关教程。

1. 命令行执行 pip install -r requirements.txt （注意包含coverage & django-nose)
2. 迁移数据库，在 manage.py 所在目录执行
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
3. 测试所有用例(确保所有测试用例通过）在启动第四步
    `python manage.py test blog`
  
4. 在 manage.py 所在目录执行
    `python manage.py runserver`

5. 浏览器输入URL
    1. http://127.0.0.1:8000/  
    2. http://127.0.0.1:8000/detail

