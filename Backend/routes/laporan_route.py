from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import LaporanCreate, LaporanResponse
from models import Laporan
from app import get_db

router = APIRouter(prefix="/laporan", tags=["Laporan"])


@router.post("/", response_model=LaporanResponse)
def buat_laporan(data: LaporanCreate, db: Session = Depends(get_db)):
    new = Laporan(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/", response_model=list[LaporanResponse])
def semua_laporan(db: Session = Depends(get_db)):
    return db.query(Laporan).all()
