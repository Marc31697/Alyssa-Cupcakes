from flask import Blueprint, render_template, abort, flash
from flask.helpers import url_for
from flask_login.utils import login_required, current_user
from werkzeug.utils import redirect
from ..models import Item, db, Reviews, Announcement
from ..forms import ItemForm, ReviewForm, PostForm

admin = Blueprint('admin', __name__, template_folder='admin_templates')

# Function to redirect if user attempting to reach this portion of the site is not an admin
def check_admin():
    if not current_user.admin:
        abort(403)

# Admin Dashboard
@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    check_admin()
    return render_template('dashboard.html', title='Dashboard')

# Start of CRUD for Items DB
@admin.route('/items')
@login_required
def list_items():
    check_admin()

    items = Item.query.all()


    return render_template('items/items.html', items=items, title='Item')

@admin.route('/admin/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    check_admin()

    add_item = True
    
    form = ItemForm()

    if form.validate_on_submit():
        item = Item(form.type.data, form.description.data, form.price.data)

        try:
            db.session.add(item)
            db.session.commit()
            flash('You have successfully added a new item')
        except:
            flash('Error: Item already exists')

        return redirect(url_for('admin.list_items'))
    
    return render_template('items/item.html', action = "Add", add_item=add_item, form=form, title = "Add Item")

@admin.route('/admin/items/edit/<int:id>', methods =['GET', 'POST'])
@login_required
def edit_item(id):
    check_admin()

    add_item = False

    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.type = form.type.data
        item.description = form.description.data
        item.price = form.price.data
        db.session.commit()
        flash('You have successfully edited the item')

        return redirect(url_for('admin.list_items'))

    form.type.data = item.type
    form.description.data = item.description
    form.price.data = item.price
    return render_template('items/item.html', action= 'Edit', add_item = add_item, form=form, item = item, title='Edit Item')

@admin.route('/admin/items/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    check_admin()

    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('You have successfully deleted the item')

    return redirect(url_for('admin.list_items'))

    return render_template(title='Delete Item')

# End of CRUD for Items DB

# Start of CRUD for Reviews DB
@admin.route('/admin/reviews')
@login_required
def list_reviews():
    check_admin()

    reviews = Reviews.query.all()


    return render_template('reviews/reviews.html', reviews=reviews, title='Review')

@admin.route('/admin/reviews/add', methods=['GET', 'POST'])
@login_required
def add_review():
    check_admin()

    add_review = True
    
    form = ReviewForm()

    if form.validate_on_submit():

        review = Reviews(form.link.data.split('"')[1], form.link.data.split('"')[5])
        print(review)
        db.session.add(review)
        db.session.commit()
        flash('You have successfully added a new review')

        return redirect(url_for('admin.list_reviews'))
    
    return render_template('reviews/review.html', action = "Add", add_review=add_review, form=form, title = "Add Review")

@admin.route('/admin/reviews/edit/<int:id>', methods =['GET', 'POST'])
@login_required
def edit_review(id):
    check_admin()

    add_review = False

    review = Reviews.query.get_or_404(id)
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.link = form.link.data
        db.session.commit()
        flash('You have successfully edited the review')

        return redirect(url_for('admin.list_reviews'))

    form.link.data = review.link
    return render_template('reviews/review.html', action= 'Edit', add_review = add_review, form=form, review = review, title='Edit Review')

@admin.route('/admin/reviews/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_review(id):
    check_admin()

    review = Reviews.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    flash('You have successfully deleted the review')

    return redirect(url_for('admin.list_reviews'))
# End of CRUD for Reviews DB

# Start of CRUD for Announcements
@admin.route('/admin/announcements')
@login_required
def list_announcements():
    check_admin()

    announcements = Announcement.query.all()


    return render_template('announcements/announcements.html', announcements=announcements, title='Announcement')

@admin.route('/admin/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    check_admin()

    add_announcement = True
    
    form = PostForm()

    if form.validate_on_submit():
        announcement = Announcement(form.post.data)
        db.session.add(announcement)
        db.session.commit()
        flash('You have successfully added a new announcement')

        return redirect(url_for('admin.list_announcements'))
    
    return render_template('announcements/announcement.html', action = "Add", add_announcement=add_announcement, form=form, title = "Add Announcement")

@admin.route('/admin/announcements/edit/<int:id>', methods =['GET', 'POST'])
@login_required
def edit_announcement(id):
    check_admin()

    add_announcement = False

    announcement = Announcement.query.get_or_404(id)
    form = PostForm(obj=announcement)
    if form.validate_on_submit():
        announcement.post = form.post.data
        db.session.commit()
        flash('You have successfully edited the announcement')

        return redirect(url_for('admin.list_announcements'))

    form.post.data = announcement.post
    return render_template('announcements/announcement.html', action= 'Edit', add_announcement = add_announcement, form=form, announcement = announcement, title='Edit Review')

@admin.route('/admin/announcements/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_announcement(id):
    check_admin()

    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash('You have successfully deleted the announcement')

    return redirect(url_for('admin.list_announcements'))
# End of CRUD