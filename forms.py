#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired("请输入标题")],
                        description="请输入标题", render_kw={'required': 'required', "class": "form-control"})
    news_type = SelectField('类型', validators=[DataRequired("请选择")], render_kw={'class': "form-control"},
                            choices=[('推荐', '推荐'), ('百家', '百家'), ('娱乐', '娱乐'), ('体育', '体育')])
    content = TextAreaField('内容', validators=[DataRequired("请输入内容")], description="请输入标题",
                            render_kw={'required': 'required', "class": "form-control"})
    submit = SubmitField('提交', render_kw={"class": "btn btn-default"})