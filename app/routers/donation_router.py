from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.donation_model import Donations
from ..schemas.donation_schema import DonationCreate

router = APIRouter(prefix="/donations", tags=["Donations"])

@router.post("/")
def create_donation(data: DonationCreate, db: Session = Depends(get_db)):
    donation = Donations(**data.model_dump())
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

@router.get("/")
def get_all_donations(db: Session = Depends(get_db)):
    return db.query(Donations).all()



@router.get("/{donation_id}")
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donations).filter(Donations.donation_id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation



