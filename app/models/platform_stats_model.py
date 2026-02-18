from sqlalchemy import Column, Integer, String
from app.database import Base

class PlatformStats(Base):
    __tablename__ = "platform_stats"

    id = Column(Integer, primary_key=True, index=True)
    total_funds_raised = Column(String, default="₹0")
    lives_impacted = Column(String, default="0")
    successful_campaigns = Column(String, default="0")
    success_rate = Column(String, default="0")
