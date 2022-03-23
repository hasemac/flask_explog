from apps.app import db


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

    # データベースのカラムを取得
    def get_db_columns(self):
        a = []
        for e in self.tbinf:
            a.append(e.dbc)
        a = tuple(a)
        return a    

    # 特定のhtmlnameに値を設定
    def set_one_val(self, htmlname, val):
        for e in self.tbinf:
            if htmlname == e.html:
                e.val = val

            
    def clear_val(self):
        # 文字列で初期化-htmlで表示するのが殆ど
        for e in self.tbinf:
            # e.val = None
            e.val = ""                    
    
    # 表示するターブルのヘッダーを生成  
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

    # テーブルの入力業に関する情報を取得
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

    # データベースへの登録用クラスの作成
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
