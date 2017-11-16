# -*- coding: utf-8 -*-
import sqlite3 as lite
import time


class SqlLiteDb:

    def __init__(self):
        self.con = lite.connect("marshalas.db")
        self.con.row_factory = self.__dict_factory
        self.cur = self.con.cursor()

    def init_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS quotes (quote TEXT, added_by TEXT, added INT)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS giphy_keywords (keyword TEXT, search_term TEXT)')
        self.con.commit()

    def close(self):
        if self.con:
            self.con.close()

    def get_random_quote(self):
        self.cur.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;')
        return self.cur.fetchall()

    def insert_quote(self, quote, added_by):
        self.cur.execute('INSERT INTO quotes (quote, added_by, added) VALUES (?,?,?)', (quote, added_by, time.time()))

    def get_giphy_keywords(self):
        self.cur.execute('SELECT * FROM giphy_keywords')
        return self.cur.fetchall()


    # private method
    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d