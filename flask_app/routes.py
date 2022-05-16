# 3rd-party packages
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    Blueprint,
    session,
    g,
)
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from .models import User, Group
main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():

    if current_user.is_authenticated:
        return redirect(url_for('songs.groups'))  
    else:
        return redirect(url_for('users.login'))