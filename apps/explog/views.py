#from apps.explog.forms import Shot_table_form
import apps.explog.forms as frms
from apps.app import db
from apps.explog.models import Comment, Comment_info, table_class
from flask import Blueprint, render_template, request, session

explog = Blueprint(
    "explog",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@explog.route("/")
def index():
    db.session.query(Comment).all()
    return render_template("explog/index.html")

@explog.route("/tab", methods=['GET', 'POST'])
def tab():
    numperpage = 10
    sht = 1
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
            
        if True == form.btn_save.data:
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
    
    return render_template("explog/tab.html", coms=coms, form=form)
