from pydantic import BaseModel

class SuccessStoryBase(BaseModel):
    title: str
    content: str

class SuccessStoryCreate(SuccessStoryBase):
    pass

class SuccessStoryResponse(SuccessStoryBase):
    id: int

    class Config:
        from_attributes = True
