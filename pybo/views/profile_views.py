from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User, Question, Answer, Comment
from sqlalchemy import text

import functools

bp = Blueprint('profile', __name__, url_prefix='/profile')


# 프로필 확인
@bp.route('/base/<int:user_id>/')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if user_id != user.id:
        flash("잘못된 접근 입니다.")
        return redirect(url_for('main.index'))
    return render_template('profile/profile.html', user=user)


# 작성글 조회
@bp.route('/list/<int:user_id>/')
def profile_list(user_id):
    page = request.args.get('page', type=int, default=1)
    user = User.query.get_or_404(user_id)
    if user_id != user.id:
        flash("잘못된 접근 입니다.")
        return redirect(url_for('main.index'))
    my_list = Question.query.where(Question.user_id == user.id).order_by(Question.create_date.desc())   # 내가 쓴 글만 가져와 작성일자가 최신인 순으로 정렬
    my_list = my_list.paginate(page, per_page=10)
    return render_template('profile/profile_list.html', my_list=my_list, user=user, page=page)


# 답글 조회
@bp.route('/answer/<int:user_id>/')
def answer_list(user_id):
    page = request.args.get('page', type=int, default=1)
    user = User.query.get_or_404(user_id)
    if user_id != user.id:
        flash("잘못된 접근 입니다.")
        return redirect(url_for('main.index'))
    my_answer = Answer.query.where(Answer.user_id == user.id).order_by(Answer.create_date.desc())   # 내가 쓴 답글만 가져와 작성일자가 최신인 순으로 정렬
    my_answer = my_answer.paginate(page, per_page=10)
    return render_template('profile/answer_list.html', my_answer=my_answer, user=user, page=page)


# 댓글 조회
@bp.route('/comment/<int:user_id>/')
def comment_list(user_id):
    page = request.args.get('page', type=int, default=1)
    user = User.query.get_or_404(user_id)
    if user_id != user.id:
        flash("잘못된 접근 입니다.")
        return redirect(url_for('main.index'))
    my_comment = Comment.query.where(Comment.user_id == user.id).order_by(Comment.create_date.desc())   # 내가 쓴 답글만 가져와 작성일자가 최신인 순으로 정렬
    my_comment = my_comment.paginate(page, per_page=10)
    return render_template('profile/comment_list.html', my_comment=my_comment, user=user, page=page)