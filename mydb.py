import pymysql


dbsetting = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'yhgood',
    'password':'987654321',
    'db':'yongheSoyMilk',
    'charset':'utf8'
    }

conn = pymysql.connect(**dbsetting)