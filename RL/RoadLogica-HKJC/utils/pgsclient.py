#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
    Name:         PgsClient
    Description:  
    Email         wanglin1851@dingtalk.com
    Author:       Wang
    Time:         2019/11/25 18:17
-------------------------------------------------------------------------------
   Change Activity
                  2019/11/25 18:17
-------------------------------------------------------------------------------
"""
__author__ = 'Wang'

import sys
import copy
import datetime
import traceback
import psycopg2
import psycopg2.extras

sys.path.append("../")
from utils.logger import storage
from utils.settings import pgs
from DBUtils.PooledDB import PooledDB


class PostGreSql(object):

    def __init__(self, **kwargs):
        self.db_config = pgs
        self.db_config.update(kwargs)
        self._pool = None

    def get_pool_conn(self):
        if not self._pool:
            self._pool = self.init_pgs_conn()
        return self._pool.connection()

    def close_pool(self):
        if self._pool:
            self._pool.close()

    def init_pgs_conn(self):
        try:
            storage.info(
                'Begin to create {0} postgresql pool on：{1}.\n'.format(self.db_config['host'], datetime.datetime.now()))
            pool = PooledDB(creator=psycopg2,
                            maxconnections=6,
                            mincached=2,
                            maxcached=4,
                            maxshared=1,
                            blocking=True,
                            maxusage=None,
                            setsession=[],
                            ping=0,
                            host=self.db_config['host'],
                            port=int(self.db_config['port']),
                            user=self.db_config['user'],
                            password=self.db_config['password'],
                            database=self.db_config['database'],
                            cursor_factory=psycopg2.extras.RealDictCursor)
            storage.info('SUCCESS: create postgresql success.\n')
            return pool
        except Exception as e:
            storage.error('ERROR: create postgresql pool failed：{0}\n')
            self.close_pool()
            sys.exit('ERROR: create postgresql pool error caused by {0}'.format(str(e)))

    def fetchall(self, sql, *args):
        """
        查询返回全部结果
        :param sql:
        :param args:
        :return:
        """
        conn = self.get_pool_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            data = cursor.fetchall()
            return data
        except Exception as ex:
            storage.error('execute the sql：{}, raise the exception: {}\n{}'.format(sql, ex, traceback.format_exc()))
            return {}
        finally:
            cursor.close()
            conn.close()

    def fetchone(self, sql, *args):
        """
        查询返回单条结果
        :param sql:
        :param args:
        :return:
        """
        conn = self.get_pool_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, *args)
            data = cursor.fetchone()
            return data
        except Exception as ex:
            storage.error('execute the sql：{}, raise the exception: {}\n{}'.format(sql, ex, traceback.format_exc()))
        finally:
            cursor.close()
            conn.close()

    def fetchmany(self, sql, size, *args):
        """
        查询返回部分结果
        :param sql:
        :param size:
        :param args:
        :return:
        """
        conn = self.get_pool_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            data = cursor.fetchmany(size)
            return data
        except Exception as ex:
            storage.error('execute the sql：{}, raise the exception: {}\n{}'.format(sql, ex, traceback.format_exc()))
        finally:
            cursor.close()
            conn.close()

    def _execute(self, sql, *args):
        """
        执行_sql
        :param sql:
        :param args:
        :return:
        """
        conn = self.get_pool_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception as ex:
            storage.info('execute the sql：{}, raise the exception: \n{}'.format(sql, ex, traceback.format_exc()))
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def _execute_many(self, sql, *args):
        """
        sql
        :param sql:
        :param args:
        :return:
        """
        conn = self.get_pool_conn()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, args)
            conn.commit()
            return True
        except Exception as ex:
            storage.info('execute the sql：{}, raise the exception: \n{}'.format(sql, ex, traceback.format_exc()))
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_many(self, table, *values):
        """
        批量插入
        :param table: 表名
        :param values: 数据列表[{'key':'value'},]
        :return:
        """
        key_sql, val_sql, set_sql = PostGreSql._key_val_sql(values)
        _sql = "insert into {table} ({key_sql}) values ({val_sql})".format(table=table, key_sql=key_sql,
                                                                           val_sql=val_sql)
        resp = self._execute_many(_sql, *values)
        return resp

    def update(self, table, value, query):
        """
        根据条件更新列表
        :param table:
        :param value:
        :param query:
        :return:
        """
        key_sql = ' and '.join([f"{key}=\'{val}\'" for key, val in query.items()])
        val_sql = ','.join([f"{key}=\'{val}\'" for key, val in value.items()])
        _sql = f"update {table} set {val_sql} where {key_sql}"
        self._execute(_sql)

    def update_insert(self, table, values: [], primary_key: str):
        """
        批量插入
        :param table: 表名
        :param values: 数据列表[{'key':'value'},]
        :param primary_key: 唯一id
        :return:
        """
        key_sql, val_sql, set_sql = PostGreSql._key_val_sql(values, primary_key)
        if set_sql:
            _sql = "insert into {table} ({key_sql}) values ({val_sql}) on conflict({primary_key}) do update set {set_sql}".format(
                table=table,
                key_sql=key_sql, val_sql=val_sql, primary_key=primary_key, set_sql=set_sql)
            resp = self._execute_many(_sql, *values)
            return resp

    def update_insert_increase(self, table, values: {}, query_key: [], increase):
        """
        批量插入
        :param table: 表名
        :param values: 数据列表[{'key':'value'},]
        :param query_key: 过滤条件
        :param increase: 自增key
        :return:
        """
        key_sql = ' and '.join([f"{key}=\'{values[key]}\'" for key in query_key])
        _tmp = self.fetchone(f"select * from {table} where {key_sql}")
        if _tmp:
            values['id'] = _tmp.get('id')
            values[increase] = int(_tmp.get(increase)) + 1
            self.update_insert(table, [values], 'id')
        else:
            self.insert_many(table, *[values])

    def update_insert_query(self, table, values: [], query_key: []):
        """
        批量插入
        :param table: 表名
        :param values: 数据[{'key':'value'}]
        :param query_key: 过滤条件
        :return:
        """
        for value in values:
            key_sql = ' and '.join([f"{key}=\'{value[key]}\'" for key in query_key])
            _tmp = self.fetchone(f"select * from {table} where {key_sql}")
            if _tmp:
                values['id'] = _tmp.get('id')
                self.update_insert(table, *[value], 'id')
            else:
                self.insert_many(table, *[value])

    @staticmethod
    def _key_val_sql(values: list, primary_key: str = None):
        keys = copy.deepcopy(list(values[0].keys()))
        key_sql = ','.join(keys)
        val_sql = ','.join([f'%({key})s' for key in keys])
        if primary_key and primary_key in keys:
            keys.remove(primary_key)
            set_sql = ",".join([f"{key}=%({key})s" for key in keys])
            return key_sql, val_sql, set_sql
        return key_sql, val_sql, None


if __name__ == '__main__':
    sql = "select a.*,b.* from rank_record a, field b where a.rank_tag=b.rank_tag"
    data = PostGreSql().fetchall(sql)
    for dt in data:
        print(dt)
