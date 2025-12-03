from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserEntity(BaseModel):
    cod: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    second_last_name: Optional[str] = None
    email: EmailStr
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    username: str
    password_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def age(self) -> Optional[int]:
        """Calcula la edad a partir de la fecha de nacimiento"""
        if not self.date_of_birth:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    def serialize(self) -> dict:
        """Convierte el modelo a dict serializando fechas como string ISO"""
        data = self.model_dump()  # usa dict() si estás en Pydantic v1
        if self.date_of_birth:
            data["date_of_birth"] = self.date_of_birth.isoformat()
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            data["updated_at"] = self.updated_at.isoformat()
        return data

