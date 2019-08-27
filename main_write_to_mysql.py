import sys
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import redis
import MySQLdb
from qichacha_zhejiang.settings import mysql_config,redis_config

class WriteToMysql(object):
    def __init__(self):
        # 初始化redis连接
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                    password=redis_config['password'])
        self.r = redis.Redis(connection_pool=pool)
        # 初始化一个mysql连接

        self.mysql_db = MySQLdb.connect(host=mysql_config['host'], user=mysql_config['user'],
                                        passwd=mysql_config['passwd'],
                                        port=mysql_config['port'],
                                        db=mysql_config['db'])

        self.mysql_db.set_character_set('utf8')
        self.mysql_db.cursor().execute('SET NAMES utf8;')
        self.mysql_db.cursor().execute('SET CHARACTER SET utf8;')
        self.mysql_db.cursor().execute('SET character_set_connection=utf8;')


    def write_to_mysql(self):
        # while True:

        while True:
            fields = self.r.rpop(redis_config["fields"])


            if fields:
                # print(fields)
                try:
                    fields = bytes.decode(fields)
                    enterprise_name = fields.split("#@@#")[0]
                    fields = fields.split("#@@#")[1].split("####")

                    insert_sql = """insert into {}(enterprise_name,
                                                        Corporate_name,Representative,zczb,sjzb,jyzt,
                                                        clrq,tyshxydm,nsrsbh,zch,zzjgdm,
                                                        qylx,sshy,hzrq,djjg,ssdq,
                                                        ywm,cym,cbrs,rygm,yyqx,
                                                        qydz,jyfw) values
                                                        ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
                                                        '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
    
                                                                        """.format(mysql_config["table"], enterprise_name,
                                                                                   fields[0], fields[1], fields[2],
                                                                                   fields[3], fields[4], fields[5],
                                                                                   fields[6], fields[7],
                                                                                   fields[8], fields[9],
                                                                                   fields[10], fields[11], fields[12],
                                                                                   fields[13], fields[14], fields[15],
                                                                                   fields[16], fields[17],
                                                                                   fields[18], fields[19],
                                                                                   fields[20], fields[21]
                                                                                   )

                    # 放入mysql
                    self.mysql_db.cursor().execute(insert_sql)
                    self.mysql_db.commit()
                except:
                    print(len(fields))
                    pass
            else:
                break



if __name__ == '__main__':
    print("开始执行")
    wtm = WriteToMysql()

    # print(wtm)
    wtm.write_to_mysql()
    print("执行结束")
