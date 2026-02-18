from pydantic import BaseModel

from typing import Optional

class PlatformStatsBase(BaseModel):
    total_funds_raised: str
    lives_impacted: str
    successful_campaigns: str
    success_rate: str

class PlatformStatsCreate(BaseModel):
    lives_impacted: str
    successful_campaigns: str
    success_rate: str
    total_funds_raised: Optional[str] = None

class PlatformStatsResponse(PlatformStatsBase):
    id: int

    class Config:
        from_attributes = True
