from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import CCTVCreate, CCTVUpdate, CCTVResponse
from models import CCTV
from app import get_db

router = APIRouter(prefix="/cctv", tags=["CCTV"])


@router.post("/", response_model=CCTVResponse)
def add_cctv(data: CCTVCreate, db: Session = Depends(get_db)):
    new = CCTV(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/", response_model=list[CCTVResponse])
def list_cctv(db: Session = Depends(get_db)):
    return db.query(CCTV).all()


@router.put("/{cctv_id}", response_model=CCTVResponse)
def update_cctv(cctv_id: int, data: CCTVUpdate, db: Session = Depends(get_db)):
    cam = db.query(CCTV).filter(CCTV.id == cctv_id).first()
    if not cam:
        raise HTTPException(404, "CCTV tidak ditemukan")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(cam, key, value)

    db.commit()
    db.refresh(cam)
    return cam


@router.delete("/{cctv_id}")
def delete_cctv(cctv_id: int, db: Session = Depends(get_db)):
    cam = db.query(CCTV).filter(CCTV.id == cctv_id).first()
    if not cam:
        raise HTTPException(404, "CCTV tidak ditemukan")

    db.delete(cam)
    db.commit()
    return {"message": "CCTV dihapus"}
