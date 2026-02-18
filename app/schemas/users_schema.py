from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    fullname : str
    phone_number : str
    password : str
    role: str = "user"
    

class UserResponse(BaseModel):
    user_id: int
    fullname: str
    phone_number: str

    @field_validator('phone_number', mode='before')
    @classmethod
    def convert_phone_to_str(cls, v):
        return str(v)

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    phone_number : str
    password : str

    @field_validator('phone_number', mode='before')
    @classmethod
    def convert_phone_to_str(cls, v):
        return str(v)
