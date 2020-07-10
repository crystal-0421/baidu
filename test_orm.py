#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime

from flask import Flask, redirect, render_template, url_for, flash, abort, request
from flask_sqlalchemy import SQLAlchemy

from forms import NewForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@127.0.0.1/baidu_news"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "asd123sad"
db = SQLAlchemy(app)


class News(db.Model):
    # 新闻模型
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    news_type = db.Column(db.Enum("推荐", "百家", "娱乐", "体育"))
    content = db.Column(db.String(2000), nullable=False)
    is_valid = db.Column(db.Boolean, default=1)
    create_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    update_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False)

    comments = db.relationship('Comments', backref='news', lazy='dynamic')

    def __repr__(self):
        return "<News %r>" % self.title


class Comments(db.Model):
    # 新闻评论模型
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    is_valid = db.Column(db.Boolean, default=1)
    create_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    update_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False)

    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return "<Comments %r>" % self.content


''' 后台管理页面 '''
@app.route('/admin/')
@app.route('/admin/<int:page>')
def admin(page=None):
    # 新闻后台管理
    PER_PAGE = 2
    if page is None:
        page = 1
    page_data = News.query.filter_by(is_valid=True).paginate(page, PER_PAGE)
    return render_template('admin/admin.html', page_data=page_data)


@app.route('/admin/add/', methods=["GET", "POST"])
def add():
    # 新增新闻
    form = NewForm()
    if form.validate_on_submit():
        new1 = News(
            title=form.title.data,
            news_type=form.news_type.data,
            content=form.content.data
        )
        db.session.add(new1)
        db.session.commit()
        flash('新增成功')
        return redirect(url_for('admin'))
    return render_template('admin/add.html', form=form)


@app.route('/admin/update/<int:pk>', methods=["GET", "POST"])
def update(pk):
    # 修改新闻
    new_obj = News.query.get(pk)
    if new_obj is None:
        abort(404)
    form = NewForm(obj=new_obj)
    if form.validate_on_submit():
        new_obj.title = form.title.data
        new_obj.news_type = form.news_type.data
        new_obj.content = form.content.data
        new_obj.update_at = datetime.now()
        db.session.add(new_obj)
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('admin'))
    return render_template('admin/add.html', form=form)


@app.route('/admin/delete/<int:pk>', methods=["POST"])
def delete(pk):
    # 修改新闻
    if request.method == 'POST':
        new_obj = News.query.get(pk)
        if new_obj is None:
            return 'no'
        new_obj.is_valid = False
        db.session.add(new_obj)
        db.session.commit()
        return 'yes'
    return 'no'


if __name__ == "__main__":
    app.run(debug=True)
