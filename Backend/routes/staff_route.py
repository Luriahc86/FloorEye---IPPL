from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import StaffCreate, StaffUpdate, StaffResponse
from models import Staff
from database import get_db   # ✅ FIXED

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=StaffResponse)
def create_staff(data: StaffCreate, db: Session = Depends(get_db)):
    new = Staff(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.get("/", response_model=list[StaffResponse])
def get_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()

@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, data: StaffUpdate, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(404, "Staff tidak ditemukan")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)
    return staff

@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(404, "Staff tidak ditemukan")

    db.delete(staff)
    db.commit()
    return {"message": "Staff dihapus"}
