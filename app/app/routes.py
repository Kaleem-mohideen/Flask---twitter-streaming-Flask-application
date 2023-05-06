from flask import render_template, url_for
from app import app, db
import pandas as pd
from app.models import Post
from app.utils import TwitterPosts
import datetime
from sqlalchemy import or_
from app.webforms import SearchForm

@app.before_first_request
def do_something_only_once():
    pst = TwitterPosts()
    posts = pst.getposts()
    for post in posts:
        exists = db.session.query(db.exists().where(Post.content == post[4])).scalar()
        if not exists:
            twitter_posts = Post(author=post[1], date_posted= datetime.datetime.strptime(post[3], "%Y-%m-%d %H:%M:%S.%f"), content=post[4], user_name=post[2], decription=post[5], image_file=post[6])
            db.session.add(twitter_posts)
            db.session.commit()
    

@app.route("/")
@app.route("/home")
def home():
    pst = TwitterPosts()
    posts = pst.getposts()
    for post in posts:
        exists = db.session.query(db.exists().where(Post.content == post[4])).scalar()
        if not exists:
            twitter_posts = Post(author=post[1], date_posted= datetime.datetime.strptime(post[3], "%Y-%m-%d %H:%M:%S.%f"), content=post[4], user_name=post[2], decription=post[5], image_file=post[6])
            db.session.add(twitter_posts)
            db.session.commit()
    posts = Post.query.all()
    return render_template('home.html', posts= posts)

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        searched = form.searched.data
        posts = posts.filter(or_(Post.content.like('%' + searched + '%'), Post.author.like('%' + searched + '%')))
        posts = posts.order_by(Post.date_posted).all()
        return render_template("search.html", form=form, searched= searched, posts = posts)