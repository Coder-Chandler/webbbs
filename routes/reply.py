from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u is not None:
        log('DEBUG回复 ->', form)
        m = Reply.new(form)
        m.set_user_id(u.id)
        return redirect(url_for('topic.detail', id=m.topic_id))
    return render_template('404.html')



