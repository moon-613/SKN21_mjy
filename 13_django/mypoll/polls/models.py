# model class들을 정의
from django.db import models

# model class 정의 - question (설문 질문) - choice (설문의 보기)
## 1. models.Model을 상속
## 2. class 변수로 Field를 정의: Field == DB column, Model 객체의 Instance 변수 이 둘에 대한 설정

# Model class 정의할 때 primary key Field를 선언하지 않으면,
# in (int auto_increment) 컬럼이 primary key 컬럼으로 자동으로 생성된다. 
class Question(models.Model):
    # Field 정의: 변수명 -(instance 변수명, column 이름)
    #            Field 객체를 할당. Field 객체 - column 설정 (type, null 허용 여부, ...)
    question_text =  models.CharField(max_length=200)  # CharField() -> 문자열 타입 (varchar)
    pub_date = models.DateTimeField(auto_now_add=True)  # Datetime Field: 일시 타입 (datetime, datetime.datetime)
    # auto_now_add: insert 될 때 일시 자동 입력.

    def __str__(self):
        return f"{self.id}. {self.question_text}"

    # SQL
    # create table question(
    #   question_text varchar(200),
    #   pub_date datetime current_timestamp
    # )


# 보기 테이블
class Choice(models.Model):

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # 정수 타입 (python도 int, DB도 int)
    question = models.ForeignKey(
        Question,  # 참조할 model class
        on_delete=models.CASCADE  # 참조값이 삭제된 경우 어떻게 할지 -> cascade: 삭제 
    )  # FK -> Question의 ID를 참조

    def __str__(self):
        return f"{self.id}. {self.choice_text}"

    # SQL
    # create table choice(
    #   choice_text varchar(200) not null,
    #   votes int not null default 0,
    #   question int,
    #   constraint q_fk foreign ket (question) references QUESTION(id)
    # )


# 모델 클래스 정의한 후에 Database에 어떻게 적용할지 정함
# project Root >  python manage.py makemigrations   # 모든 app들에 적용 
#              >  python manage.py makemigrations  polls  # polls app에만 적용 
#             -> table에 적용 (생성, 수정)할 코드를 작성

# python manage.py migrate    # 이게 실제 DB에 적용 (table 생성, 수정)