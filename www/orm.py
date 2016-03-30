#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

___author__='liuxsde'

import asyncio,logging
import aiomysql

def log(sql,args=()):
    logging.info('SQL:%s'%sql)

#创建连接池,由全局变量_pool存储
async def create_pool(loop,**kw):
    logging.info('create database connecting pool...')
    global __pool
    __pool=await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf-8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop

    )

#用函数封装select(使用带参数的sql,而不是自己拼接)
async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?','%s'),args or ())
            if size:
                rs=await cur.fetchmany(size)
            else:
                rs=await cur.fetchall()
        logging.info('rows returned:%s'%len(rs))
        return rs

#通用execute函数,执行insert/delete/update
async def execute(sql,args,autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?','%s'),args)
                affected=cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

#定义model和子类
def create_args_string(num):
    L=[]
    for n in range(num):
        L.append('?')
    return ','.join(L)

class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default
    def __str__(self):
        return '<%s,%s:%s>'%(self.__class__.__name__,self.column_type,self.name)

class StringField(Field):
    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
    


