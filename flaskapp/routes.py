import os
import secrets
from PIL import Image
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flaskapp import app, db, bcrypt
from flaskapp.models import User, Post, Draft, PostLikes
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DraftForm, MasterForm
from flask_login import login_user, current_user, logout_user, login_required
import requests

# posts = [
#     {
#     'author': 'Tom F',
#     'title': 'Post number eins',
#     'content': 'Some content 1',
#     'date_posted': 'December 7, 2019'
#     },
#     {
#     'author': 'Mr. Minecraft',
#     'title': 'Post number zwei',
#     'content': 'Some content 2',
#     'date_posted': 'December 8, 2019'
#     }


# ]

@app.route('/')
@app.route("/home")
def home():
    #name = request.args.get("name", "World")
    if current_user.is_anonymous != True:
        user_liked =  PostLikes.query.filter_by(user_id=current_user.id).all()
        pass_like = []
        for likes in user_liked:
            pass_like.append(likes.post_id)
        print(pass_like)

        posts = Post.query.all()
        return render_template('home.html', posts= posts, pass_like = pass_like)
    else:
        posts = Post.query.all()
        return render_template('home.html', posts= posts)

@app.route("/drafts")
@login_required
def drafts():
    #name = request.args.get("name", "World")
    if current_user.is_anonymous == True:
        flash('You must log in to do this!', 'danger')
        return redirect(url_for('home'))

    drafts = Draft.query.filter_by(user_id=current_user.id)
    print(drafts)
    return render_template('drafts.html', drafts= drafts)

@app.route("/drafts", methods=['GET','POST'])
@login_required
def save_draft():
    form = DraftForm()
    #if form.validate_on_submit():
    draft = Draft(title = form.title.data, content = form.content.data, author = current_user)
    db.session.add(draft)
    db.session.commit()
    flash('Your draft has been saved!', 'success')
    return redirect(url_for('drafts'))

    #return render_template('create_post.html', title='New Post', form = form)

@app.route('/about')
def about():
    #name = request.args.get("name", "World")
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    #name = request.args.get("name", "World")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash('Login Success!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
             flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form =  UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has now been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form = form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = MasterForm() #default

    if form.validate_on_submit():
        if form.post.data:
            #form = form.post
            response = requests.get('http://api.ipstack.com/check?access_key=8d65c9b303bb3dcae75300fc9f9f599b&output=json')
            thisJson = response.json()
            city = thisJson['city']
            state = thisJson['region_name']
            print(city)

            post = Post(title = form.title.data, content = form.content.data, author = current_user, city=city, state=state)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))

        if form.draft.data:
            #form = form.draft
            draft = Draft(title = form.title.data, content = form.content.data, author = current_user)
            db.session.add(draft)
            db.session.commit()
            flash('Your draft has been saved!', 'success')
            return redirect(url_for('drafts'))

    return render_template('create_post.html', title='New Post', form = form)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    if current_user.is_anonymous != True:
        post = Post.query.get_or_404(post_id)

        user_liked =  PostLikes.query.filter_by(user_id=current_user.id).all()
        pass_like = []
        for likes in user_liked:
            pass_like.append(likes.post_id)
        print(pass_like)

        return render_template('post.html', title=post.title, post = post, pass_like = pass_like )
    else:
        post = Post.query.get_or_404(post_id)
        return render_template('post.html', title=post.title, post = post)

@app.route("/drafts/<int:draft_id>", methods=['GET', 'POST'])
@login_required
def draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    return render_template('draft.html', title=draft.title, draft = draft )

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method =='GET':
      form.title.data = post.title
      form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form = form, legend='Update Post')

@app.route("/draft/<int:draft_id>/update_draft", methods=['GET', 'POST'])
@login_required
def update_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.author != current_user:
        abort(403)
    form = MasterForm()
    if form.validate_on_submit():
        if form.draft.data:
            draft.title = form.title.data
            draft.content = form.content.data
            db.session.commit()
            flash('Your draft has been updated!', 'success')
            return redirect(url_for('draft', draft_id=draft.id))
        elif form.post.data:
            db.session.delete(draft)

            response = requests.get('http://api.ipstack.com/check?access_key=8d65c9b303bb3dcae75300fc9f9f599b&output=json')
            thisJson = response.json()
            city = thisJson['city']
            state = thisJson['region_name']
            post = Post(title = form.title.data, content = form.content.data, author = current_user, city=city, state=state)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))

    elif request.method =='GET':
      form.title.data = draft.title
      form.content.data = draft.content
    return render_template('update_draft.html', title='Update Draft', form = form, legend='Update Draft')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'danger')
    return redirect(url_for('home'))

@app.route("/draft/<int:draft_id>/delete_draft", methods=['POST'])
@login_required
def delete_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.author != current_user:
        abort(403)
    db.session.delete(draft)
    db.session.commit()
    flash('Your draft has been deleted!', 'danger')
    return redirect(url_for('drafts'))

@app.route("/draft/<int:draft_id>/post_draft", methods=['POST','GET'])
@login_required
def post_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.author != current_user:
        abort(403)


    response = requests.get('http://api.ipstack.com/check?access_key=8d65c9b303bb3dcae75300fc9f9f599b&output=json')
    thisJson = response.json()
    city = thisJson['city']
    state = thisJson['region_name']
    post = Post(title = draft.title, content = draft.content, author = current_user, city=city, state=state)
    db.session.delete(draft)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created!', 'success')
    return redirect(url_for('home'))

@app.route("/like_post_home/<int:post_id>", methods=['POST','GET'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(current_user.id)
    liked = PostLikes.query.filter_by(user_id=current_user.id,post_id=post_id).first()


    if(not liked):
        new_like=PostLikes(user_id=current_user.id,post_id=post_id)
        db.session.add(new_like)
        post.num_likes = post.num_likes + 1
        db.session.commit()
    else:
        db.session.delete(liked)
        post.num_likes = post.num_likes - 1
        db.session.commit()



    return redirect(url_for('home'))

@app.route("/like_post_view/<int:post_id>", methods=['POST','GET'])
@login_required
def like_post_view(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(current_user.id)
    liked = PostLikes.query.filter_by(user_id=current_user.id,post_id=post_id).first()


    if(not liked):
        new_like=PostLikes(user_id=current_user.id,post_id=post_id)
        db.session.add(new_like)
        post.num_likes = post.num_likes + 1
        db.session.commit()
    else:
        db.session.delete(liked)
        post.num_likes = post.num_likes - 1
        db.session.commit()



    return redirect(url_for('post',post_id=post_id))
