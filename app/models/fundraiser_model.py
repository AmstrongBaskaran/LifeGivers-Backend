from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from app.database import Base

class FundraiserMaster(Base):
    __tablename__ = "fundraiser_master"

    fundraiser_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    campaign_title = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)

    patient_name = Column(String, nullable=False)
    patient_age = Column(Integer, nullable=False)
    patient_relation = Column(String, nullable=False)
    hospital_name = Column(String, nullable=False)

    story_text = Column(Text, nullable=False)

    medical_report_url = Column(Text)
    hospital_report_url = Column(Text)
    id_proof_url = Column(Text)
    campaign_image_url = Column(Text)

    bank_account_number = Column(String, nullable=False)
    ifsc_code = Column(String, nullable=False)
    phone_number = Column(String)
    pan_number = Column(String)

    agreed_terms = Column(Boolean, default=False)
    status = Column(String, default="pending")
