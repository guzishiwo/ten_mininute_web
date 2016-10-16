## 数据库已初始化(包含大量图片链接，内容等）
账号： admin
密码： admin1234

### 爬取图片URL
spider/spider.py
获取**批量**url的脚本

### 项目运行方式
确保你的开发环境是 python3，如果不是，请考虑使用虚拟环境virtualenv&pyenv 搭建python3, 自行度娘并参照相关教程。

1. 命令行执行 pip install -r requirements.txt （注意包含coverage & django-nose)

2. 迁移数据库，在 manage.py 所在目录执行
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
3. 测试所有用例(确保所有测试用例通过）再启动第四步
    `python manage.py test website`
  
4. 在 manage.py 所在目录执行
    `python manage.py runserver`

5. 浏览器输入URL
    1. http://127.0.0.1:8000/  
    2. http://127.0.0.1:8000/login
    3. http://127.0.0.1:8000/logout  
    4. http://127.0.0.1:8000/register
    5. http://127.0.0.1:8000/articles
    6. http://127.0.0.1:8000/articles/2016/10/11/title
    7. http://127.0.0.1:8000/video/1
    8. http://127.0.0.1:8000/change_password
    9. http://127.0.0.1:8000/collect_videos
    10. http://127.0.0.1:8000/change_person_info

