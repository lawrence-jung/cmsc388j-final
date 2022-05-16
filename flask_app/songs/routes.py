from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import CreateGroupForm, RegistrationForm, LoginForm, UpdateUsernameForm, CommentForm, SearchForm
from ..models import User, Group, id_counter, Comment
from ..utils import current_day, current_time
from ..client import get_songs
from datetime import datetime


songs = Blueprint("songs", __name__)

def refresh(group):
    now = current_time()
    diff = (datetime.strptime(now, "%B %d, %Y at %H:%M:%S") - datetime.strptime(group.today, "%B %d, %Y at %H:%M:%S")).days
    new_expiry = group.expiry - diff
    group.modify(expiry=new_expiry, today=now)

    if new_expiry <= 0:
        group.modify(over=True)

@songs.route('/groups', methods = ['GET', 'POST'])
@login_required
def groups():
    cg_form = CreateGroupForm()

    for g in current_user.groups:
        refresh(g)
 
    if cg_form.validate_on_submit():

        cid = -1
        try:
            cid = id_counter.objects.get().value
        except:
            pass

        if cid == -1:
            flash("Something terrible has happened and it's not your fault")

        new_g = Group(g_id = cid, name = cg_form.name.data, members = [current_user.username], expiry = cg_form.expiry.data, open_invite=cg_form.anyone_can_invite, today=current_time(), over=False, subs = [""])
        new_g.save()

        curr_gs = current_user.groups
        if curr_gs == None:
            current_user.modify(groups = [new_g])
        else:
            current_user.modify(groups=current_user.groups + [new_g])
        
        temp = cid + 1
        id_counter.objects.modify(value=temp)
        return redirect(url_for('songs.g', gid=new_g.g_id))  
     
    return render_template('groups.html', groups = current_user.groups, cg_form=cg_form)

@songs.route('/g/<gid>', methods = ['GET', 'POST'])
@login_required
def g(gid): 
    group = Group.objects(g_id=gid).first()
    refresh(group)

    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        nc = Comment(commenter=current_user.username, content=comment_form.text.data, date=current_time())
        nc.save()
        temp = group.comments + [nc]
        group.modify(comments=temp)
        return redirect(url_for('songs.g', gid=gid))

    return render_template('g.html', group=group, subs = group.subs, cf=comment_form)

@songs.route('/s/<gid>', methods = ['GET', 'POST'])
@login_required
def s(gid):
    search_form = SearchForm()

    if search_form.validate_on_submit():
        q = search_form.search_query.data
        return redirect(url_for('songs.r', q=q, gid=gid))

    return render_template('search.html',form=search_form,gid=gid)

@songs.route('/r/<gid>/<q>', methods = ['GET', 'POST'])
@login_required
def r(q, gid):
    try:
        results = get_songs(q)
        return render_template('r.html', results=results, gid=gid)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('songs.g', gid=gid))

@songs.route('/submit/<gid>/<s>', methods = ['GET', 'POST'])
@login_required
def submit(gid, s):
    group = Group.objects(g_id=gid).first()
    temp = group.subs + [s]
    group.modify(subs=temp)
    return redirect(url_for('songs.g', gid=gid))
