from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from app.database import Base
from datetime import datetime

class Donations(Base):
    __tablename__ = "donations"

    donation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)  # Allow anonymous donations
    fundraiser_id = Column(Integer, ForeignKey("fundraiser_master.fundraiser_id", ondelete="CASCADE"))
    donor_name = Column(String)
    amount = Column(Float)
    payment_method = Column(String)  # UPI, GPay, PhonePay, BankTransfer
    donation_date = Column(DateTime, default=datetime.utcnow)
