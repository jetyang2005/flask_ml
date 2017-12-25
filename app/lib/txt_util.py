# coding:utf-8
import sys
from app.lib.mysql_connectionpool_util import Mysql
reload(sys)
sys.setdefaultencoding('utf8')

# 每行求和
def addEachLine(line):
    values = line.split()
    values = [int(v) for v in values if v.strip()]
    return sum(values)

def main():
    result = []
    mysql = Mysql()
    with open("/Users/yangwm/log/station.txt") as f:
        buf = f.read()
        lines = buf.splitlines()

        #lines = [l.strip() for l in lines if l.split(',')]

        for l in lines:
             print l.split(',')
             insertSql = "insert into T_TEST_EARTHQUAKE values (%s,%s,%s,%s,%s,%s,%s)"
             insertSqlData = l.split(',')
             mysql.insertOne(insertSql,insertSqlData)
    mysql.dispose()
    # 打印结果
    # for r in result:
    #     print r

if __name__ == '__main__':
      main()
    # str="AH            AH                       ANQ                       \xe5\xae\x89\xe5\xba\x86                      117.02                            30.58                              75        "
    # lines = [l for l in str if l.strip()]
    # print lines