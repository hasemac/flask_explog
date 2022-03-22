from datetime import datetime

from apps.app import db
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text


class One_info:
    html = None # html name
    val = None
    pname = None    # printing name
    dbc = None      # databese column
    editable = None
    htype = None
    width = None
    height = None

class Class_info:
    Model_class = None
    
    #[("print_name", colspan),,]
    header = None
    
    # [(html_name, printing_name, db, editable, edit_type, width, height),,]
    colinf = None
    
    # array of One_info
    tbinf = None
    def __init__(self, Model_class):
        self.Model_class = Model_class
        self.set_table_info()
        
    def set_table_info(self):
        cinf = []
        for e in self.colinf:
            f = One_info()
            f.html = e[0]
            f.pname = e[1]
            f.dbc = e[2]
            f.editable = e[3]
            if f.editable:
                f.htype = e[4]
                if 6 <= len(e):
                    f.width = e[5]
                if 7 <= len(e):
                    f.height = e[6]
            cinf.append(f)

        self.tbinf = cinf

    def get_db_columns(self):
        a = []
        for e in self.tbinf:
            a.append(e.dbc)
        a = tuple(a)
        return a    

    def set_one_val(self, htmlname, val):
        for e in self.tbinf:
            if htmlname == e.html:
                e.val = val

            
    def clear_val(self):
        # 文字列で初期化-htmlで表示するのが殆ど
        for e in self.tbinf:
            # e.val = None
            e.val = ""                    
                                
    def get_html_header(self):
        h = self.header.copy()
        res = []
        for e in self.tbinf:
            res.append((e.pname, 1))
        h.append(res)
        return h
    
    # 1つのrecordの取得
    def get_record(self, sh):
        #cl = tuple([e.dbc for e in self.cinf])
        cl = self.get_db_columns()
        q = db.session.query(*cl).filter(self.Model_class.shot == sh).all()
        return q        

    def get_html_fields(self, sh):
        q = self.get_record(sh)
        if 0 == len(q):
            # データベースに該当するショットがない場合
            # 値をすべてクリア
            self.clear_val()
            self.set_one_val("shot", sh)
            
            q = self.get_record(sh-1)
            if 0 != len(q):
                # 一つ前のショットでデータがある場合
                # editableの個所をコピーする。
                q = q[0]
                for c, v in zip(self.tbinf, q):
                    if c.editable:
                        c.val = v
        else:
            q = q[0]
            for c, v in zip(self.tbinf, q):
                c.val = v            
        
        # Noneの要素は""に変更
        for e in self.tbinf:
            if None == e.val:
                e.val = ""
                
        return self.tbinf
    
    def get_data(self, sh_start, sh_end):
        cl = self.get_db_columns()
        q = db.session.query(*cl).filter(self.Model_class.shot >= sh_start, self.Model_class.shot <= sh_end).all()

        # Noneを""に変更して、html上でNoneと表示されないようにする。
        q = [tuple([e if None != e else "" for e in a])
             for a in q]
        
        return q

    def get_new_class(self, request_form):
        d = {}
        # get html key names
        keys = []
        for e in self.tbinf:
            keys.append(e.html)
            
        for e in keys:
            #print("key", e, " val", request_form.get(e))
            v = request_form.get(e)
            if "" == v:
                continue
            d[e] = request_form.get(e)
        return self.Model_class(**d)   
class Comment(db.Model):
    __tablename__='comment'
    shot = db.Column('shot', db.Integer, primary_key=True, autoincrement=False)
    #dt = db.Column('datetime', db.DateTime, default=datetime.now)
    dt = db.Column('datetime', db.DateTime)
    created = db.Column('created', Timestamp, server_default=text('CURRENT_TIMESTAMP'))
    updated = db.Column('updated', Timestamp, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    comment = db.Column('comment', db.Text)
class Comment_info(Class_info):    
    #[[("print_name", colspan),,],,]
    header = [
        [("shot_date", 2), ("comment", 1)],
        ]
    
    # [(html_name, printing_name, db, editable, edit_type, width, height),,]
    # html_name should be same to the variable name of column such as dt.
    colinf = [
            ("shot", "放電", Comment.shot, False, ),
            ("dt", "日時", Comment.dt, False),
            ("comment", "コメント", Comment.comment, True, "textarea", 60, 5),
            ] 

    def __init__(self):
        super().__init__(Comment)

class Rfpc(db.Model):
    __tablename__='rfpc'
    shot = db.Column('shot', db.Integer, primary_key=True, autoincrement=False)
    #dt = db.Column('datetime', db.DateTime, default=datetime.now)
    dt = db.Column('datetime', db.DateTime)
    created = db.Column('created', Timestamp, server_default=text('CURRENT_TIMESTAMP'))
    updated = db.Column('updated', Timestamp, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    system = db.Column('system', db.Text)
    order = db.Column('order', db.Text)
    sttime = db.Column('start_time', db.Text)
    entime = db.Column('end_time', db.Text)
class Rfpc_info(Class_info):    
    #[[("print_name", colspan),,],,]
    header = [
        [("shot", 1), ("RF_PC", 4)],
        ]
    
    # [(html_name, printing_name, db, editable, edit_type, width, height),,]
    # html_name should be same to the variable name of column such as dt.
    colinf = [
            ("shot", "放電", Rfpc.shot, False, ),
            ("system", "使用系統", Rfpc.system, True, "text", 16),
            ("order", "指令値", Rfpc.order, True, "text", 8),
            ("sttime", "開始時刻", Rfpc.sttime, True, "text", 8),
            ("entime", "終了時刻", Rfpc.entime, True, "text", 8),
            ] 

    def __init__(self):
        super().__init__(Rfpc)


tables = [
    ("sc", "shot comment", Comment_info()),
    ("rfpc", "RF_PC", Rfpc_info()),
          ]
table_selection = [(e[0], e[1]) for e in tables]
table_class = [(e[0], e[2]) for e in tables]
    