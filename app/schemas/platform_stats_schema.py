from pydantic import BaseModel

class PlatformStatsBase(BaseModel):
    total_funds_raised: str
    lives_impacted: str
    successful_campaigns: str
    success_rate: str

class PlatformStatsCreate(PlatformStatsBase):
    pass

class PlatformStatsResponse(PlatformStatsBase):
    id: int

    class Config:
        from_attributes = True
