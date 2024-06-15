# sqlalchemy = 도서관의 책들을 잘 관리하고 접근할 수 있게 도와주는 도구 
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./myapi.db' #데이터베이스 접속주소(=도서관의 주소)


# 데이터베이스 엔진 설정 : 데이터베이스와의 연결을 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False}
) # 엔진 = 도서관의 문을 열고 들어가는 열쇠


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 도서관에서 책을 대출하고 반납하는 절차

Base = declarative_base() # 도서관의 책의 형식
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
} # MetaData 클래스를 사용하여 데이터베이스의 이름 규칙을 새롭게 정의 (수동)
Base.metadata = MetaData(naming_convention=naming_convention)




def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()
