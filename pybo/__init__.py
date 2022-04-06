from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


# 오류페이지 처리 : 404
def page_not_found(e):
    return render_template('404.html'), 404
    # return문의 두번째 매개변수인 404를 명시적으로 적어주는게 필요. 만약 404 생략하면 오류 페이지는 나타나지만
    # 클라이언트는 200 코드를 수신하게 될 것이다.


# 오류페이지 처리 : 500
def server_error(e):
    return render_template('500.html'), 500


def create_app():  # 애플리케이션 팩토리 함수 => DB, url 호출, 필터 등 각종 확장기능 app에 부착하기
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    # config.py 파일에 작성한 항목을 app.config 환경 변수로 부르기 위해 해당 코드 추가. ~4/1
    # 4/2~ : app.config.from_object(config) -> app.config.from_envvar('APP_CONFIG_FILE') 로 변경
    # 이는 APP_CONFIG_FILE에 정의된 파일을 환경 파일로 사용하겠다는 의미


    # ORM
    db.init_app(app)  # db 객체 초기화
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)  # migrate 객체 초기화
    from . import models

    # 블루 프린트
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime  # 'datetime' = 필터명

    # markdown
    Markdown(app, extentions=['nl2br', 'fenced_code'])
        # nl2br : 줄바꿈 문자를 <br>로 바꿔줌.
        # fenced_code :  코드 표시 기능

    # 오류 페이지 : 404
    app.register_error_handler(404, page_not_found)

    # 오류 페이지 : 500
    app.register_error_handler(500, server_error)

    return app