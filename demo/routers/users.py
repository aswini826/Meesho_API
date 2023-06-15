from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Customer

router = APIRouter(
    prefix='/Customer API',
    tags=['customer']
)

session = SessionLocal()


class CreateCustomerRequest(BaseModel):
    customer_id: int
    customer_name: str
    email: EmailStr
    age: int
    gender: str
    phone: str


class UpdateProductDetails(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/customer", status_code=status.HTTP_201_CREATED)
def create_customer(db: db_dependency,
                    create_customer_request: CreateCustomerRequest):
    if db.query(Customer).filter(Customer.customer_id == create_customer_request.customer_id).first():
        raise HTTPException(status_code=400, detail="Customer ID already exists")

    create_customer_model = Customer(
        customer_id=create_customer_request.customer_id,
        customer_name=create_customer_request.customer_name,
        email=create_customer_request.email,
        age=create_customer_request.age,
        gender=create_customer_request.gender,
        phone=create_customer_request.phone

    )

    db.add(create_customer_model)
    db.commit()
    db.refresh(create_customer_model)
    return {"message": "Customer created Successfully"}


@router.get("/catagory", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency,
                    page: int = Query(1, gt=0)):
    per_page = 4
    offset = (page - 1) * per_page
    return db.query(Customer).offset(offset).limit(per_page).all()


@router.put("/update_customer_details")
async def update_customer(update_customer_details: UpdateProductDetails,
                          db: db_dependency):
    user = db.query(Customer).filter(Customer.email == update_customer_details.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Email are already exists")

    db.commit()
    return {'message': 'Customer details changed Successfully'}


@router.delete('/delete_user/{user_id}')
def delete_user(user_id: int, db: db_dependency):
    user = db.query(Customer).filter(Customer.id == user_id).first()
    db.delete(user)
    db.commit()
    return {'message': 'Customer deleted Successfully'}
