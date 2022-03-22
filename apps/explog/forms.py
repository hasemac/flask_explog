from tkinter import Widget

from apps.explog.models import table_selection
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
    #table = SelectField('Table:', choices=[
    #    ("sc", "shot comment"), 
    #    ("rfpc", "RF-PC"),
    #    ])
    table = SelectField('Table:', choices=table_selection)
    
    btn_move        = SubmitField("move")
    btn_prev_page   = SubmitField("prev_page")
    btn_prev        = SubmitField("previous")
    btn_next        = SubmitField("next")
    btn_next_page   = SubmitField("next_page")
    btn_last        = SubmitField("last")
    
    btn_save = SubmitField("save")
    
    # fields
    # [(html_name, value, editable, type, width, height),,]
    fields = [] 

    # header
    # [[("title", colspan),,,,],,,,,]
    header = None

