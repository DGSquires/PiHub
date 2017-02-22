# Defines routes used for authentication module
from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from . import profile
from .. import db
from ..models import User, Node, Association, Permissions
from .forms import NodeInfoForm, UserInfoForm, UserPassword


@profile.route('/node/<int:id>', methods=['GET', 'POST'])
@login_required
def node(id):
    node_info = Node.query.filter_by(id=id).first()
    user_id_list = [i.user_id for i in Association.query.filter_by(node_id=node_info.id).all()]
    users = User.query.filter(User.id.in_(user_id_list)).all()
    session['node_name'] = node_info.name #REMEMBER TO CLEAR
    return render_template('profile/node.html',
                           node=node_info, users=users)


@profile.route('/node_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def node_edit(id):   #User role must be SUPER to add or remove others, ADMIN to edit settings
    node = db.session.query(Node).filter_by(id=id).first()
    session['node_name'] = node.name
    form = NodeInfoForm()
    if form.validate_on_submit():
        session.pop('node_name', None)
        node.name = form.name.data
        node.ip_address = form.ip_address.data
        node.dat_start = form.dat_start.data
        node.dat_end = form.dat_end.data
        db.session.commit()
        flash('Access point has been updated')
        return redirect(url_for('.node', id=node.id))
    form.name.data = node.name
    form.ip_address.data = node.ip_address
    form.dat_start = node.dat_start
    form.dat_end = node.dat_end
    session['node_name'] = node.name
    return render_template('profile/node_edit.html',
                           node=node, form=form)

@profile.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    node_id_list = [i.node_id for i in Association.query.filter_by(user_id=user.id).all()]
    nodes = Node.query.filter(Node.id.in_(node_id_list)).all()
    return render_template('profile/user.html', user=user, nodes=nodes)

@profile.route('/user_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = User.query.filter_by(id=id).first()
    form = UserInfoForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('.user', id=user.id))
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    return render_template('profile/user_edit.html', user=user, form=form)

@profile.route('/user_password/<int:id>', methods=['GET', 'POST'])
@login_required
def user_password(id):
    user = User.query.filter_by(id=id).first()
    form = UserPassword()
    if form.validate_on_submit():
        if user.verify_password(form.current_password.data):
            user.password = form.password.data
            db.session.commit()
            flash('Password updated')
            return redirect(url_for('.user', id=session['user_id']))
        flash('Current and form passwords do not match')
    return render_template('profile/user_password.html', form=form)




