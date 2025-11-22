from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ==========================
# User Table
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="staff")   # admin / staff

    staff = relationship("Staff", back_populates="user", uselist=False)


# ==========================
# Staff Table
# ==========================
class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone = Column(String(20))
    shift = Column(String(50))

    user = relationship("User", back_populates="staff")


# ==========================
# CCTV Table
# ==========================
class CCTV(Base):
    __tablename__ = "cctv"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    rtsp_url = Column(Text)
    location = Column(String(100))


# ==========================
# Laporan Kebersihan
# ==========================
class Laporan(Base):
    __tablename__ = "laporan"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    status = Column(String(20))  # bersih / kotor
    timestamp = Column(DateTime, default=datetime.utcnow)
    lokasi = Column(String(100))

    staff = relationship("Staff")
