from flask import Blueprint, url_for # 라우트가 설정된 함수명으로 URL을 역으로 찾아준다.
from werkzeug.utils import redirect  # 입력받은 URL로 리다이렉트 해준다.

# Blueprint : 라우트 함수를 구조 적으로 관리할 수 있다
# render_template : 템플릿 파일을 화면으로 렌더링하는 함수
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/') # 클래스 명으로 생성자 만들땐 맨 앞 매개변수에 객체 명을 넣어야 한다.



@bp.route('/hello')
# 특정 URL에 접속하면 바로 다음 줄에 있는 함수를 호출하는 플라스크의 데코레이터. https://wikidocs.net/83687 참고
def hello_pybo(): # URL에 '/'에 매핑되는 함수. 그 매핑을 @app.route('/')라는 애너테이션이 만들어 줌. 이런 걸 라우트 함수라고 함.
    return 'Hello, Pybo!'

@bp.route('/')
def index() :
    3/0 # 강제로 오류 발생
    return redirect(url_for('question._list')) # question은 등록한 블루프린트 이름, _list는 호출할 함수명.