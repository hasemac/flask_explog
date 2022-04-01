#from apps.explog.forms import Shot_table_form
import signal
import sys
import threading
import time

import apps.explog.db_base as dbb
import apps.explog.forms as frms
import requests
from apps.app import db
from apps.explog.models import Comment, Comment_info, table_class
from flask import Blueprint, render_template, request, session

explog = Blueprint(
    "explog",
    __name__,
    template_folder="templates",
    static_folder="static",
)

def get_current_shot_number():
    shot = 1
    # ubuntu_mariadbのゲートウェイはDMZ側に設定している
    # csv02は192.168.52.2で返されるのでDMZに行ってします。
    # しかたないのでIP直打ちにする。
    #uinf = requests.get('http://csv02.exp.triam.kyushu-u.ac.jp/expinfo/shotNumber.txt')        
    uinf = requests.get('http://192.168.0.253/expinfo/shotNumber.txt')
    shot = int(uinf.text)
    return shot

class Thread_shot(threading.Thread):
    flg = True
    shot = 1
    

    #def __init__(self):
    #    super().__init__()
        
    def restart(self):
        self.flg = True
        self.start()
        
    def run(self):
        while self.flg:
            time.sleep(5)
            s = get_current_shot_number()
            if self.shot != s:
                self.shot = s
                for e in table_class:
                    ndb = dbb.db_table(e[1].Model_class.__tablename__)
                    ndb.set_new_shot_data(s)
                    #e[1].regist_class_for_new_shot(self.shot)


th_shot = Thread_shot()
th_shot.restart()

def check_ip(ip: str):
    res = False
    dom = ['127.0.0.1', 
           '192.168.0.',
           '192.168.52.', 
           '192.168.71.'
           ]
    for e in dom:
        if ip.startswith(e):
            res = True
    return res
              
@explog.route("/")
def index():
    db.session.query(Comment).all()
    return render_template("explog/index.html")

@explog.route("/table/", methods=['GET', 'POST'])
def tab():
    numperpage = 10
    sht = get_current_shot_number()
    tbn = Comment_info()

    form = frms.Total_form()

    # GET 
    if "shot" in session:
        sht = session["shot"]
    
    # POST
    if form.validate_on_submit():
        sht = form.shot.data
        stname = form.table.data
        for e in table_class:
            if stname == e[0]:
                tbn = e[1]
        
        if True == form.btn_next.data:
            sht += 1
        if True == form.btn_prev.data:
            sht -= 1
        if True == form.btn_next_page.data:
            sht += numperpage
        if True == form.btn_prev_page.data:
            sht -= numperpage
        if True == form.btn_last.data:
            sht = th_shot.get_current_shot_number()
            
        if True == form.btn_save.data:
            
            ip = request.remote_addr
            if check_ip(ip):
                
                # shtが既にあれば、shtのデータを削除
                if 0 != len(tbn.get_record(sht)):
                    db.session.query(tbn.Model_class).filter_by(shot=sht).delete()
                    db.session.commit()
                    
                # 新しいクラスを作成して登録
                c = tbn.get_new_class(request.form)
                db.session.add(c)
                db.session.commit()
                sht += 1
        
        # shotの値の範囲の確認    
        if 0 >= sht:
            sht = 1
        if 999999 < sht:
            sht = 999999
    form.shot.default = sht
    
    # header
    #print("request headers: ", request.headers)
    #print("header: ", request.headers.get("some_key"))
    #print("header: ", request.headers["some_key"]) # error when no key
    
    # form
    #print("form", request.form.to_dict())
    
    form.header = tbn.get_html_header()
    form.fields = tbn.get_html_fields(sht)
        
    #form.set_model(c, sht)
    coms = tbn.get_data(sht-numperpage, sht-1)
    # リストを反転してショット番号が大きい順
    coms.reverse() 
    
    session["shot"] = sht
    
    return render_template("explog/table.html", coms=coms, form=form)
