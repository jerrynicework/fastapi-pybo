import datetime
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user : User | None
    question_id : int # 프론트엔드에서 답변을 수정한 후에 다시 원래의 질문 상세 화면으로 돌아가기 위해서 해당 답변이 작성된 질문의 고유번호 필요
    modify_date : datetime.datetime | None = None 



class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int