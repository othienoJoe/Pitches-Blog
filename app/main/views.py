from flask import render_template, url_for, abort, flash, request
from werkzeug.utils import redirect
from . import main
from flask_login import login_required, current_user
from ..models import User, Role, Post, Comment, Dislike, Like, Category
from slugify import slugify
from .. import db, photos
from .forms import UpdateProfileForm, CommentForm, CategoryForm

def getAuthor(id):
    user = User.query.filter_by(id = id).first()
    return user

# Adding category to the datebase
@main.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('.index'))
    return render_template('add_category.html', form=form)

@main.route('/')
def index():
    """
        View root page function that returns the index page and its data
    """
    pitches = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('index.html', pitches=pitches)

# Creating the profile page
@main.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = UpdateProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', username=user.username))
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.about_me.data = user.about_me

    # Get all the posts of the current user with its category
    pitches = Post.get_posts_by_author(
        user.id).order_by(Post.timestamp.desc()).all()

    # Get all categories
    categories = Category.get_all_categories()

    return render_template('profile/profile.html', user=user, form=form, pitches=pitches, categories=categories)

# Updating the profile picture
@main.route('/update_profile_pic', methods=['POST'])
@login_required
def update_profile_pic():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        current_user.profile_image = path
        db.session.commit()
    return redirect(url_for('.profile', username=current_user.username))

# Creating a new pitch
@main.route('/new_pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():

    title = request.args.get('title')
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    body = request.args.get('body')

    # make a new slug from the title
    slug = slugify(title)
    # check if the slug already exists
    pitch = Post.query.filter_by(slug=slug).first()
    if pitch is not None:
        # if it exists, append a number to the slug
        slug = slugify(title) + '-' + str(pitch.id)

    new_pitch = Post(
        title=title,
        body=body,
        user_id=user_id,
        category_id=category_id,
        slug=slug,
    )
    db.session.add(new_pitch)
    db.session.commit()
    flash('New pitch created successfully!', 'success')
    return redirect(url_for('.profile', username=current_user.username))

# Getting pitch details by their id
@main.route('/pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def pitch(id):
    # get all comments of the pitch
    comments = Comment.query.filter_by(post_id=id).all()
    pitch = Post.query.get(id)
    if pitch is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            post_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.body.data = ''
        flash('Your comment has been posted successfully!', 'success')
        return redirect(url_for('.pitch', pitch=pitch, form=form, comments=comments,id=id))

    return render_template('single_pitch.html',
                           pitch=pitch,
                           form=form,
                           comments=comments
                           )

# Adding a like to a pitch
@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    pitch = Post.query.get(id)
    if pitch is None:
        abort(404)
    # check if the user has already liked the pitch
    like = Like.query.filter_by(user_id=current_user.id, post_id=id).first()
    if like is not None:
        # if the user has already liked the pitch, delete the like
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unlike the pitch!', 'success')
        return redirect(url_for('.index'))
    # if the user has not liked the pitch, add a like
    new_like = Like(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully liked the pitch!', 'success')
    return redirect(url_for('.index'))

# Adding a dislike to a pitch
@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    pitch = Post.query.get(id)
    if pitch is None:
        abort(404)
    # check if the user has already disliked the pitch
    dislike = Dislike.query.filter_by(
        user_id=current_user.id, post_id=id).first()
    if dislike is not None:
        # if the user has already disliked the pitch, delete the dislike
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully undisliked the pitch!', 'success')
        return redirect(url_for('.index'))
    # if the user has not disliked the pitch, add a dislike
    new_dislike = Dislike(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully disliked the pitch!', 'success')
    return redirect(url_for('.index'))

# Deleting a pitch 
@main.route('./delete_pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_pitch(id):
    pitch = Post.query.get(id)
    if pitch is None:
        abort(404)
    # check if the pitch has comments, like and dislike, if yes, delete all comments, likes and dislikes
    if pitch.comment:
        for comment in pitch.comment:
            db.session.delete(comment)
            db.session.commit()

    if pitch.like:
        for like in pitch.like:
            db.session.delete(like)
            db.session.commit()

    if pitch.dislike:
        for dislike in pitch.dislike:
            db.session.delete(dislike)
            db.session.commit()

    db.session.delete(pitch)
    db.session.commit()
    flash('You have successfully deleted the pitch!', 'danger')
    return redirect(url_for('.profile', username=current_user.username))


# Filter pitches by category
@main.route('/category/<int:category_id>', methods=['GET', 'POST'])
def filter_pitches_by_category(category_id):
    pitches = Post.query.filter_by(category_id=category_id).all()
    category = Category.query.get(category_id)
    return render_template('filter_pitches_by_category.html', pitches=pitches, category=category)