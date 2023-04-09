from kakaodecrypt import KakaoDecrypt
import sqlite3
import json
import datetime
import time
import os

HOME_PATH = os.getenv('HOME')
DB_PATH = f'{HOME_PATH}/.local/share/waydroid/data/data/com.kakao.talk/databases/'

class KakaoDB:
    def __init__(self):
        self.con = sqlite3.connect(DB_PATH+'KakaoTalk.db')
        self.cur = self.con.cursor()
        self.cur.execute(f"ATTACH DATABASE '{DB_PATH}KakaoTalk2.db' AS db2")

    def get_column_info(self,table):
        try:
            self.cur.execute(f'SELECT * FROM ? LIMIT 1',[table])
            cols = [description[0] for description in self.cur.description]
            return cols
        except:
            return []

    def get_table_info(self):
        self.cur.execute(f"SELECT name FROM sqlite_schema WHERE type='table';")
        tables = [table[0] for table in self.cur.fetchall()]
        return tables

    def get_name_of_user_id(self,user_id):
        self.cur.execute(f"SELECT name,enc FROM db2.friends WHERE id=?",[user_id])
        res = self.cur.fetchall()
        for row in res:
            row_name = row[0]
            enc = row[1]
            dec_row_name = KakaoDecrypt.decrypt(enc, row_name)
            return dec_row_name

    def get_row_from_log_id(self,log_id):
        self.cur.execute(f"SELECT * FROM chat_logs WHERE id = ?",[log_id])
        res = self.cur.fetchall()
        return res[0]

    def clean_chat_logs(self,days):
        try:
            days = float(days)
            now = time.time()
            days_before_now = round(now - days*24*60*60)
            sql = f'delete from chat_logs where created_at < ?;'
            self.cur.execute(sql,[days_before_now])
            self.con.commit()
            res = f'{days:g}일 이상 지난 데이터가 삭제되었습니다.'
        except:
            res = f'요청이 잘못되었거나 에러가 발생하였습니다.'
        return res

    def log_to_dict(self,log_id):
        sql = f'select * from chat_logs where id = ?'
        self.cur.execute(sql,[log_id])
        descriptions = [d[0] for d in self.cur.description]
        rows = self.cur.fetchall()[0]
        return {descriptions[i] : rows[i] for i in range(len(descriptions))}
