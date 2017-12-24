from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board

main = Blueprint('board', __name__)


@main.route("/")
def index():
    u = current_user()
    print(u.role)
    return render_template('board/admin_index.html', user=u)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.role == 'admin':
        m = Board.new(form)
    return redirect(url_for('topic.index'))
