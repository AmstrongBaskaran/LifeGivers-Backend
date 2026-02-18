from pydantic import BaseModel


class DonationCreate(BaseModel):
    user_id: int | None = None
    fundraiser_id: int | None = None
    donor_name: str
    amount: float
    payment_method: str



    