from fastapi import APIRouter, Depends, HTTPException # 사서가 일을 하기 위해 필요한 도구를 직접 만들지 않고, 도서관 시스템이 제공해주는 방식
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix = "/api/question",
) # 도서관 안내 데스크를 설치하고 '질문' 카테고리 안내 표지를 달았음


# 질문 목록 엔드포인트
# 방문객이 "question_schema.Question리스트를 보여주세요" 라고 요청하면, 사서(=db)가 질문 목록을 가져와서 보여줌
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword : str = ''):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }

# 질문 세부 정보 엔드포인트
# 방문객이 특정 질문의 세부 정보를 알고 싶어 하면, 사서가 데이터베이스에서 해당 질문의 세부 정보를 찾아서 제공
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question



# FastAPI를 사용하여 새로운 질문을 생성하는 API 엔드포인트를 정의한 예제
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user : User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,
                                  user=current_user)
    
# 먼저 입력 항목인 QuestionUpdate의 question_id로 db_question을 조회한다. 조회 결과가 없을 경우에는
# "데이터를 찾을 수 없습니다" 라는 400 오류를 발생시킨다. 그리고 조회환 db_question의 작성자와 현재 로그인한 사용자(current_user)가
# 동일인인지 검증한다. 만약 다른 사람일 경우 "수정 권한이 없습니다" 라는 400 오류를 발생시킨다.
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)
    



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)