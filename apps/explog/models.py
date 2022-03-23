from datetime import datetime

from apps.app import db
from apps.explog.models_sub import Class_info
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text


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
    sys = db.Column('sys', db.Text)
    order_value = db.Column('order_value', db.Text)
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
            ("system", "使用系統", Rfpc.sys, True, "text", 16),
            ("order", "指令値", Rfpc.order_value, True, "text", 8),
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

