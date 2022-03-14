#from apps.explog.forms import Shot_table_form
import apps.explog.forms as frms
from apps.app import db
from apps.explog.models import Comment
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

    sht = 10
    tbn = ""

    form = frms.Total_form()

    # GET 
    if "shot" in session:
        sht = session["shot"]
    
    # POST
    if form.validate_on_submit():
        sht = form.shot.data
        tbn = form.table.data
        
        if True == form.btn_next.data:
            sht += 1   
    
            
    
    form.shot.default = sht

    ########################################
    #for e in form:
    #    print(e)

    c = Comment()    
    form.set_model(c, sht)

    print("aaaaaaaaaaaaaaaaaa", sht, tbn, form.btn_move.data, form.btn_next.data, request.form.getlist("name1") )
    #coms = Comment.query.all()


    coms = c.get_dat(sht)

    session["shot"] = sht
    
    return render_template("explog/tab.html", coms=coms, form=form)
