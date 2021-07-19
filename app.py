from operator import pos
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "12345679"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home():
    return redirect('/users')


@app.route('/users')
def show_users():
    users = User.query.order_by(User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def add_user():
    users = User.query.all()
    return render_template('add_user.html')


@app.route('/users/new', methods=["POST"])
def post_user():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if request.form["img_url"]:
        img_url = request.form["img_url"]
    else:
        img_url = None
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edited_user(user_id):

    user = User.query.filter(User.id == user_id).one()
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).one()
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/post/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_new.html', user=user)


@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def handle_post_form(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get(post_id)
    return render_template('post_edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    user_id = Post.query.get(post_id).user_id
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/home')
def posts_home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts_home.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404