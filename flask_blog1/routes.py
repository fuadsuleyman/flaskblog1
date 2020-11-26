import os
import secrets
from flask import render_template, url_for, redirect, request
from flask_blog1 import app, db
from flask_blog1.forms import PostForm, CommentForm
from flask_blog1.models import Post, Comment


# posts = [
#     {
#         'title': 'Post 1',
#         'description': 'Post1 description'
#     },
#     {
#         'title': 'Post 2',
#         'description': 'Post2 description'
#     },
# ]

# her iki route eyni yeri acir
@app.route("/")
@app.route("/home")
def home_page():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('add_post.html', form=form)

@app.route("/comment/new", methods=['GET', 'POST'])
def new_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post_id=form.id.data)
        db.session.add(comment)
        db.session.commit()
        # return redirect(url_for("{{ post(form.id.data) }}"))
        return redirect(url_for("home_page"))
    return render_template('add_comment.html', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    return render_template('post.html', post=post, comments=comments)


