from tkinter import Widget

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class Total_form(FlaskForm):
    shot = IntegerField(
        "Shot:",
        validators=[
            DataRequired(message='Shot number is required.'),
            NumberRange(1, 999999, 'incorrect number'),
        ],
    )
    table = SelectField('Table:', choices=[("sc", "shot comment"), ("rf", "RF-PC")])

    btn_move        = SubmitField("move")
    btn_prev_page   = SubmitField("prev_page")
    btn_prev        = SubmitField("previous")
    btn_next        = SubmitField("next")
    btn_next_page   = SubmitField("next_page")
    btn_last        = SubmitField("last")
    
    btn_save = SubmitField("save")
    
    # fields
    # (value, editable, type, width, height)
    fields = [
        ("value1", False, "text", ), 
        ("v2", False, "text", ), 
        ("v3", True, "textarea", 20, 2)
        ]    

    # header
    # [[("title", colspan),,,,],,,,,]
    header = None
    
    def set_model(self, model, shot):
        # tableのヘッダーの作成
        self.header = [model.header]
        res = []
        for e in model.cols:
            res.append((e[1], 1))
        self.header.append(res)

        # 入力用fieldsの作成
        vals = model.get_record(shot)
        if 0 == len(vals):
            vals = tuple([shot])+tuple(["" for e in range(len(model.cols)-1)])
        else:
            vals = vals[0]
        
        self.fields = []
        for v, e in zip(vals, model.cols):
            f = tuple([v])+e[2:]
            self.fields.append(f)
