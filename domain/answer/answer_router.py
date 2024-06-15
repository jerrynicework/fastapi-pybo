from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/answer",
)

# 새로운 답변을 생성하는 엔드포인트 정의
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, # 위 url 경로 매개변수로 질문 ID를 받음
                  _answer_create: answer_schema.AnswerCreate, # 요청 본문에서 답변 생성 데이터를 받음
                  db: Session = Depends(get_db),
                  current_user : User = Depends(get_current_user)): # 의존성 주입을 통해 데이터베이스 세션 받기

    # create answer (도서관 직원이 책 대출 요청을 처리하는 과정)
    question = question_crud.get_question(db, question_id=question_id) # 질문객체 가져오기 (데이터베이스에서 해당 질문을 가져옴)
    if not question: # 질문이 존재하지 않으면 예외 발생
        raise HTTPException(status_code=404, detail="Question not found")
    

    # 답변 생성 (답변 객체를 생성하고 데이터베이스에 추가)
    answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user = current_user)
    

@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer





@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    answer_crud.update_answer(db=db, db_answer=db_answer,
                              answer_update=_answer_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)