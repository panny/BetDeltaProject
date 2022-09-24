#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
    Name:         RedisClient
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
import redis

sys.path.append("../")


class RedisClient(object):

    def __init__(self, **kwargs):
        self.db_prop = kwargs
        self.__conn = None

    def connection(self):
        if not self.__conn:
            pool = redis.ConnectionPool(host=self.db_prop.get('host', '127.0.0.1'),
                                        port=int(self.db_prop.get('port', '6379')),
                                        db=int(self.db_prop.get('database', '1')),
                                        password=self.db_prop.get('password', ''),
                                        decode_responses=True)
            self.__conn = redis.StrictRedis(connection_pool=pool)
        return self.__conn

    def set(self, name, value):
        conn = self.connection()
        conn.set(name=name, value=value)

    def expire(self, name, value, expire=60 * 60):
        conn = self.connection()
        return conn.set(name, value, expire)

    def get(self, name, value=None):
        conn = self.connection()
        if conn.exists(name):
            if conn.type(name) == 'set':
                return conn.smembers(name)
            elif conn.type(name) == 'hash':
                if value:
                    return conn.hget(name, value)
                else:
                    return conn.hgetall(name)
            elif conn.type(name) == 'zset':
                return conn.zrange(name, 0, -1)
            elif conn.type(name) == 'list':
                return conn.lrange(name, 0, -1)
            else:
                return conn.get(name)
        return None

    def delete(self, name):
        return self.connection().delete(name)

    def exists(self, name, value=None):
        conn = self.connection()
        if not value:
            return conn.exists(name)
        else:
            if conn.exists(name):
                if conn.type(name) == 'set':
                    return conn.sismember(name, value=value)
                elif conn.type(name) == 'hash':
                    return conn.hexists(name, key=value)
                else:
                    return False
            return False

    def len(self, name):
        conn = self.connection()
        if conn.exists(name):
            if conn.type(name) == 'set':
                return conn.scard(name)
            elif conn.type(name) == 'hash':
                return conn.hlen(name)
            elif conn.type(name) == 'list':
                return conn.llen(name)
        else:
            return 0


if __name__ == '__main__':
    client = RedisClient(database=2)
    client.connection().set('test', 'test', ex=60*60)
    print(client.get('test'))

