import datetime
import os

import mysql.connector


class db_table:
    
    con = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE'),
    )
    
    def __init__(self, tablename):
        self.cur = self.con.cursor()          
        self.tablename = tablename

    def close(self):
        self.con.close()

    def commit(self):
        self.con.commit()

    def commitClose(self):
        self.commit()
        self.close()        
    
    def getColumnNames(self):
        res = []
        self.cur.execute("SHOW COLUMNS FROM "+self.tablename)
        for v in self.cur:
            res.append(v[0])
        return res
    
    def getData(self, shot):
        sql = 'SELECT * FROM '+self.tablename+' WHERE shot=%s'
        self.cur.execute(sql, [shot])
        res = self.cur.fetchone()
        return res
    
    def regist_newshot_datetime(self, shot, colname, data):
        # shotの個所は新しいshotに
        # datetimeの個所は現在時刻に
        #print('shot, col, data', shot, colname, data)
        res = []
        for c, d in zip(colname, data):
            if 'created' == c or 'updated' == c:
                continue
            if 'shot' == c:
                res.append((c, shot))
                continue
            if 'datetime' == c:
                res.append((c, datetime.datetime.now()))
                continue
            res.append((c, d))
        
        # 要素が存在していれば削除
        if self.getData(shot) is not None:
            sql = 'DELETE FROM '+self.tablename+' WHERE shot=%s'
            self.cur.execute(sql, [shot])
            #print(sql)
            
        # 新規作成するSQLの作成
        sql = 'INSERT INTO '+self.tablename+' ('
        sqdata = []
        sqst = ""
        for e in res:
            c = e[0]
            v = e[1]
            sql += c+', '
            sqst += '%s, '
            sqdata.append(v)
        sql = sql[:-2]
        sqst = sqst[:-2]
        sql += ') VALUES ('+sqst+')'
        
        self.cur.execute(sql, sqdata)
        
        self.commit()
            
    
    def set_new_shot_data(self, shot):
        cols = self.getColumnNames()
        data = self.getData(shot)
        # shotがある場合は時刻を更新して保存
        if  data is not None:
            self.regist_newshot_datetime(shot, cols, data)
            return
        
        # 一つ前のデータがある場合はショット番号と時刻を更新
        data = self.getData(shot-1)
        if data is not None:
            self.regist_newshot_datetime(shot, cols, data)
            return
        
        data = [None]*len(cols)
        self.regist_newshot_datetime(shot, cols, data)
        return                    
        
