from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.platform_stats_model import PlatformStats
from app.models.donation_model import Donations
from sqlalchemy import func
from app.schemas.platform_stats_schema import PlatformStatsCreate, PlatformStatsResponse

router = APIRouter(
    prefix="/platform-stats",
    tags=["Platform Stats"]
)

@router.get("/", response_model=PlatformStatsResponse)
def get_platform_stats(db: Session = Depends(get_db)):
    # Calculate real total from donations
    total_sum = db.query(func.sum(Donations.amount)).scalar() or 0
    formatted_total = f"₹{total_sum:,.0f}"

    stats = db.query(PlatformStats).first()
    if not stats:
        stats = PlatformStats(
            total_funds_raised=formatted_total,
            lives_impacted="15,240",
            successful_campaigns="2,847",
            success_rate="98.5%"
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
    else:
        # Sync the total just in case
        stats.total_funds_raised = formatted_total
        db.commit()
        
    return stats

@router.put("/", response_model=PlatformStatsResponse)
def update_platform_stats(stats_in: PlatformStatsCreate, db: Session = Depends(get_db)):
    stats = db.query(PlatformStats).first()
    if not stats:
        stats = PlatformStats(**stats_in.dict())
        db.add(stats)
    else:
        # We DON'T update total_funds_raised from the input, it's automatic
        stats.lives_impacted = stats_in.lives_impacted
        stats.successful_campaigns = stats_in.successful_campaigns
        stats.success_rate = stats_in.success_rate
    
    db.commit()
    db.refresh(stats)
    return stats
