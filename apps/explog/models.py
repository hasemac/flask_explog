from datetime import datetime

from apps.app import db
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text


class Comment(db.Model):
    __tablename__='comment'
    shot = db.Column('shot', db.Integer, primary_key=True, autoincrement=False)
    dt = db.Column('datetime', db.DateTime, default=datetime.now)
    created = db.Column('created', Timestamp, server_default=text('CURRENT_TIMESTAMP'))
    updated = db.Column('updated', Timestamp, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    comment = db.Column('comment', db.Text)    

    header = [("name1", 2), ("name2", 1)]
    
    cols = None
    def __init__(self):
        super().__init__()
        # ((html_name, printing_name, db, editable, edit_type, width, height))
        # ((colname, str, editable))
        self.cols = [
            ("shot", "放電", Comment.shot, False, )
            (Comment.shot, "放電", False),
            (Comment.dt, "日時", False),
            (Comment.comment, "コメント", True, "textarea", 20, 5),
            ]
        
    # 1つのrecordの取得
    def get_record(self, sh):
        cl = tuple([e[0] for e in self.cols])
        q = db.session.query(*cl).filter(Comment.shot == sh).all() 
        return q
        
    # 表示するカラムの定義    
    def get_dat(self, sh):
        #cols = (Comment.shot, Comment.dt, Comment.created, Comment.updated)
        #q = db.session.query(Comment.shot, Comment.dt).filter(Comment.shot >= 2, Comment.shot <= 10)
        #q = db.session.query(Comment).filter(Comment.shot >= 2, Comment.shot <= 10)
        cl = tuple([e[0] for e in self.cols])
        q = db.session.query(*cl).filter(Comment.shot >= 2, Comment.shot <= 10).all()
        return q
        
    