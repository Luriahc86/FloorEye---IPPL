from pydantic import BaseModel
from datetime import datetime


# =====================================
# USER (Auth)
# =====================================

class UserBase(BaseModel):
    username: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True    # Pydantic v2 (pengganti orm_mode)

# =====================================
# STAFF
# =====================================
class StaffBase(BaseModel):
    phone: str | None = None
    shift: str | None = None

class StaffCreate(StaffBase):
    user_id: int

class StaffUpdate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# =====================================
# CCTV
# =====================================
class CCTVBase(BaseModel):
    name: str
    rtsp_url: str
    location: str

class CCTVCreate(CCTVBase):
    pass

class CCTVUpdate(BaseModel):
    name: str | None = None
    rtsp_url: str | None = None
    location: str | None = None

class CCTVResponse(CCTVBase):
    id: int

    class Config:
        orm_mode = True


# =====================================
# LAPORAN
# =====================================
class LaporanBase(BaseModel):
    staff_id: int
    status: str
    lokasi: str

class LaporanCreate(LaporanBase):
    pass

class LaporanResponse(LaporanBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
