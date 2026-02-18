from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.fundraiser_model import FundraiserMaster
from app.models.donation_model import Donations

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/")
@router.get("")
def get_stats(db: Session = Depends(get_db)):
    # Calculate statistics for the Admin Dashboard
    # Count how many fundraisers are total vs approved vs pending
    total_fundraisers = db.query(FundraiserMaster).count()
    verified_fundraisers = db.query(FundraiserMaster).filter(FundraiserMaster.status == "approved").count()
    pending_fundraisers = db.query(FundraiserMaster).filter(FundraiserMaster.status == "pending").count()
    
    # Calculate Total Donations collected across the entire platform
    total_donations = db.query(func.sum(Donations.amount)).scalar() or 0
    
    print(f"DEBUG Stats: F={total_fundraisers}, V={verified_fundraisers}, P={pending_fundraisers}, D={total_donations}")
    
    return {
        "total_fundraisers": total_fundraisers,
        "verified_fundraisers": verified_fundraisers,
        "pending_fundraisers": pending_fundraisers,
        "total_donations": total_donations
    }
