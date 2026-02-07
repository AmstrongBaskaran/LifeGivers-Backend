from pydantic import BaseModel


class FundraiserCreate(BaseModel):
    user_id : int
    campaign_title : str
    target_amount : float
    category : str
    location : str
    patient_name : str
    patient_age : int
    patient_relation : str
    hospital_name : str
    story_text : str
    medical_report_url : str | None = None
    hospital_report_url : str | None = None
    id_proof_url : str | None = None
    campaign_image_url : str |None = None
    bank_account_number : str 
    ifsc_code : str
    phone_number : str | None = None
    pan_number : str | None = None
    agreed_terms : bool
    

class UploadImage(BaseModel):
    medical_report_url : str | None = None
    hospital_report_url : str | None = None
    id_proof_url : str | None = None
    campaign_image_url : str | None = None
