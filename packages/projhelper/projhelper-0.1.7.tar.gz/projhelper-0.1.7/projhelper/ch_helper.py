# -*- coding: utf-8 -*-
""" 
@File    : ch_helper
@Time    : 23/2/17 15:13
@Author  : jianhua.ou
"""
import time

import  pandas as pd
import re
import numpy as np

#pandas入到CH时， 转换成CH的类型
    #https://blog.csdn.net/weixin_42902669/article/details/109954641
# from juvo_tools.db_helper import DBHelper
from projhelper.log import logger


def _read_sql(client,sql):
    data, columns = client.execute(sql, columnar=True, with_column_types=True)
    df = pd.DataFrame({re.sub(r'\W', '_', col[0]): d for d, col in zip(data, columns)})
    return df

def _get_type_dict(client,database,table_name):

    sql = f"select name, type from system.columns where database = '{database}' and table='{table_name}';"
    df = _read_sql(client,sql)
    df = df.set_index('name')
    type_dict = df.to_dict('dict')['type']
    return type_dict

def valmap(func, d, factory=dict):
    """ Apply function to values of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    See Also:
        keymap
        itemmap
    """
    rv = factory()
    rv.update(zip(d.keys(), map(func, d.values())))
    return rv

def delete_ch(client,database,table_name,condition):
    #删除前检查，为0则不删除
    check_sql = f"select count(*) as cnt from {database}.{table_name} {condition} "
    # logger.debug("running sql {}".format(check_sql))
    result, columns = client.execute(check_sql, with_column_types=True)
    df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])

    # if df.iloc[0, 0] == 0:
    if df["cnt"][0] == 0 :
        logger.info(f"{database}.{table_name} : There is no record with condition,ignore mutation executeion")
        return True


    delete_sql = f"alter table {database}.{table_name} delete {condition}"
    result, columns = client.execute(delete_sql, with_column_types=True)
    logger.info(f"{database}.{table_name} success delete, sql : %s " % (delete_sql))

    #删除后检查
    cnt = 1
    while cnt > 0:
        result, columns = client.execute(check_sql, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        cnt = df["cnt"][0]
        logger.info(f"{database}.{table_name} wait delete finish , has rows:{cnt} !! ")
        # logger.info("has %s DDL running : %s.%s : %s " % (cnt, database, table, df["cmd"][0]))
        if cnt > 0:
            time.sleep(10)
    return True

    #参考 juvo-tool
    # def running_delete_juvo_tools(db_table,start_date,end_date):
    #     database,table_name=db_table.split(".")
    #     ch_db_info_tcp = dict(host=host,
    #                           port=port,
    #                           database=database,
    #                           user=user,
    #                           password=password)
    #
    #     db = ClickHouseDBHelper(ch_db_info_tcp)
    #     db.delete_by_mutation(database, table_name, __SPECIAL_CONDITION__="file_date >= toDate('%s') and file_date <= toDate('%s')" % (start_date, end_date))
    #

def pd_to_ch(client, df, database,table_name):
    type_dict = _get_type_dict(client,database,table_name)
    columns = list(type_dict.keys())
    # 类型处理
    try:
        for i in range(len(columns)):
            col_name = columns[i]
            col_type = type_dict[col_name]

            if 'Array' in col_type:
                pass
            elif 'Date' in col_type:
                df[col_name] = pd.to_datetime(df[col_name])
            elif 'UInt' in col_type:
                try:
                    df[col_name] = df[col_name].astype('uint64')
                except:
                    pass
            elif 'Int' in col_type:
                try:
                    df[col_name] = df[col_name].astype('Int64')
                except:
                    try:
                        df[col_name] = df[col_name].astype('int')
                    except:
                        pass
            elif 'Float' in col_type:
                df[col_name] = df[col_name].astype('float')
            elif 'Decimal' in col_type:
                df[col_name] = df[col_name].astype('float')
            elif 'String' in col_type:
                df[col_name] = df[col_name].astype('str').replace('nan', np.nan).replace('None', np.nan)
                # df[col_name] = df[col_name].astype('str')
    except BaseException as e:
        raise e
    # df数据存入clickhouse
    cols = ','.join(columns)
    data = df.to_dict('records')
    data = [
        valmap(lambda x: None if not isinstance(x, list) and (x is pd.NA or x is pd.NaT or pd.isna(x)) else x,
               e)
        for e in data]


    client.execute(f"INSERT INTO {database}.{table_name} ({cols}) VALUES", data, types_check=True)

if __name__ == '__main__':
    pass
    # from clickhouse_driver import Client
    # client = Client(host='host', port=9000, database='default', user='user', password='password')
    # pd_to_ch(client, df, db, table)
    # delete_ch(client, database, table_name, "where file_date >= toDate('%s') and file_date <= toDate('%s')" % (start_date, end_date))
