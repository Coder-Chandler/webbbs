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
from models.reply import Reply


main = Blueprint('topic', __name__)


import uuid
csrf_tokens = dict()
@main.route("/")
def index():
    # board_id = 2
    log('request ->', request)
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        #ms = Topic.cache_all()
        ms = Topic.all_delay()
    else:
        #ms = Topic.cache_find(board_id)
        ms = Topic.find_all(board_id=board_id)
    u = current_user()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, bs=bs, user=u)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    token = str(uuid.uuid4())
    u = current_user()
    if u is not None:
        csrf_tokens[token] = u.id
        log('csrf_tokens', csrf_tokens)
    else:
        csrf_tokens[token] = None
        log('csrf_tokens', csrf_tokens)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, token=token, user=u)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    log('add form ->', form)
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    m = Topic.new(form, user_id=u.id)
    # for i in range(1000):
    #     m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    log('token ->', token)
    log('csrf_tokens ->', csrf_tokens)
    u = current_user()
    topic = Topic.get(id)
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == topic.user_id:
        csrf_tokens.pop(token)
        if u is not None:
            log('删除 topic 用户是', u, id)
            log('要删除的topic', Topic.get(id))
            topic = Topic.get(id)
            Topic.delete(topic)
            return redirect(url_for('.index'))
        else:
            return render_template('404.html')
    else:
        return render_template('403.html')


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)
