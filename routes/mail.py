from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.mail import Mail


main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    if current_user() is not None:
        form = request.form
        mail = Mail.new(form)
        mail.set_sender(current_user().id)
        return redirect(url_for(".index"))
    else:
        return redirect(url_for('topic.index'))


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    if u is not None:
        send_mail = Mail.find_all(sender_id=u.id)
        received_mail = Mail.find_all(receiver_id=u.id)

        return render_template("mail/index.html", sends=send_mail, receives=received_mail, user=u)
    else:
        return redirect(url_for('topic.index'))


@main.route("/view/<int:id>")
def view(id):
    if current_user() is not None:
        mail = Mail.find(id)
        if current_user().id == mail.receiver_id:
            mail.mark_read()
        if current_user().id in [mail.receiver_id, mail.sender_id]:
            return render_template("mail/detail.html", mail=mail, user=current_user())
        else:
            return redirect(url_for(".index"))
    else:
        return redirect(url_for('topic.index'))

