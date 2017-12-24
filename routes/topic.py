from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic
from models.board import Board


main = Blueprint('topic', __name__)


import uuid
csrf_tokens = dict()
@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        #ms = Topic.cache_all()
        ms = Topic.all_delay()
    else:
        #ms = Topic.cache_find(board_id)
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens[token] = u.id
    print('csrf_tokens', csrf_tokens)
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    # for i in range(1000):
    #     m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    topic_id = int(request.args.get('id'))
    print(id)
    token = request.args.get('token')
    print(token)
    print(csrf_tokens)
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u, topic_id)
            Topic.delete(topic_id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)
