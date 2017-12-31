from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from config import user_file_director
import os

from utils import log

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    log('index 的 request ->', request)
    u = current_user()
    return redirect(url_for('topic.index'))


@main.route("/signin")
def signin():
    log('index 的 request ->', request)
    u = current_user()
    return render_template("login.html", user=u)


@main.route("/signup")
def signup():
    log('index 的 request ->', request)
    u = current_user()
    return render_template("register.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    log('注册的用户form ->', form)
    # print('用户注册的form', form)
    # 用类函数来判断
    u = User.register(form)
    # print('注册的用户', u)
    return redirect(url_for('.signin'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    print(form)
    log('用户登录的form ->', form)
    u = User.validate_login(form)
    print(u)
    log('登录用户验证 ->', form)
    if u is None:
        # 转到 topic.index 页面
        return render_template('404.html')
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route("/logout")
def logout():
    session['user_id'] = -1
    return redirect(url_for('.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".profile"))


@main.route("/uploads/<filename>")
def uploads(filename):
    if filename is None:
        return redirect(url_for(".profile"))
    return send_from_directory(user_file_director, filename)
