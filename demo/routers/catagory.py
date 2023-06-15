from datetime import datetime

from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Catagory

router = APIRouter(
    prefix='/Catagory API',
    tags=['catagory']
)

session = SessionLocal()


class CreateCatagoryRequest(BaseModel):
    catagory_id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class UpdateCatagory(BaseModel):
    name: str
    description: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/catagory", status_code=status.HTTP_201_CREATED)
def create_catagory(db: db_dependency,
                    create_catagory_request: CreateCatagoryRequest):
    if db.query(Catagory).filter(Catagory.catagory_id == create_catagory_request.catagory_id).first():
        raise HTTPException(status_code=400, detail="Catagory already exists")

    create_catagory_model = Catagory(
        catagory_id=create_catagory_request.catagory_id,
        name=create_catagory_request.name,
        description=create_catagory_request.description,
        created_at=create_catagory_request.created_at,
        updated_at=create_catagory_request.updated_at
    )

    db.add(create_catagory_model)
    db.commit()
    db.refresh(create_catagory_model)
    return {"message": "Catagory created Successfully"}


@router.get("/catagory", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency,
                    page: int = Query(1, gt=0)):
    per_page = 5
    offset = (page - 1) * per_page
    return db.query(Catagory).offset(offset).limit(per_page).all()


@router.put("/update_catagory_details")
async def update_catagory(update_catagory_details: UpdateCatagory,
                          db: db_dependency):
    user = db.query(Catagory).filter(Catagory.name == update_catagory_details.name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This name are already exists")

    db.commit()
    return {'message': 'Catagory details changed Successfully'}


@router.delete('/delete_user/{user_id}')
def delete_user(user_id: int, db: db_dependency):
    user = db.query(Catagory).filter(Catagory.id == user_id).first()
    db.delete(user)
    db.commit()
    return {'message': 'Catagory deleted Successfully'}
