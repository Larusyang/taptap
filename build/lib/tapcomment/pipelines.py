# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
import pymysql
import pymysql.cursors
import codecs
from twisted.enterprise import adbapi

class TapcommentPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def __init__(self,dbpool):
        self.dbpool = dbpool


    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)  # 调用插入的方法
        log.msg("-------------------连接好了-------------------")
        d.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        d.addBoth(lambda _: item)
        return d

    def _conditional_insert(self, conn, item, spider):
        log.msg("-------------------打印-------------------")
        sql =" insert into t_comment (game_id,game_name,game_rate,comment_author,author_verified,author_id,comment_id,comment_rate,comment_time,comment_phone,comment_content,comment_smile,comment_up,comment_down,comment_reply) values(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        parms =  (item['game_id'], item['game_name'], item['game_rate'],item['comment_author'],item['author_verified'],
                      item['author_id'],item['comment_id'],item['comment_rate'],item['comment_time'],item['comment_phone'],item['comment_content'],
                      item['comment_smile'],item['comment_up'],item['comment_down'],item['comment_reply'])
        conn.execute(sql,parms)

        log.msg("-------------------一轮循环完毕-------------------")
    def _handle_error(self, failue, item, spider):
        print(failue)
