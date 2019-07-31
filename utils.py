import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from qichacha_zhejiang.settings import mysql,file

class File_In_Out(object):
    def __init__(self):
        self.filepath = file

class Mysql_In_Out(object):
    def __init__(self):
        import MySQLdb
        conn = MySQLdb.connect(host=mysql['host'], port=mysql['port'], user=mysql['user'], passwd=mysql['passwd'],
                               use_unicode=True, encode='utf8')

        self.consor = conn.consor()

    def read_from_mysql(self):
        sql_str = "select * from {}".format(mysql['table'])
        datas = self.consor.execute(sql_str).fetch_all()
        return datas

    def write_to_redis(self):
        '''
        把从mysql读到的数据写入到redis中，redis的list队列中
        '''
        pass

    def read_from_redis(self):
        '''
        从redis中获得数据
        :return:
        '''
        pass
    def write_to_mysql(self):
        '''
        将解析处理后的结果放入到mysql
        :return:
        '''