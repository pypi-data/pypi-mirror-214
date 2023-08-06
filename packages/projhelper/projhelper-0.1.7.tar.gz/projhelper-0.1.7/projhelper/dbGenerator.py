#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
 @Time    : 19/3/1 15:47
 @Author  : oujianhua
 @mail  : ojhtyy@163.com
 @desc :
 '''
from __future__ import unicode_literals
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
import traceback
from urllib.parse import quote_plus
from projhelper.log import logger
import pymysql
pymysql.install_as_MySQLdb()
class Db:
    def __init__(self,s_db_con_str):
        self.engine = create_engine(s_db_con_str,
                                    echo=False,
                                    pool_size=1,
                                    pool_recycle=3600,
                                    pool_timeout=300,
                                    pool_pre_ping=True,
                                    max_overflow=-1)
        '''
        #连接池参数说明:
        #pool_size 最多缓存的连接数目  默认为10
        #pool_recycle 连接重置周期，单位 秒 :默认-1， 表示连接在给定时间之后会被回收，注意不要超过 MySQL 默认时长 8 小时
        #pool_timeout 等待 pool_timeout 秒，没有获取到连接之后，放弃从池中获取连接
        #pool_pre_ping (SQLAlchemy==1.2.0) 后支持该参数 : 每次有一个连接从连接池检出的时候， pre ping 会发出一个 “SELECT 1” 来检查 SQL 连接是否有效，如果有无效链接，则会重置此链接以及所有早于此连接的连接。
        # max_overflow 最多多几个连接，默认为10，意义是允许超过连接池限额即 poolsize 的数量，超过连接数限额 maxoverflow 之后不再允许创建新连接，而是要等待之前的连接完成操作。
                     #设置为"-1"，那么连接池会允许“上溢”无限多
        #实际最大连接数为 pool_size+max_overflow
        '''
        # DML操作加上事务 , 如果不加事务, 用engine.execute执行DML,默认是一个SQL一次提交
        Session = sessionmaker(bind=self.engine)  # 在 engine连接上绑定事务
        self.session = Session()
    #sql_before_exec=["set @@sql_log_bin = 1"])
    def execute_dml(self,s_sql,params=(),commit=1,sql_before_exec=[]):
        #try:
        # 中间有用 engine.execute 执行DML, 不影响session的事务
        try:
            for bef_sql in sql_before_exec:
                self.session.execute(bef_sql)
            res= self.session.execute(s_sql,params).rowcount
            if commit==1:
                self.session.commit()
            return res
        except BaseException as e:
            logger.error(traceback.format_exc())
            raise e
    #except:
    #    self.session.rollback()
    #返回结果格式　：　list是行, touple是列, 一个列也是touple  如:　[('USERS', 4388, 13), ('UNDOTBS1', 2, 0)］
    def execute_query(self,s_sql):
        try:
            return self.engine.execute(s_sql).fetchall()

        except BaseException as e:
            logger.error(traceback.format_exc())
            raise e
    #返回格式 : 字段:VAL  [{u'host': '%', u'user': 'monitoruser'}, {u'host': '%', u'user': 'replication'}]
    def execute_query_return_with_col(self,sql):
        #data=self.engine.execute(sql).fetchall()
        data = self.execute_query(sql)
        d_col_val = [dict(zip(result.keys(), result)) for result in data]
        return d_col_val
#获取多个DB
def get_multiDb(d_servicesDbStr):
    d_serviceAndDbconn={}
    for s_serviceName in d_servicesDbStr:
        #d_serviceAndDbconn[s_serviceName]=Db(d_servicesDbStr[s_serviceName])
        d_serviceAndDbconn[s_serviceName]=getDb(d_servicesDbStr[s_serviceName])
    return(d_serviceAndDbconn)

#获取一个DB
def getDb(url):
    try:
        db=Db(url)
        return (db)
    except BaseException as e:
        logger.error(traceback.format_exc())
        raise e


if __name__=='__main__':
    #oracle
    #import os
    #os.environ['ORACLE_HOME'] = '/oracle/app/oracle/product/11.2.0/dbhome_1'
    #os.environ['NLS_LANG'] = "#.UTF8"
    ##DB_CON_STR = 'oracle://user:host@localhost:1521/orcldb'
    #s_sql = text("select * from user_objects")

    #mysql 可以不指定 db
    #DB_CON_STR = 'mysql+mysqldb://user:pass@localhost:3306/mysql?charset=utf8'
    #quote_plus 解决密码有特殊字符
    DB_CON_STR = 'mysql+mysqldb://user:%s@localhost:3306/mysql?charset=utf8'%quote_plus('eff%1124&eee')
    s_sql = text("select user,host from mysql.user limit 2")

    #mssql
    #DB_CON_STR = 'mssql+pymssql://user:pass@localhost/ccds?charset=utf8'



    db=getDb(DB_CON_STR)

    #传参： https://www.adamsmith.haus/python/docs/sqlalchemy.orm.session.Session.execute
    s_sql = text(" update t set str=:str where id=:id")
    db.execute_dml(s_sql,{'str':'b','id':1})

    s_sql = text(" insert into t values(:id,:str)")
    db.execute_dml(s_sql,[{'id':2,'str':'b'},{'id':3,'str':'c'}])

    s_sql = text(" update t set str='cd' where id=1")
    db.execute_dml(s_sql,params=(),commit=1)



    l_rowsColsWithCol = db.execute_query_return_with_col(s_sql)


    l_rowsCols = db.execute_query(s_sql)

    for t_rowCols in l_rowsCols:
        for col in t_rowCols:
            print (col,)
    #转成  [{u'host': u'%', u'user': u'alog_kettle'}xxx] 格式
    ld_colVals = [dict(zip(result.keys(), result)) for result in l_rowsCols]
    print(ld_colVals)