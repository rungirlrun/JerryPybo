from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash, current_app
from werkzeug.utils import redirect
from .. import db
from sqlalchemy import func, nullslast
from ..models import Question, Answer, User, question_voter
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


def _nullslast(obj):
    if current_app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        return obj
    else:
        return nullslast(obj)


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)  # 페이지
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(_nullslast(sub_query.c.num_voter.desc()), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(_nullslast(sub_query.c.num_answer.desc()), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회 : 기회되면 코드 분석해보기
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # get_or_404 : 올바른 페이지를 호출하거나, 존재하지 않는 페이지를 요청받으면 404페이지 리턴
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)  # user_id=g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required  # 로그인이 필요한 동작에 추가하는 애너테이션
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)  # form 변수에 들어 있는 데이터(화면에 입력되어 있는 데이터)를 question 객체에 적용시켜줌.
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
